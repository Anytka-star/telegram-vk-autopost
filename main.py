
import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
VK_GROUP_ID = os.getenv("VK_GROUP_ID")
VK_ACCESS_TOKEN = os.getenv("VK_ACCESS_TOKEN")

logging.basicConfig(level=logging.INFO)

async def forward_to_vk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.channel_post:
        return

    text = update.channel_post.text_html or update.channel_post.caption_html
    if not text:
        return

    response = requests.post(
        "https://api.vk.com/method/wall.post",
        params={
            "owner_id": f"-{VK_GROUP_ID}",
            "from_group": 1,
            "message": text,
            "access_token": VK_ACCESS_TOKEN,
            "v": "5.199"
        }
    )
    logging.info(f"VK response: {response.text}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, forward_to_vk))
    app.run_polling()
