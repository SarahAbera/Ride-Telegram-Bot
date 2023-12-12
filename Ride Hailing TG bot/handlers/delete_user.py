from random import randint
from aiogram.filters import CommandStart,Command
from aiogram import F, Router, html, types
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from database import db
import pymysql
from bot_instance import bot
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
delete_router = Router()
Delete_state = State()

@delete_router.message(Command("delete_account"))
async def handle_delete_user(message: Message, state: FSMContext):
    await state.set_state(Delete_state)
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Yes"),
                KeyboardButton(text="No")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Are you sure? \n Do you want to delete your account?", reply_markup=reply_markup)

@delete_router.message(Delete_state)
async def delete_account(message:Message, state: FSMContext):
    user_id = message.from_user.id
    response = message.text.lower()
    if response == "yes":
        db.delete_user(user_id)
        await message.answer("Account deleted successfully!\n Use '/start' command for registration.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Account deletion Cancelled", reply_markup=ReplyKeyboardRemove())
