import asyncio
from aiogram import types, Bot, Dispatcher
from aiogram.filters.command import Command
import os

tg_bot = Bot(token=os.getenv('BOT_DEV_TOKEN'))
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer('Теперь мы работаем как микро-сервисы. А парсеры запустятся через совсем маленькое время или даже уже запустились! Вы всегда можете написать мне в tg или чекнуть репку на github-e')

async def main():
    await dp.start_polling(tg_bot)

if __name__ == '__main__':
    asyncio.run(main())