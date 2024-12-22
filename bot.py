from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import yt_dlp


# Функція для завантаження відео
def download_video(url):
    options = {
        'outtmpl': 'downloaded_video.%(ext)s',
        'format': 'mp4'
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    return 'downloaded_video.mp4'


# Обробник стартової команди
async def start(update: Update, context):
    await update.message.reply_text(
        "Привіт Шкіряний! Надішли мені посилання на TikTok або Instagram відео, і я завантажу його для тебе!")


# Обробник посилань
async def handle_message(update: Update, context):
    url = update.message.text
    try:
        video_path = download_video(url)
        await update.message.reply_video(video=open(video_path, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"Помилка: {str(e)}")


# Налаштування бота
if __name__ == "__main__":
    app = ApplicationBuilder().token("7833529200:AAFwgSYGCUqCfT8zXd3dxQCWnB0sYtLWqo4").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущений!")
    app.run_polling()
