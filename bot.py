from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import yt_dlp
import time
import os

# Функція для завантаження відео
def download_video(url):
    timestamp = int(time.time())  # Унікальна мітка часу
    filename = f"downloaded_video_{timestamp}.mp4"
    options = {
        'outtmpl': filename,  # Динамічне ім'я файлу
        'format': 'mp4'
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    return filename

# Обробник команди /start
async def start(update: Update, context):
    await update.message.reply_text("Привіт Шкіряний! Надішли мені посилання на TikTok або Instagram відео, і я завантажу його для тебе!")

# Обробник повідомлень із посиланнями
async def handle_message(update: Update, context):
    url = update.message.text
    try:
        video_path = download_video(url)  # Завантажуємо відео
        await update.message.reply_video(video=open(video_path, 'rb'))  # Відправляємо відео
        os.remove(video_path)  # Видаляємо файл після надсилання
    except Exception as e:
        await update.message.reply_text(f"Помилка: {str(e)}")

# Налаштування бота
if __name__ == "__main__":
    TOKEN = os.getenv("7833529200:AAFwgSYGCUqCfT8zXd3dxQCWnB0sYtLWqo4")  # Отримуємо токен з середовища
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущений!")
    app.run_polling()
