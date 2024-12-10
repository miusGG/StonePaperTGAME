#  общий конфиг куда можно добавить какую либо информацию о бота, сейчас там токен
cfg = {
    "TOKEN": "7921775209:AAHSjWnM5_9cigxHu9TrRJqIXMQnibuwfos"
}

#  словарь для понимания какие карты есть у пользователя
cards_check = {
    "rock": True,
    "paper": True,
    "scissors": True,
    "axe": True,
    "picaxe": True
}

#  изображение для каждой карты
images_cards = {
    "rock": "icons/rock.jpg",
    "paper": "icons/paper.PNG",
    "scissors": "icons/scissors.PNG",
    "axe": "icons/axe.PNG",
    "picaxe": "icons/picaxe.PNG"
}

# далее идут доп функции для бота и клавиатуры
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


# клавиатруы:
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
        callback_data="rock"),
    )
    builder.add(types.InlineKeyboardButton(
        text="Scissors",
        callback_data="scissors")
    )
    builder.add(types.InlineKeyboardButton(
        text="Paper",
        callback_data="paper")
    )
    builder.add(types.InlineKeyboardButton(
        text="Axe",
        callback_data="axe")
    )
    builder.add(types.InlineKeyboardButton(
        text="Picaxe",
        callback_data="picaxe")
    )
    return builder.as_markup()


def duel_keybord():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="СЫГРАТЬ ЭТОЙ КАРТОЙ!",
        callback_data="duel"),
    )
    return builder.as_markup()


# функции для обновления побед порожений и игр
def update_game_stats(filepath="stats.txt"):
    """
    Читает статистику игр из файла, обновляет ее после победы и записывает обратно.
    """
    try:
        with open(filepath, "r") as f:
            games, wins, losses = map(int, f.readline().split())
    except FileNotFoundError:
        games, wins, losses = 0, 0, 0
        print("Файл со статистикой не найден. Создан новый файл.")

    games += 1
    wins += 1

    with open(filepath, "w") as f:
        f.write(f"{games} {wins} {losses}")

    print(f"Статистика обновлена: Игры - {games}, Победы - {wins}, Поражения - {losses}")


def update_game_stats_loss(filepath="stats.txt"):
    """
    Читает статистику игр из файла, обновляет ее после поражения и записывает обратно.
    """
    try:
        with open(filepath, "r") as f:
            games, wins, losses = map(int, f.readline().split())
    except FileNotFoundError:
        games, wins, losses = 0, 0, 0
        print("Файл со статистикой не найден. Создан новый файл.")

    games += 1
    losses += 1

    with open(filepath, "w") as f:
        f.write(f"{games} {wins} {losses}")

    print(f"Статистика обновлена: Игры - {games}, Победы - {wins}, Поражения - {losses}")
