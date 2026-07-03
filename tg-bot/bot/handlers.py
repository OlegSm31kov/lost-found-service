from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, CallbackQueryHandler, filters

from keyboards import menu_keyboard, location_keyboard
from backend_client import find_item

DATE = 0
STATION = 1
LOCATION = 2
SUMMARY = 3

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Что вы хотите сделать?",reply_markup=menu_keyboard)

async def new_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "Опишите потерянную вещь для поиска\n"
        "Постарайтесь описать её как можно более подробно и точно"
    )
    return SUMMARY

async def get_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["summary"] = update.message.text

    await update.message.reply_text("Введите дату потери (ДД.ММ.ГГ или ДД.ММ.ГГГГ):")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    for fmt in ("%d.%m.%y", "%d.%m.%Y"):
        try:
            date_lost = datetime.strptime(text, fmt).date()
            break
        except ValueError:
            date_lost = None

    if not date_lost:
        await update.message.reply_text("Неверный формат даты")
        return DATE

    context.user_data["date_lost"] = date_lost

    await update.message.reply_text("Введите станцию метро, где вы потеряли вещь")
    return STATION

async def get_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # либо сделать строгий выбор, либо добавить проверку
    context.user_data["station"] = update.message.text

    await update.message.reply_text(
        "Где вы оставили вещь?", reply_markup=location_keyboard
    )

    return LOCATION

async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["location"] = query.data

    await query.edit_message_text("Ищу совпадения...")

    result = await find_item(
        date_lost=context.user_data["date_lost"],
        station=context.user_data["station"],
        summary=context.user_data["summary"],
        location=context.user_data["location"],
    )

    if result:
        await query.message.reply_text(
            "Ваша вещь найдена! Обратитесь за ней по адресу: ..."
        )
        print(result)
    else:
        await query.message.reply_text(
            "К сожалению, ваша вещь отсутствует среди найденных в метро."
        )

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

        LOCATION: [
            CallbackQueryHandler(get_location)
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