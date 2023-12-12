from random import randint
from aiogram.filters import CommandStart,Command
from aiogram import F, Router, html, types
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from database import db
import pymysql
from bot_instance import bot
from handlers.register_user import LoginState
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

class Order(StatesGroup):
    current_location = State()
    destination = State()
    Accept = State()
    AddToHistory = State()

ride_router = Router()

@ride_router.message(Command("order_ride"))
async def handle_ride_order(message: Message, state: FSMContext):
        user_id = message.from_user.id
        user = db.get_user(userId=user_id)
        role = user[3]
        if role.lower() == "passenger":
            await state.set_state(Order.current_location)
            example = "e.g: Semit"
            rep = f"Enter your current location 😉 \n {html.bold(example)}"
            await message.answer(rep)
        else:
             await message.answer("This command is allowed only for PASSENGERS")

@ride_router.message(Order.current_location)
async def handle_order_ride(message:Message, state:FSMContext):
    await state.update_data(currentLocation = message.text)
    await state.set_state(Order.destination)
    await message.answer("Enter your destination")

@ride_router.message(Order.destination)
async def destination_handler(message:Message, state:FSMContext):
    await state.update_data(destination = message.text)
    results = db.get_drivers()
    passenger_id = message.from_user.id
    passenger = db.get_user(passenger_id)

    data = await state.get_data()
    start = data["currentLocation"]
    destination = message.text
    price = randint(150,350)
    await state.update_data(price = price)

    db.insert_into_ride_request(passenger_id, start, destination, price)
    for driver in results:
        driver_id = driver[0]
        answer = f"New ride request from {passenger}"
        await bot.send_message(driver_id, answer,
                               reply_markup=InlineKeyboardMarkup(
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="Show Ongoing Requests", callback_data= "ongoing requests"),
                                    ]
                                ],
                                resize_keyboard=True,
                            )
                        )
    await state.set_state(Order.AddToHistory)

@ride_router.message(Order.AddToHistory)
async def add_accepted_ride_request_handler(message: Message, state: FSMContext):
    id = message.from_user.id
    data = state.get_data()
    start = data["currentLocation"]
    destination = data["destination"]
    price = data["price"]
    date = datetime.now()
    current_date = date.strftime("%d %A %B %Y")
    print(current_date)
    db.insert_into_history_table(id, start, destination, price, current_date)


@ride_router.callback_query(LoginState)
async def handle_callback(callback_query: types.CallbackQuery, state: FSMContext):
    callback_data = callback_query.data
    if callback_data == "ongoing requests":
        await state.set_state(Order.Accept)
        requests = db.get_all_ride_requests()
        lst = []
        keyboard = []
        for idx, request in enumerate(requests):
            start = request[1]
            dest = request[2]
            price = request[3]
            passenger_id = request[0]
            answer = str(idx+1) + ", From" + start + " to " + dest + f" with a price of {price}"
            lst.append(answer)
            keyboard.append(InlineKeyboardButton(text= str(idx + 1), callback_data=str(passenger_id)))
        
        reply_text = "\n".join(lst)
        await callback_query.message.answer(reply_text,reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[keyboard]
            )
        )
    else:
         await callback_query.message.answer("Tab 'Show ongoing requests' button")

@ride_router.callback_query(Order.Accept)
async def handle_accept_ride(callback_query: types.CallbackQuery, state: FSMContext):
     callback_data = callback_query.data
     driver_id = callback_query.from_user.id
     driver = db.get_user(driver_id)
     user_id = int(callback_data)
     db.remove_ride_request(user_id)
     reply = f"Ride request is Accepted \n Driver {driver[1]} is on the way"
     await bot.send_message(user_id, reply)
     