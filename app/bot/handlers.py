import os

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot import utils
from bot.create_bot import bot
from bot.keyboards import start_keyboard
from logger import logger






async def start(message: Message):
    username = message.from_user.full_name
    logger.info(f'{username} executed "/start" command)')
    await message.answer(f"Привет, {username}!\nЧто будем делать?",
                         reply_markup=start_keyboard)


async def mainmenu(message: Message, state: FSMContext):
    username = message.from_user.full_name
    logger.info(f'{username} executed "/mainmenu" command)')

    if await state.get_state():
        await state.finish()
        await message.answer("Чем займёмся?", reply_markup=start_keyboard)
    else:
        await message.answer("Уже тут)")


async def unexpected_message(message: Message):
    username = message.from_user.full_name
    logger.info(f'{username} write to the bot without choosing the option)')
    await message.answer("Мая твая ни панима")


async def wrong_content_type(message: Message):
    username = message.from_user.full_name
    logger.info(f'{username} sended not a text message)')
    await message.answer("Пожалуста введите текст")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, utils.chat_is_private,
                                commands="start", state=None)
    dp.register_message_handler(mainmenu, utils.chat_is_private,
                                commands="mainmenu", state='*')


def register_wrong_handlers(dp: Dispatcher):
    dp.register_message_handler(unexpected_message, utils.chat_is_private,
                                content_types='any', state=None)
    dp.register_message_handler(wrong_content_type, utils.chat_is_private,
                                content_types='any', state='*')
