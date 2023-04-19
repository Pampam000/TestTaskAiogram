from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from logger import logger
from .keyboards import create_poll_keyboard
from .states import Polls


async def go_back(message: Message, state: FSMContext):
    async with state.proxy() as data:
        poll_info = data.as_dict()
        poll_keys: int = len(poll_info.keys())
        if poll_keys == 1:
            await Polls.previous()
            await message.answer("Введите название опроса")
        else:
            variants: int = poll_keys - 1
            await enter_next_variant(message=message, plus=0,
                                     variant_number=variants, num=2)
            del data[f'{variants}_variant']


async def enter_next_variant(message: Message, variant_number: int, num: int,
                             plus: int):
    if variant_number > num:
        await message.answer(f"Введите {variant_number + plus} вариант ответа",
                             reply_markup=create_poll_keyboard)
    else:
        await message.answer(f"Введите {variant_number + plus} вариант ответа")
