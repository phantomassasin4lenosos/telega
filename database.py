from decimal import Decimal
import sqlite3 as sq

db = sq.connect("telegram.db")
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    block TEXT DEFAULT 'main',
    balance INTEGER DEFAULT 50
)""")


def balance(user_id):
    return Decimal(cur.execute(f"SELECT balance FROM users WHERE user_id == {user_id}").fetchone()[0]).quantize(
        Decimal("1.00"))


def register(user_id):
    return cur.execute(f"SELECT user_id FROM users WHERE user_id == {user_id}").fetchone()


def block(user_id):
    return cur.execute(f"SELECT block FROM users WHERE user_id == {user_id}").fetchone()[0]
