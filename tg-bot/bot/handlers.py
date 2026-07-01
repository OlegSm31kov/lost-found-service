from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

from keyboards import menu_keyboard
from backend_client import find_item

DATE = 0
STATION = 1
SUMMARY = 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Что вы хотите сделать?",reply_markup=menu_keyboard)

async def new_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите дату утери в формате ДД.ММ.ГГ")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["date"] = datetime.strptime(update.message.text, "%d.%m.%y").date()
        await update.message.reply_text(
            "Введите станцию, где вы потеряли вещь"
        )
        return STATION
    except ValueError:
        await update.message.reply_text(
            "Неверный формат даты.\n"
            "Используйте ДД.ММ.ГГ или ДД.ММ.ГГГГ."
        )
        return DATE

async def get_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # todo: либо сделать выбор, либо добавить проверку
    context.user_data["station"] = update.message.text

    await update.message.reply_text(
        "Введите описание утерянной вещи\n"
        "Постарайтесь описать её как можно подробнее, "
        "если это пакет или сумка - опишите содержимое"
    )

    return SUMMARY

async def get_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["summary"] = update.message.text
    await update.message.reply_text("Ищем, есть ли у нас такая вещь...")

    result = await find_item(context.user_data)
    await update.message.reply_text(f"Ответ:\n{result}")

    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Создание заявки отменено")
    return ConversationHandler.END

conversation = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex("^Подать новую заявку$"),
            new_request
        )
    ],

    states={
        DATE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_date
            )
        ],

        STATION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_station
            )
        ],

        SUMMARY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_summary
            )
        ],
    },

    fallbacks=[]
)