import asyncio
from aiogram import Bot, Dispatcher
from handlers import register
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "ТВОЙ_ТОКЕН_ТУТ"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(register.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
