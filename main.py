import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirim link TikTok ke saya untuk download tanpa watermark.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "tiktok.com" not in url:
        await update.message.reply_text("Kirim link TikTok yang valid ya!")
        return

    api_url = f"https://tikwm.com/api/?url={url}"
    r = requests.get(api_url).json()
    
    if r["data"]:
        video_url = r["data"]["play"]
        await update.message.reply_video(video=video_url, caption="Ini videonya tanpa watermark!")
    else:
        await update.message.reply_text("Gagal mengambil video. Coba lagi.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
