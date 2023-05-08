import asyncio
from aiogram import types, Bot, Dispatcher
from aiogram.filters.command import Command
import os
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import Session

from models import Base, User

tg_bot = Bot(token=os.getenv('BOT_DEV_TOKEN'))
dp = Dispatcher()

engine = create_engine(f"postgresql+psycopg2://admin:admin@{os.getenv('DB_URL')}/{os.getenv('DB_NAME')}", pool_pre_ping=True)
engine.dispose(close=False)
Base.metadata.create_all(bind=engine)

@dp.message(Command('start'))
async def start(message: types.Message):
    with Session(bind=engine) as db:
        tg_id = db.query(User).filter(User.tg_id == message.from_user.id).one_or_none()
        if tg_id:
            await message.answer('You are already exists! Just wait! P.S. Vse chto ya sdelal - libo raboet libo rabotaet no ne tak kak ti ozhidaesh. by DanyaTHEdeveloper')
        else:
            new_user = User(tg_id=message.from_user.id, tg_username=message.from_user.username)
            db.add(new_user)
            db.commit()
            await message.answer('Hi, within time you will get push-ups with legit items "STEAM-BUFF or BUFF-STEAM. See you later!"')

            
async def main():
    await dp.start_polling(tg_bot)

if __name__ == '__main__':
    asyncio.run(main())