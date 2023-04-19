from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards import start_keyboard
from config import CURRENCY_SERVICE_NAME
from logger import logger
from . import service
from .schemas import CurrencyData
from .states import Currency


async def enter_currency_input_callback(callback: CallbackQuery):
    username = callback.from_user.full_name
    logger.info(f'{username} has chosen currency service)')

    await Currency.inputt.set()
    await callback.message.answer(
        "Укажите валюту, которую нужно конвертировать\n"
        "Например: EUR, RUB, USD")
    await callback.answer()


async def enter_currency_input(message: Message, state: FSMContext):
    inputt = message.text.upper()
    username = message.from_user.full_name
    logger.info(f'{username} entered {inputt})')

    if service.check_if_currency_exists(inputt):
        logger.info(f'{username}:{inputt} exists in a list of currency')
        async with state.proxy() as data:
            data['inputt'] = inputt

        await Currency.amount.set()
        await message.answer(f"Сколько {message.text} нужно поменять?")

    else:
        logger.info(f'{username}{inputt} NOT exists in a list of currency')
        await message.answer("Такой валюты не существует.\n"
                             "Попробуйте ещё раз")


async def enter_currency_amount(message: Message, state: FSMContext):
    username = message.from_user.full_name
    logger.info(f'{username} entered {message.text})')

    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        logger.info(f"{username}:{message.text} is not valid")
        await message.answer("Пожалуйства введите положительное число.\n"
                             "Если это дробь, то введите число через точку.")
    else:
        logger.info(f"{username}:{message.text} is valid")
        async with state.proxy() as data:
            data['amount'] = amount

        await Currency.output.set()
        await message.answer("На какую валюту нужно обменять?")


async def enter_currency_output(message: Message, state: FSMContext):
    output = message.text.upper()
    username = message.from_user.full_name
    logger.info(f'{username} entered {output})')

    if service.check_if_currency_exists(output):

        logger.info(f'{username}:{output} exists in a list of currency')
        async with state.proxy() as data:
            data['output'] = output
        data = CurrencyData(**data.as_dict())
        result: float = await service.convert_currency(data)

        await message.answer(
            f"{data.amount} {data.inputt} = {result} {data.output}")
        await state.finish()
        await message.answer("Чем займёмся?",
                             reply_markup=start_keyboard)

    else:
        logger.info(f'{username}:{output} exists in a list of currency')
        await message.answer("Такой валюты не существует.\n"
                             "Попробуйте ещё раз")


async def back(message: Message, state: FSMContext):
    username = message.from_user.full_name
    logger.info(f'{username} executed "/back" command')

    await Currency.previous()
    current_state: str = await state.get_state()
    logger.info(f'{username}: {current_state}')

    if not current_state:
        await message.answer("Чем займёмся?",
                             reply_markup=start_keyboard)
    elif "inputt" in current_state:
        await message.answer("Укажите валюту, которую нужно конвертировать")
    elif "amount" in current_state:
        async with state.proxy() as data:
            await message.answer(f"Сколько {data['inputt']} нужно поменять?")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(back, commands="back",
                                state=Currency.states)
    dp.register_callback_query_handler(
        enter_currency_input_callback,
        lambda callback: CURRENCY_SERVICE_NAME in callback.data,
        state=None)
    dp.register_message_handler(enter_currency_input, content_types="text",
                                state=Currency.inputt)
    dp.register_message_handler(enter_currency_amount, content_types="text",
                                state=Currency.amount)
    dp.register_message_handler(enter_currency_output, content_types="text",
                                state=Currency.output)
