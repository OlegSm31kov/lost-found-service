import os
from pathlib import Path

from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, filters, ApplicationBuilder

from keyboards import menu_keyboard
from handlers import conversation

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Здравствуйте! Я - бот, который поможет "
                                    "найти вещи, потерянные в метро",
                                    reply_markup=menu_keyboard)

def main():
    TOKEN = os.getenv("TOKEN")
    print(f"TOKEN = {TOKEN!r}")
    print(os.getcwd())
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(conversation)
    application.run_polling()

if __name__ == "__main__":
    main()