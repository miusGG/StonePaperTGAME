import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.types import CallbackQuery

from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.filters import MagicData

from config import cfg

# Bot token can be obtained via https://t.me/BotFather
TOKEN = cfg["TOKEN"]

# All handlers should be attached to the Router (or Dispatcher)

maintenance_router = Router()
maintenance_router.message.filter(MagicData(F.maintenance_mode.is_(True)))
maintenance_router.callback_query.filter(MagicData(F.maintenance_mode.is_(True)))

router = Router()

dp = Dispatcher()
#dp.include_routers(router)

allCards_bt = KeyboardButton(text='ВСЕ МОИ КАРТЫ')
startGame_bt = KeyboardButton(text='Начать игру')
stats_bt = KeyboardButton(text='Моя статистика')
main_kb_buttons = [
    [allCards_bt],
    [startGame_bt],
    [stats_bt]
]
main_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=main_kb_buttons)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! Этот игровой бот сыграет с тобой с "
                         f"усложненную версию игры - камень, ножницы, бумага. Так же вам будет представлен полностью "
                         f"новые ключевые предметы для игры. И со временем Вам откроются новые, надо лишь играть!)",
                         reply_markup=main_kb)


@dp.message(F.text == "ВСЕ МОИ КАРТЫ")
async def callback_query_handler(callback: CallbackQuery):
    await callback.answer("Ваши карты!)")
    await callback.message.answer("CARDS")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot, dispatcher=dp)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
