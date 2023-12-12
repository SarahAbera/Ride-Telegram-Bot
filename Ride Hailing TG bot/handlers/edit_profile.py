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

class Edit(StatesGroup):
    Waiting_choice = State()
    userName = State()
    phoneNo = State()
    role = State()

edit_router = Router()

@edit_router.message(Command("edit_profile"))
async def edit_cmd_handler(message:Message, state: FSMContext):
    user_id = message.from_user.id
    current_user = db.get_user(userId=user_id)
    user_name = current_user[1]
    user_phone = current_user[2]
    user_role = current_user[3]
    
    await state.set_state(Edit.Waiting_choice)
    ans = f"Your current name = {user_name} \n current phone_no= {user_phone} \n current role = {user_role}"
    await message.answer(ans,
                            reply_markup= InlineKeyboardMarkup(
                                inline_keyboard= [
                                    [
                                        InlineKeyboardButton(text="Edit Name", callback_data="edit_name"),
                                        InlineKeyboardButton(text="Edit PhoneNo", callback_data="edit_phone"),
                                        InlineKeyboardButton(text="Edit Role", callback_data="edit_role")
                                    ]
                                ]
                            ),
                            resize_keyboard = True
                        )

@edit_router.callback_query(Edit.Waiting_choice)
async def edit_waiting_handler(callback_query: types.CallbackQuery, state:FSMContext):
    choice = callback_query.data
    if choice == "edit_name":
        await state.set_state(Edit.userName)
        await callback_query.message.answer("Enter your new name")

    elif choice == "edit_phone":
        await state.set_state(Edit.phoneNo)
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Share Contact', request_contact=True),
                ]
            ],
            resize_keyboard=True,
        )
        await callback_query.message.answer("Enter your new phone number.", reply_markup= reply_markup)

    elif choice == "edit_role":
        await state.set_state(Edit.role)
        reply_markup = ReplyKeyboardMarkup(
            keyboard= [
                [
                    KeyboardButton(text="PASSENGER"),
                    KeyboardButton(text="DRIVER")
                ]
            ],
            resize_keyboard= True,
        )
        await callback_query.message.answer("Select your new role", reply_markup=reply_markup)
        
    else:
        await callback_query.message.answer("Select the right option to edit your profile.")

@edit_router.message(Edit.userName)
async def edit_name_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = db.get_user(userId=user_id)
    new_name = message.text
    db.update_user_profile(user_id,new_name,user[2],user[3])
    await message.reply("Your name is changed")

@edit_router.message(Edit.phoneNo)
async def edit_phone_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = db.get_user(userId=user_id)
    updated_phone = message.contact.phone_number
    print("updated_phone", updated_phone)
    db.update_user_profile(user_id,user[1],updated_phone,user[3])
    await message.reply("Phone number is updated")

@edit_router.message(Edit.role)
async def edit_role_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = db.get_user(userId=user_id)
    updated_role = message.text
    db.update_user_profile(user_id,user[1],user[2], updated_role)
    await message.reply("Your role is changed")

