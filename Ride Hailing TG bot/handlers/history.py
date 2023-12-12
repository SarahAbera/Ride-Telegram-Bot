from aiogram.filters import CommandStart,Command
from aiogram import F, Router, html, types
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from database import db


history_router = Router()

@history_router.message(Command("show_history"))
async def history_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = db.get_user(userId=user_id)
    print("History command", user[3].lower())
    if user[3].lower() == "passenger":
        ride_history = db.get_history(user_id)

        lst = []
        for idx, history in enumerate(ride_history):
            start = history[1]
            dest = history[2]
            price = history[3]
            date = history[4]
            answer = str(idx+1) + ", From" + start + " to " + dest + f" with a price of {price}\nOn date {date}"
            lst.append(answer)
        
        reply_text = "\n\n".join(lst)
        ans = f"Your accepted ride request history is...\n {reply_text}"
        await message.answer(ans)

    else:
        await message.reply("This feature is allowed for Passengers")
