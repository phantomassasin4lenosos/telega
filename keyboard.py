from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu = [
    [KeyboardButton(text="Выбрать игру 🎰")],
    [KeyboardButton(text="Баланс 💰")],
    [KeyboardButton(text="Пополнить 💵"), KeyboardButton(text="Вывести 💸")]
]

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=menu,
    resize_keyboard=True
)

games = [
    [KeyboardButton(text="CoinFlip 🪙"), KeyboardButton(text="Dice 🎲")],
    [KeyboardButton(text="Назад")]
]

games_keyboard = ReplyKeyboardMarkup(
    keyboard=games,
    resize_keyboard=True
)


coinflip = [
    [KeyboardButton(text="Орел"), KeyboardButton(text="Решка")],
    [KeyboardButton(text="Назад")]
]

coinflip_keyboard = ReplyKeyboardMarkup(
    keyboard=coinflip,
    resize_keyboard=True
)
