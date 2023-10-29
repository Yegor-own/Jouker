import telegram.error
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, PicklePersistence
import env

from yt_dlp import YoutubeDL
import os
import uuid


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет я Джокербот помогу скачать любое видео из Vk, YouTube или Dzen.\nПросто кидай мне сылку, а я попробую скачать.")


async def load(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id = str(uuid.uuid4())
    URL = update.message.text
    opts = {'outtmpl': './' + id+".mp4"}
    path = id+".mp4"

    await update.message.reply_text('Скачиваю это может занять время')

    err_code = 0
    with YoutubeDL(opts) as ydl:
        err_code = ydl.download(URL)

    if err_code:
        await update.message.reply_text('Упс что-то пошло не так')
    else:

        await update.message.reply_video(video=open(path, 'rb'))
        os.remove(path)



my_persistence = PicklePersistence(filepath='per')

app = (ApplicationBuilder().token(env.BOT_TOKEN) \
       .local_mode(local_mode=True) \
       .base_url("http://localhost:8081/bot") \
       .build())

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, load))

app.run_polling()
