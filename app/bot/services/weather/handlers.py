from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards import start_keyboard
from config import WEATHER_SERVICE_NAME
from logger import logger
from . import service
from .states import Weather


async def enter_city_name(callback: CallbackQuery):
    username = callback.from_user.full_name
    logger.info(f'{username} has chosen weather service)')
    await Weather.enter_city.set()
    await callback.message.answer("Введите город")
    await callback.answer()


async def get_weather(message: Message, state: FSMContext):
    username = message.from_user.full_name
    logger.info(f'{username} entered {message.text})')

    if result_message := await service.get_city_weather(message.text):
        logger.info(f'{username}:{message.text} exists\n{result_message}')
        await state.finish()
        await message.answer(result_message)
        await message.answer("Чем займёмся?",
                             reply_markup=start_keyboard)

    else:
        logger.info(f'{username}:{message.text} not exists')
        await message.answer(
            "Такого города не существует.\n"
            "Попробуйте вести название транслитом.\n"
            "Например: Novosibirsk.")


async def back(message: Message, state: FSMContext):
    username = message.from_user.full_name
    logger.info(f'{username} executed "/back" command')

    await state.finish()
    await message.answer("Чем займёмся?", reply_markup=start_keyboard)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(back, commands="back",
                                state=Weather.enter_city)
    dp.register_callback_query_handler(
        enter_city_name, lambda callback: WEATHER_SERVICE_NAME in
                                          callback.data, state=None)
    dp.register_message_handler(get_weather, content_types="text",
                                state=Weather.enter_city)
