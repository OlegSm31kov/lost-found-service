from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

menu_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("Подать новую заявку")]],
    resize_keyboard=True
)

conversation_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("Отмена")]],
    resize_keyboard=True
)

location_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("В вагоне", callback_data="В вагоне")],
        [InlineKeyboardButton("На станции", callback_data="На станции")],
        [InlineKeyboardButton("Не помню", callback_data="Не помню")],
    ]
)