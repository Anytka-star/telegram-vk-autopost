import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

VK_ACCESS_TOKEN = os.environ.get("VK_ACCESS_TOKEN")
VK_GROUP_ID = os.environ.get("VK_GROUP_ID")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    message = update.message
    text = message.text

    # Отправка в ВКонтакте
    vk_api_url = "https://api.vk.com/method/wall.post"
    params = {
        "access_token": VK_ACCESS_TOKEN,
        "v": "5.199",
        "owner_id": f"-{VK_GROUP_ID}",
        "message": text
    }
    response = requests.post(vk_api_url, data=params)

    if response.ok:
        print("Успешно отправлено в ВКонтакте")
    else:
        print("Ошибка при отправке в ВКонтакте:", response.text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    app.add_handler(handler)
    print("Бот запущен")
    app.run_polling()
