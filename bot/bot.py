"""Минимальный бот для прототипа FairPari Mini App (aiogram 3)."""
import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandObject, CommandStart

BOT_TOKEN = os.environ["BOT_TOKEN"]
APP_URL = os.environ["APP_URL"].rstrip("/") + "/"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(msg: types.Message, command: CommandObject) -> None:
    ref = command.args or "ref_339"  # t.me/<бот>?start=ref_339
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="▶ Открыть FairPari", web_app=types.WebAppInfo(url=f"{APP_URL}?ref={ref}"))
    ]])
    await msg.answer("Ставки на спорт и казино FairPari прямо в Telegram.", reply_markup=kb)


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
