import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram import F
from config import cfg, main_keyboard, play_keyboard, cards_check, update_game_stats_loss, update_game_stats, \
    duel_keybord, images_cards
from checkHowWin import check
import random

# Bot token can be obtained via https://t.me/BotFather
TOKEN = cfg["TOKEN"]  # токен для работы бота в телеграмм

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()
all_cards = list(images_cards.keys())  # все карты
temp = "rock"  # временная переменная для хранение нашей карты


@dp.message(CommandStart())  # Команда для /start для бота
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! Этот игровой бот сыграет с тобой с "
                         f"усложненную версию игры - камень, ножницы, бумага. Так же вам будет представлен полностью "
                         f"новые ключевые предметы для игры. И со временем Вам откроются новые, надо лишь играть!)",
                         reply_markup=main_keyboard())


@dp.message(F.text == "Все мои карты")
async def send_all_your_cards(mes: Message, bot: Bot):  # выврд всех имющийхся карт у пользователя
    await mes.answer("Ваши карты:")
    photos = []
    if cards_check["rock"]:
        photoRock = InputMediaPhoto(type='photo', media=FSInputFile(r'icons/rock.jpg'))
        photos.append(photoRock)
    if cards_check["paper"]:
        photoPaper = InputMediaPhoto(type='photo', media=FSInputFile(r'icons/paper.PNG'))
        photos.append(photoPaper)
    if cards_check["scissors"]:
        photoScissors = InputMediaPhoto(type='photo', media=FSInputFile(r'icons/scissors.PNG'))
        photos.append(photoScissors)
    if cards_check["axe"]:
        photoAxe = InputMediaPhoto(type='photo', media=FSInputFile(r'icons/axe.PNG'))
        photos.append(photoAxe)
    if cards_check["picaxe"]:
        photoPicaxe = InputMediaPhoto(type='photo', media=FSInputFile(r'icons/picaxe.PNG'))
        photos.append(photoPicaxe)
    await bot.send_media_group(mes.chat.id, photos)  # сделать систему этих карточек и отправить


@dp.message(F.text == "Начать игру")
async def send_all_your_cards(mes: Message, bot: Bot):  # команда для начала дуэли
    await mes.answer("Игра началась...")
    await mes.answer("Выберите свою карту:", reply_markup=play_keyboard())


@dp.message(F.text == 'Моя статистика')
async def send_all_your_cards(mes: Message, bot: Bot):  # команда для общей статистики 1 игрока
    with open("stats.txt", "r") as f:
        games, wins, losses = map(int, f.readline().split())
    await mes.answer(f"Победы: {wins}\nПоражения:{losses}\nВсего игр:{games}")


# далее идут команды для выбора карты во время дуэли
@dp.callback_query(F.data == "rock")
async def rock_callback(callback: CallbackQuery, bot: Bot):
    await callback.answer("Вы выбрали КАМЕНЬ!")
    await callback.message.answer("КАМЕНЬ", reply_markup=duel_keybord())  # добавление клавиатуры
    photoRock = InputMediaPhoto(type='photo', media=FSInputFile(r'icons/rock.jpg'))  # вывод карты картинки
    photos = [photoRock]
    await bot.send_media_group(callback.message.chat.id, photos)
    global temp
    temp = "rock"  # запись карты в переменную         Далее все аналогично:


@dp.callback_query(F.data == "paper")
async def rock_callback(callback: CallbackQuery, bot: Bot):
    await callback.answer("Вы выбрали БУМАГУ!")
    await callback.message.answer("БУМАГА", reply_markup=duel_keybord())
    photo = InputMediaPhoto(type='photo', media=FSInputFile(r'icons/paper.PNG'))
    photos = [photo]
    await bot.send_media_group(callback.message.chat.id, photos)
    global temp
    temp = "paper"


@dp.callback_query(F.data == "scissors")
async def rock_callback(callback: CallbackQuery, bot: Bot):
    await callback.answer("Вы выбрали НОЖНИЦЫ!")
    await callback.message.answer("НОЖНИЦЫ", reply_markup=duel_keybord())
    photo = InputMediaPhoto(type='photo', media=FSInputFile(r'icons/scissors.PNG'))
    photos = [photo]
    await bot.send_media_group(callback.message.chat.id, photos)
    global temp
    temp = "scissors"


@dp.callback_query(F.data == "axe")
async def rock_callback(callback: CallbackQuery, bot: Bot):
    await callback.answer("Вы выбрали ТОПОР!")
    await callback.message.answer("ТОПОР", reply_markup=duel_keybord())
    photo = InputMediaPhoto(type='photo', media=FSInputFile(r'icons/axe.PNG'))
    photos = [photo]
    await bot.send_media_group(callback.message.chat.id, photos)
    global temp
    temp = "axe"


@dp.callback_query(F.data == "picaxe")
async def rock_callback(callback: CallbackQuery, bot: Bot):
    await callback.answer("Вы выбрали КИРКУ!")
    await callback.message.answer("КИРКА", reply_markup=duel_keybord())
    photo = InputMediaPhoto(type='photo', media=FSInputFile(r'icons/picaxe.PNG'))
    photos = [photo]
    await bot.send_media_group(callback.message.chat.id, photos)
    global temp
    temp = "picaxe"


@dp.callback_query(F.data == "duel")
async def duel(callback: CallbackQuery, bot: Bot):
    temp_cards = all_cards
    temp_cards.remove(temp)  # создаю массив без карты которую выбрал игрок
    print("Ряд карт на рассмотрение для врага", temp_cards)
    en_card = random.choice(temp_cards)  # выбор карты для врага
    await callback.message.answer("Карта врага!")
    photo = InputMediaPhoto(type='photo', media=FSInputFile(rf"{images_cards[en_card]}"))
    photos = [photo]
    await bot.send_media_group(callback.message.chat.id, photos) # вывод карты врага
    if check(temp, en_card):  # отпределение победителя или проигравшего:
        await callback.message.answer("ВЫ ПОБЕДИЛИ!!!")
        update_game_stats()  # обновление статистики
    elif not check(temp, en_card):
        await callback.message.answer("ВЫ ПРОИГРАЛИ.")
        update_game_stats_loss()   # обновление статистики
    else:  # если что то пойдет не так будет выведена ошибка
        print("Неизвестная ошибка")
        await callback.message.answer("Неизвестная ошибка... Попробуйте еще раз")


async def main() -> None:  # функция для запуска бота
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot, dispatcher=dp)


if __name__ == "__main__":  # его запуск
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
