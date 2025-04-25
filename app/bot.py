import asyncio
from aiogram import Bot, Dispatcher
from handlers import register
from aiogram.fsm.storage.memory import MemoryStorage
import logging
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
ADMIN_ID_FIRST = int(os.getenv("ADMIN_ID_FIRST"))
ADMIN_ID_SECOND = int(os.getenv("ADMIN_ID_SECOND"))


async def main():
    bot = Bot(token=API_KEY)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(register.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())