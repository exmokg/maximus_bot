import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, LOG_FILE
from handlers.broadcast import broadcast_router
from handlers.report import report_router

def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

async def main():
    setup_logging()
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(broadcast_router)
    dp.include_router(report_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())