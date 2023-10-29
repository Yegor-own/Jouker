import telegram.error
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from yt_dlp import YoutubeDL
import os
import uuid



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет я Джокербот помогу скачать любое видео из Vk, YouTube или Dzen.\nПросто кидай мне сылку, а я попробую скачать.")

async def load(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    id = str(uuid.uuid4())
    URL = update.message.text
    opts = {'outtmpl': './' + id + '.%(ext)s'}
    path = id + ".mp4"
    err_code = 0
    with YoutubeDL(opts) as ydl:
        err_code = ydl.download(URL)

    if err_code:
        await update.message.reply_text('Упс что-то пошло не так')
    else:
        try:
            await update.message.reply_video(video=open(path, 'rb'))
        except telegram.error.NetworkError:
            await update.message.reply_text('Похоже видео слшком большое')
        os.remove(path)


app = ApplicationBuilder().token("6583238890:AAGh4IfVBy1RB3J5-fE4h4SHUVr7rklgrRU").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, load))

app.run_polling()
