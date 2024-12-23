from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import yt_dlp
import time
import os

# Function to download video
def download_video(url):
    timestamp = int(time.time())  # Unique timestamp
    filename = f"downloaded_video_{timestamp}.mp4"
    options = {
        'outtmpl': filename,  # Dynamic file name
        'format': 'mp4'
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    return filename

# Command handler for /start
async def start(update: Update, context):
    await update.message.reply_text("Привіт Шкіряний! Надішли мені посилання на TikTok або Instagram відео, і я завантажу його для тебе!")

# Message handler for video links
async def handle_message(update: Update, context):
    message = update.message
    chat_type = message.chat.type

    # Перевіряємо, чи бот у групі, і чи повідомлення адресоване йому
    if chat_type in ["group", "supergroup"]:
        if not (message.text.startswith(f"@{context.bot.username}") or message.reply_to_message and message.reply_to_message.from_user.id == context.bot.id):
            return  # Ігноруємо, якщо бот не згадано

    url = message.text.replace(f"@{context.bot.username}", "").strip()  # Видаляємо згадку про бота
    try:
        video_path = download_video(url)  # Download video
        with open(video_path, 'rb') as video_file:
            await message.reply_video(video=video_file)  # Send video
        os.remove(video_path)  # Delete file after sending
    except Exception as e:
        await message.reply_text(f"Не вдалося завантажити відео. Перевірте посилання або спробуйте пізніше. Помилка: {str(e)}")

# Bot setup
if __name__ == "__main__":
    TOKEN = "7833529200:AAFwgSYGCUqCfT8zXd3dxQCWnB0sYtLWqo4"  # Retrieve token from environment
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущений!")
    app.run_polling()
