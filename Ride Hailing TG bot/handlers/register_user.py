import logging
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
)


class SignupStates(StatesGroup):
    SIGNUP_FULL_NAME = State()
    SIGNUP_PHONE_NUMBER = State()
    SIGNUP_ROLE = State()

class User(StatesGroup):
    Edit_Profile = State()
    Show_History = State()
    Delete = State()

LoginState = State()

user_router = Router()

@user_router.message(Command(""))

@user_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
 
    user_id = message.from_user.id
    result = db.check_user_exists(user_id)

    if result[0] == 0:
        await state.set_state(SignupStates.SIGNUP_FULL_NAME)
        await message.reply("Welcome! Please sign up to continue. Send me your full name.")

    else:
        user_id = message.from_user.id
        result = db.get_user(userId=user_id)
        full_name = result[1]
        cmd = "See available commands on the command section"
        ans = f"Welcome back {html.bold(full_name)}\n {html.italic(cmd)}"
        await state.set_state(LoginState)
        await message.reply(ans, reply_markup=ReplyKeyboardRemove())

@user_router.message(Command("cancel"))
async def handle_cmd_cancel(message:Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return await message.answer(
            "Already Cancelled.",
            reply_markup=ReplyKeyboardRemove(),
        )

        logging.info("Cancelling state %r", current_state)
        await state.clear()
        await message.answer(
            "Cancelled.",
            reply_markup=ReplyKeyboardRemove(),
        )

@user_router.message(SignupStates.SIGNUP_FULL_NAME)
async def handle_full_name(message:Message, state: FSMContext):

    await state.update_data(full_name=message.text)
    reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Share Contact', request_contact=True),
                ],
            ],
            resize_keyboard=True,
        )

    await message.reply("Please share your phone number using the 'Share Contact' button.",
                         reply_markup=reply_markup)

    await state.get_state() == SignupStates.SIGNUP_FULL_NAME
    await state.set_state(SignupStates.SIGNUP_PHONE_NUMBER)

@user_router.message(SignupStates.SIGNUP_PHONE_NUMBER)
async def handle_phone_number(message: types.Message, state: FSMContext):
    # Store the phone number in the user's state
    print("phone state")
    await state.update_data(phone=message.text)
    await state.set_state(SignupStates.SIGNUP_ROLE)
    await message.answer("choose your role",
            reply_markup = ReplyKeyboardMarkup(
            keyboard= [
                [
                    KeyboardButton(text="PASSENGER"),
                    KeyboardButton(text="DRIVER"),
                ],
            ],
            resize_keyboard= True,
        ),
    )

@user_router.message(SignupStates.SIGNUP_ROLE)
async def passenger_handler(message: Message, state:FSMContext):

    # Determine the role (driver or passenger)
    if F.text.casefold() == "driver":
        role = "driver" 
    else: role = "passenger"

    # Store the user's information in the database
    user_id = message.from_user.id
    data = await state.get_data()
    full_name = data.get('full_name')
    phone = data.get('phone')

    db.insert_into_ride_bot_table(user_id, full_name, phone, role)

    await state.set_state(LoginState)

    # Send a welcome message
    await message.reply(f"Welcome, {full_name}! You have successfully signed up / logged in as a {role}.", reply_markup=ReplyKeyboardRemove())

