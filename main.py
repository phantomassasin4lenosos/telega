import asyncio
import sqlite3 as sq
import decimal

from random import randint
from database import db, cur, register, balance, block
from config import access_token
from aiogram.types import Message
from aiogram import Bot, Dispatcher, F
from keyboard import main_keyboard, games_keyboard, coinflip_keyboard

bot = Bot(token=access_token)
dp = Dispatcher()


@dp.message(F.text == "/start")
async def sender(message: Message):
    try:
        cur.execute(f"INSERT INTO users (user_id) VALUES ({message.from_user.id})")
        await message.answer("""✅ Вы успешно зарегистрировались!

Почему именно AMG4GAMES?

- Моментальный бонус за регистрацию 50₽
- Быстрые выплаты
- Высокий процент выйгрыша
- Полная анонимность для всех игроков
- Разнообразие игровых режимов

Список команд быстрого доступа - /help""", reply_markup=main_keyboard)
    except sq.IntegrityError:
        await message.answer("Главное меню:", reply_markup=main_keyboard)
    db.commit()


@dp.message(F.text == "/games")
@dp.message(F.text == "Выбрать игру 🎰")
async def sender(message: Message):
    if register(message.from_user.id):
        cur.execute("UPDATE users SET block = 'games'")
        await message.answer("Выберите игру: ", reply_markup=games_keyboard)
    db.commit()


@dp.message(F.text == "Назад")
async def sender(message: Message):
    if register(message.from_user.id):
        if block(message.from_user.id) == "games":
            cur.execute("UPDATE users SET block = 'main'")
            await message.answer("Главное меню:", reply_markup=main_keyboard)

        elif block(message.from_user.id) in ["coinflip", "cf_bet1", "cf_bet2"]:
            cur.execute("UPDATE users SET block = 'games'")
            await message.answer("Выберите игру: ", reply_markup=games_keyboard)
    db.commit()


@dp.message(F.text == "/coinflip")
@dp.message(F.text == "CoinFlip 🪙")
async def sender(message: Message):
    if register(message.from_user.id):
        cur.execute("UPDATE users SET block = 'coinflip'")
        await message.answer("Орел / Решка:", reply_markup=coinflip_keyboard)
    db.commit()


@dp.message(F.text == "/balance")
@dp.message(F.text == "Баланс 💰")
async def sender(message: Message):
    if register(message.from_user.id):
        await message.answer(f"Ваш баланс: {balance(message.from_user.id)}₽")


@dp.message(F.text == "Орел")
@dp.message(F.text == "Решка")
async def sender(message: Message):
    if register(message.from_user.id):
        if block(message.from_user.id) in ["coinflip", "cf_bet1", "cf_bet2"]:
            if message.text == "Орел":
                cur.execute("UPDATE users SET block = 'cf_bet1'")

            elif message.text == "Решка":
                cur.execute("UPDATE users SET block = 'cf_bet2'")

            await message.answer(f"""Ваш баланс: {balance(message.from_user.id)}₽
Ставка: {message.text}

Сделайте ставку:""")
        else:
            await message.answer("""Пожалуйста используйте /help для навигации

Или нажмите /start чтобы вернуться в главное меню""")
    db.commit()


@dp.message(F.text)
async def sender(message: Message):
    try:
        if register(message.from_user.id):
            if block(message.from_user.id) in ["cf_bet1", "cf_bet2"]:
                bet = decimal.Decimal(message.text).quantize(decimal.Decimal("1.00"))
                rand = randint(1, 2)
                if bet < decimal.Decimal("0.01"):
                    await message.answer("Минимальная сумма ставки: 0.01₽")

                elif bet <= balance(message.from_user.id):
                    if rand == 1:
                        if block(message.from_user.id) == "cf_bet1":
                            cur.execute(f"UPDATE users SET balance = {balance(message.from_user.id) + bet}")
                            await message.answer(f"Орел, Вы выйграли Ваш баланс: {balance(message.from_user.id)}₽")
                        elif block(message.from_user.id) == "cf_bet2":
                            cur.execute(f"UPDATE users SET balance = {balance(message.from_user.id) - bet}")
                            await message.answer(f"Орел, Вы проиграли Ваш баланс: {balance(message.from_user.id)}₽")

                    elif rand == 2:
                        if block(message.from_user.id) == "cf_bet1":
                            cur.execute(f"UPDATE users SET balance = {balance(message.from_user.id) - bet}")
                            await message.answer(f"Решка, Вы проиграли Ваш баланс: {balance(message.from_user.id)}₽")
                        elif block(message.from_user.id) == "cf_bet2":
                            cur.execute(f"UPDATE users SET balance = {balance(message.from_user.id) + bet}")
                            await message.answer(f"Решка, Вы выйграли Ваш баланс: {balance(message.from_user.id)}₽")
                    db.commit()
                else:
                    await message.answer("Недостаточно средств")
            else:
                await message.answer("""Пожалуйста используйте /help для навигации

Или нажмите /start чтобы вернуться в главное меню""")
    except decimal.InvalidOperation:
        await message.answer("Некорректная сумма")


@dp.message(F.text == "/help")
async def sender(message: Message):
    if register(message.from_user.id):
        await message.answer("""Команды быстрого доступа:
        
/start - Главное меню
/balance - Баланс
/games - Выбрать игру
/coinflip - CoinFlip
/dice - Dice""")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
