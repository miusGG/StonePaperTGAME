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

from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile

from aiogram import Router, F
from aiogram.methods.delete_message import DeleteMessage
from aiogram.filters import Command
from aiogram.filters import MagicData

from config import cfg, main_keyboard, play_keyboard, cards_check

# Bot token can be obtained via https://t.me/BotFather
TOKEN = cfg["TOKEN"]

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()




@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! Этот игровой бот сыграет с тобой с "
                         f"усложненную версию игры - камень, ножницы, бумага. Так же вам будет представлен полностью "
                         f"новые ключевые предметы для игры. И со временем Вам откроются новые, надо лишь играть!)",
                         reply_markup=main_keyboard())


@dp.message(F.text == "Все мои карты")
async def send_all_your_cards(mes: Message, bot: Bot):
    await mes.answer("Ваши карты:")
    photo1 = InputMediaPhoto(type='photo', media=FSInputFile(r'icons/rock.jpg'))
    photos = [photo1]
    await bot.send_media_group(mes.chat.id, photos) #сделать систему этих карточек

@dp.message(F.text == "Начать игру")
async def send_all_your_cards(mes: Message, bot: Bot):
    await mes.answer("Игра началась...")
    await mes.answer("Выберите свою карту", reply_markup=play_keyboard())


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot, dispatcher=dp)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
