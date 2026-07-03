from telegram import KeyboardButton, ReplyKeyboardMarkup

menu_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Подать новую заявку")]
    ],
    resize_keyboard=True
)

location_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("В вагоне")],
        [KeyboardButton("На станции")],
        [KeyboardButton("Не помню")]
    ],
    resize_keyboard=True
)