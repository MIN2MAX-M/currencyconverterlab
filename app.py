import os
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv("APIKEY")
RAPIDAPI_HOST = os.getenv("APIHOST")

URL = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"


def rapidapi_headers():
    if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
        raise RuntimeError("Missing APIKEY or APIHOST env vars")
    return {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["GET"])
def get_currency_value():
    source_currency = request.args.get("from", default="USD", type=str).upper()
    target_currency = request.args.get("to", default="EUR", type=str).upper()
    amount = request.args.get("amount", default=1.0, type=float)

    params = {"from": source_currency, "to": target_currency, "amount": amount}

    try:
        r = requests.get(URL, headers=rapidapi_headers(), params=params, timeout=10)
        # If RapidAPI returns an error code, surface it clearly
        if r.status_code != 200:
            return jsonify({"error": "RapidAPI request failed", "status": r.status_code, "body": r.text}), r.status_code
        return jsonify(r.json())
    except requests.Timeout:
        return jsonify({"error": "RapidAPI timeout"}), 504
    except requests.RequestException as e:
        return jsonify({"error": "Request error", "details": str(e)}), 502


if __name__ == "__main__":
    env = os.getenv("FLASK_ENV", "development")
    debug_mode = env == "development"
    app.run(debug=debug_mode, host="0.0.0.0", port=5555)
