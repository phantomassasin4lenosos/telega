import asyncio
import decimal
import sqlite3 as sq
import random

from decimal import Decimal
from database import db, cur, register, block, balance
from config import access_token, reg_text, help_text, bet_text, nav_text
from aiogram.types import Message
from aiogram import Bot, Dispatcher, F
from keyboard import main_keyboard, games_keyboard, coinflip_keyboard

bot = Bot(token=access_token)
dp = Dispatcher()


@dp.message(F.text == "/start")
async def sender(message: Message):
    try:
        cur.execute(f"INSERT INTO users (user_id) VALUES ({message.from_user.id})")
        await message.answer(reg_text, reply_markup=main_keyboard)

    except sq.IntegrityError:
        await message.answer("Главное меню:", reply_markup=main_keyboard)

    cur.execute(f"UPDATE users SET block = 'main' WHERE user_id == {message.from_user.id}")
    db.commit()


@dp.message(F.text == "/help")
async def sender(message: Message):
    if register(message.from_user.id):
        await message.answer(help_text)


@dp.message(F.text == "/balance")
@dp.message(F.text == "Баланс 💰")
async def sender(message: Message):
    if register(message.from_user.id):
        await message.answer(f"Ваш баланс: {balance(message.from_user.id)}₽")


@dp.message(F.text == "Назад")
async def sender(message: Message):
    if register(message.from_user.id):
        if block(message.from_user.id) == "games":
            cur.execute(f"UPDATE users SET block = 'main' WHERE user_id == {message.from_user.id}")
            await message.answer("Главное меню:", reply_markup=main_keyboard)

        elif block(message.from_user.id) in ["coinflip", "cf_bet1", "cf_bet2"]:
            cur.execute(f"UPDATE users SET block = 'games' WHERE user_id == {message.from_user.id}")
            await message.answer("Выберите игру: ", reply_markup=games_keyboard)
    db.commit()


@dp.message(F.text == "/games")
@dp.message(F.text == "Выбрать игру 🎰")
async def sender(message: Message):
    if register(message.from_user.id):
        cur.execute(f"UPDATE users SET block = 'games' WHERE user_id == {message.from_user.id}")
        await message.answer("Выберите игру: ", reply_markup=games_keyboard)
    db.commit()


@dp.message(F.text == "/coinflip")
@dp.message(F.text == "CoinFlip 🪙")
async def sender(message: Message):
    if register(message.from_user.id):
        cur.execute(f"UPDATE users SET block = 'coinflip' WHERE user_id == {message.from_user.id}")
        await message.answer("Орел / Решка:", reply_markup=coinflip_keyboard)
    db.commit()


@dp.message(F.text == "Орел")
@dp.message(F.text == "Решка")
async def sender(message: Message):
    if register(message.from_user.id):
        if block(message.from_user.id) in ["coinflip", "cf_bet1", "cf_bet2"]:
            if message.text == "Орел":
                cur.execute(f"UPDATE users SET block = 'cf_bet1' WHERE user_id == {message.from_user.id}")

            elif message.text == "Решка":
                cur.execute(f"UPDATE users SET block = 'cf_bet2' WHERE user_id == {message.from_user.id}")

            await message.answer(bet_text(message.text, message.from_user.id))

        else:
            await message.answer(nav_text)
    db.commit()


@dp.message(F.text)
async def sender(message: Message):
    if register(message.from_user.id):
        if block(message.from_user.id) in ["cf_bet1", "cf_bet2"]:

            try:
                bet = Decimal(message.text).quantize(Decimal("1.00"))
                cf_result = random.randint(1, 2)

                if bet < Decimal("0.01"):
                    await message.answer("Минимальная сумма ставки: 0.01₽")

                elif bet > balance(message.from_user.id):
                    await message.answer(f"Недостаточно средств. Ваш баланс: {balance(message.from_user.id)}₽")

                else:
                    if cf_result == 1:
                        if block(message.from_user.id) == "cf_bet1":
                            cur.execute(f"UPDATE users SET balance = {balance(message.from_user.id) + bet} WHERE user_id == {message.from_user.id}")

                        elif block(message.from_user.id) == "cf_bet2":
                            cur.execute(f"UPDATE users SET balance = {balance(message.from_user.id) - bet} WHERE user_id == {message.from_user.id}")

                        await message.answer(f"Орел. Ваш баланс: {balance(message.from_user.id)}₽")
                    elif cf_result == 2:
                        if block(message.from_user.id) == "cf_bet1":
                            cur.execute(f"UPDATE users SET balance = {balance(message.from_user.id) - bet} WHERE user_id == {message.from_user.id}")

                        elif block(message.from_user.id) == "cf_bet2":
                            cur.execute(f"UPDATE users SET balance = {balance(message.from_user.id) + bet} WHERE user_id == {message.from_user.id}")

                        await message.answer(f"Решка. Ваш баланс: {balance(message.from_user.id)}₽")
            except decimal.InvalidOperation:
                await message.answer("Некорректная сумма ставки")
        else:
            await message.answer(nav_text)
    db.commit()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
