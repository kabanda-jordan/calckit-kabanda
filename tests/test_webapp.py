import pytest

from calc_toolkit.webapp import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def calc(client, expression):
    return client.post("/api/calc", json={"expression": expression}).get_json()


def stats(client, numbers, operation="mean"):
    return client.post(
        "/api/stats", json={"numbers": numbers, "operation": operation}
    ).get_json()


def test_index_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "calc-kabanda" in body
    assert "placeholder" in body


def test_calc_endpoint(client):
    assert calc(client, "2 + 3")["result"] == "5"
    assert calc(client, "2 + 3 * 4")["result"] == "14"
    assert calc(client, "sqrt(16)")["result"] == "4"
    assert calc(client, "10 / 4")["result"] == "2.5"


def test_calc_reports_errors_without_crashing(client):
    assert "error" in calc(client, "1 / 0")
    assert "error" in calc(client, "2 +")
    assert "error" in calc(client, "__import__('os')")


def test_stats_endpoint(client):
    assert stats(client, [2, 4, 6, 8])["result"] == "5"
    assert stats(client, [1, 3, 2], "median")["result"] == "2"
    assert stats(client, [1, 2, 2], "mode")["result"] == "2"
    assert stats(client, [3, 1, 2], "min")["result"] == "1"
    assert stats(client, [3, 1, 2], "max")["result"] == "3"


def test_stats_errors(client):
    assert "error" in stats(client, [], "mean")
    assert "error" in stats(client, [1, 2], "nonsense")
    assert "error" in stats(client, [1, 0], "geomean")


def test_malformed_json_is_handled(client):
    response = client.post(
        "/api/calc", data="not json", content_type="application/json"
    )
    assert response.status_code == 200
    assert "error" in response.get_json()