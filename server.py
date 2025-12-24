from flask import Flask, request
from flask_cors import CORS
import os
import asyncio
from telegram import Bot

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

bot = Bot(token=BOT_TOKEN)

@app.route("/")
def health():
    return "OK", 200

async def send_photo(image_bytes):
    await bot.send_photo(chat_id=CHAT_ID, photo=image_bytes)

@app.route("/capture", methods=["POST"])
def capture():
    image = request.files["image"]
    img_bytes = image.read()

    # Fire-and-forget async task
    asyncio.get_event_loop().create_task(send_photo(img_bytes))

    return "OK", 200
