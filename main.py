import telebot
import yt_dlp
import os

TOKEN = os.environ.get("8493058967:AAGH7p5q2M3PcvZ_CiZwicSCMou6n463Nrw")

if not TOKEN:
    print("TOKEN not found")
    exit()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Отправь ссылку на видео")

@bot.message_handler(func=lambda message: True)
def download(message):
    url = message.text
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(filename)

    except Exception as e:
        bot.reply_to(message, "Ошибка при скачивании")

bot.infinity_polling()
