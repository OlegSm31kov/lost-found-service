from telegram import KeyboardButton, ReplyKeyboardMarkup

menu_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Подать новую заявку")]
    ],
    resize_keyboard=True
)