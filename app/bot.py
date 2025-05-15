import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import os
from handlers import register, profile, match, admin
from dotenv import load_dotenv
from database.db import init_db

load_dotenv()

API_KEY = os.getenv("API_KEY")
ADMIN_ID_FIRST = int(os.getenv("ADMIN_ID_FIRST"))
ADMIN_ID_SECOND = int(os.getenv("ADMIN_ID_SECOND"))


async def main():
    init_db()
    bot = Bot(token=API_KEY)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(register.router)
    dp.include_router(profile.router)
    dp.include_router(match.router)
    dp.include_router(admin.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())