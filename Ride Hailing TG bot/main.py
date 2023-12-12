import asyncio
from aiogram import Dispatcher, Router
from bot_instance import bot
from handlers.register_user import user_router
from handlers.edit_profile import edit_router
from handlers.order_ride import ride_router
from handlers.delete_user import delete_router
from handlers.history import history_router


def register_router(dp: Dispatcher):
    dp.include_router(user_router)
    dp.include_router(edit_router)
    dp.include_router(ride_router)
    dp.include_router(history_router)
    dp.include_router(delete_router)

async def main():
    """ Main entry point """
    dp = Dispatcher()
    register_router(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())