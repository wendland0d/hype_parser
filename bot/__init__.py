from aiogram import Bot, Dispatcher
import os

tg_bot = Bot(token=os.getenv('BOT_TOKEN_DEV'))
dp = Dispatcher()