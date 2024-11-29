cfg = {
    "TOKEN": "7921775209:AAHSjWnM5_9cigxHu9TrRJqIXMQnibuwfos"
}
my_cards = {
    "rock": "icons/rock.jpg', 'rb",
    "paper": '',
    "scissors": '',
}

cards_check = {
    "rock": True,
    "paper": True,
    "scissors": True
}

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def main_keyboard():
    allCards_bt = KeyboardButton(text='Все мои карты')
    startGame_bt = KeyboardButton(text='Начать игру')
    stats_bt = KeyboardButton(text='Моя статистика')
    main_kb_buttons = [
        [allCards_bt],
        [startGame_bt],
        [stats_bt]
    ]
    main_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=main_kb_buttons,
                                                       resize_keyboard=True,
                                                       input_field_placeholder="Камень, ножницы, бумага раз....два....ТРИ")
    return main_kb

def play_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Rock",
        callback_data="rock")
    )
    builder.add(types.InlineKeyboardButton(
        text="Scissors",
        callback_data="scissors")
    )
    builder.add(types.InlineKeyboardButton(
        text="Paper",
        callback_data="paper")
    )
    return builder.as_markup()