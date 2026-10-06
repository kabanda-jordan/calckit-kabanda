"""A browser calculator for calckit-kabanda.

Run it with the ``calc-kabanda`` command, which starts a local server and opens
your default browser. Nothing is sent anywhere: the page and the API both run on
your own machine.
"""

from __future__ import annotations

import threading
import webbrowser

from flask import Flask, jsonify, request

from .evaluate import evaluate
from .errors import CalcError
from .statistics import (
    geometric_mean,
    harmonic_mean,
    maximum,
    mean,
    median,
    minimum,
    mode,
    standard_deviation,
    total,
    value_range,
    variance,
)

STATS = {
    "total": total,
    "mean": mean,
    "average": mean,
    "median": median,
    "mode": mode,
    "min": minimum,
    "max": maximum,
    "range": value_range,
    "variance": variance,
    "stdev": standard_deviation,
    "geomean": geometric_mean,
    "harmmean": harmonic_mean,
}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>calc-kabanda</title>
<style>
  :root {
    --bg: #12141a; --panel: #1b1e26; --key: #262a34; --key-hi: #333846;
    --accent: #ff9f0a; --text: #f2f4f8; --muted: #8b93a5; --danger: #ff6b6b;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh; background: var(--bg); color: var(--text);
    font-family: ui-sans-serif, system-ui, "Segoe UI", Roboto, sans-serif;
    display: flex; align-items: center; justify-content: center; padding: 24px;
  }
  .app { width: 100%; max-width: 400px; }
  header {
    display: flex; align-items: baseline; justify-content: space-between;
    margin-bottom: 14px;
  }
  h1 { font-size: 15px; font-weight: 600; letter-spacing: .04em; margin: 0; }
  .tag { font-size: 12px; color: var(--muted); }
  .screen {
    background: var(--panel); border-radius: 16px; padding: 18px 20px 20px;
    margin-bottom: 14px; min-height: 116px;
    display: flex; flex-direction: column; justify-content: flex-end;
  }
  #expression {
    color: var(--muted); font-size: 15px; min-height: 22px; word-break: break-all;
    font-family: ui-monospace, "Cascadia Code", Consolas, monospace;
  }
  #result {
    font-size: 40px; font-weight: 600; text-align: right; margin-top: 6px;
    word-break: break-all; line-height: 1.1;
  }
  #result.error { color: var(--danger); font-size: 17px; font-weight: 500; }
  .pad { display: grid; grid-template-columns: repeat(4, 1fr); gap: 9px; }
  button {
    background: var(--key); color: var(--text); border: 0; border-radius: 12px;
    padding: 17px 0; font-size: 17px; cursor: pointer; transition: .12s;
    font-family: inherit;
  }
  button:hover { background: var(--key-hi); }
  button:active { transform: scale(.95); }
  button.op { background: #313643; color: var(--accent); font-weight: 600; }
  button.fn { background: #2b303c; color: var(--muted); font-size: 14px; }
  button.wide { grid-column: span 2; }
  button.go { background: var(--accent); color: #12141a; font-weight: 700; }
  .stats { margin-top: 16px; background: var(--panel); border-radius: 16px; padding: 16px 20px; }
  .stats h2 { font-size: 12px; text-transform: uppercase; letter-spacing: .09em;
              color: var(--muted); margin: 0 0 10px; font-weight: 600; }
  .row { display: flex; gap: 8px; margin-bottom: 10px; }
  input, select {
    background: var(--key); border: 0; border-radius: 10px; color: var(--text);
    padding: 11px 13px; font-size: 14px; font-family: inherit; width: 100%;
  }
  #numbers { font-family: ui-monospace, Consolas, monospace; }
  #statsOut { color: var(--accent); font-weight: 600; font-size: 17px; min-height: 24px;
              text-align: right; font-family: ui-monospace, Consolas, monospace; }
  footer { margin-top: 16px; font-size: 12px; color: var(--muted); text-align: center; }
</style>
</head>
<body>
<div class="app">
  <header>
    <h1>calc-kabanda</h1>
    <span class="tag">v__VERSION__</span>
  </header>

  <div class="screen">
    <div id="expression">&nbsp;</div>
    <div id="result">0</div>
  </div>

  <div class="pad" id="pad"></div>

  <div class="stats">
    <h2>Statistics</h2>
    <div class="row">
      <input id="numbers" placeholder="2, 4, 6, 8" autocomplete="off">
      <select id="statOp"></select>
    </div>
    <div id="statsOut">&nbsp;</div>
  </div>

  <footer>calckit-kabanda &middot; MIT</footer>
</div>

<script>
const KEYS = [
  ["C", "fn"], ["(", "fn"], [")", "fn"], ["/", "op"],
  ["7", ""], ["8", ""], ["9", ""], ["*", "op"],
  ["4", ""], ["5", ""], ["6", ""], ["-", "op"],
  ["1", ""], ["2", ""], ["3", ""], ["+", "op"],
  ["0", ""], [".", ""], ["^", "op"], ["%", "op"],
  ["sqrt(", "fn wide"], ["⌫", "fn wide"], ["=", "go wide"]
];

const pad = document.getElementById("pad");
for (const [label, cls] of KEYS) {
  const b = document.createElement("button");
  b.textContent = label;
  b.className = cls;
  b.addEventListener("click", () => press(label));
  pad.appendChild(b);
}

const stats = document.getElementById("statOp");
for (const name of __STATS__) {
  const o = document.createElement("option");
  o.value = o.textContent = name;
  stats.appendChild(o);
}

const out = document.getElementById("result");
const expr = document.getElementById("expression");
let buffer = "";

function show(value, error) {
  expr.textContent = value || "\\u00a0";
  out.textContent = error ? value : value;
  out.classList.toggle("error", Boolean(error));
}

function press(label) {
  if (label === "C") { buffer = ""; show("0"); return; }
  if (label === "⌫") { buffer = buffer.slice(0, -1); show(buffer || "0"); return; }
  if (label === "=") { return send(); }
  buffer += label === "^" ? "**" : label;
  show(buffer);
}

async function send() {
  if (!buffer.trim()) return;
  const response = await fetch("/api/calc", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expression: buffer })
  });
  const data = await response.json();
  if (data.error) show(data.error, true);
  else { expr.textContent = buffer + " ="; out.textContent = data.result; out.classList.remove("error"); }
}

document.getElementById("numbers").addEventListener("input", async (event) => {
  const raw = event.target.value.trim();
  if (!raw) { document.getElementById("statsOut").innerHTML = "&nbsp;"; return; }
  const numbers = raw.split(",").map(s => parseFloat(s.trim())).filter(n => !isNaN(n));
  if (!numbers.length) return;
  const response = await fetch("/api/stats", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ numbers, operation: stats.value })
  });
  const data = await response.json();
  document.getElementById("statsOut").textContent = data.error || data.result;
});

window.addEventListener("keydown", (event) => {
  const map = { "/": "/", "*": "*", "-": "-", "+": "+", ".": ".", "(": "(", ")": ")" };
  if (/^[0-9]$/.test(event.key)) press(event.key);
  else if (map[event.key]) press(map[event.key]);
  else if (event.key === "Enter" || event.key === "=") { event.preventDefault(); press("="); }
  else if (event.key === "Backspace") press("⌫");
  else if (event.key === "Escape") press("C");
});
</script>
</body>
</html>
"""


def _tidy(value: float) -> str:
    """Render a float for display.

    Snaps values that are a rounding error away from a whole number, so
    ``log(1000)`` shows ``3`` rather than ``2.9999999999999996``.
    """
    value = round(float(value), 10)
    nearest = round(value)
    if abs(value - nearest) < 1e-9:
        return str(int(nearest))
    return str(value)


def create_app() -> Flask:
    """Build the Flask application."""
    from . import __version__

    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    @app.get("/")
    def index() -> str:
        page = PAGE.replace("__VERSION__", __version__)
        return page.replace("__STATS__", repr(sorted(STATS)))

    @app.post("/api/calc")
    def api_calc():
        payload = request.get_json(silent=True) or {}
        expression = payload.get("expression", "")
        try:
            value = evaluate(expression)
        except CalcError as exc:
            return jsonify(error=str(exc)), 200
        except (ValueError, OverflowError, ZeroDivisionError, TypeError) as exc:
            return jsonify(error=f"Cannot calculate that: {exc}"), 200
        return jsonify(result=_tidy(value))

    @app.post("/api/stats")
    def api_stats():
        payload = request.get_json(silent=True) or {}
        numbers = payload.get("numbers") or []
        operation = str(payload.get("operation", "mean"))
        function = STATS.get(operation)
        if function is None:
            return jsonify(error=f"Unknown statistic {operation!r}"), 200
        try:
            value = function(*numbers)
        except CalcError as exc:
            return jsonify(error=str(exc)), 200
        except (TypeError, ValueError) as exc:
            return jsonify(error=f"Cannot calculate that: {exc}"), 200
        return jsonify(result=_tidy(value))

    return app


def main(host: str = "127.0.0.1", port: int = 5000, open_browser: bool = True) -> int:
    """Start the calculator server and open it in a browser."""
    url = f"http://{host}:{port}"
    print(f"calc-kabanda running at {url}")
    print("Press Ctrl+C to stop.")

    if open_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    create_app().run(host=host, port=port, debug=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())