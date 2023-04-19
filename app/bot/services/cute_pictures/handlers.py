from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InputFile

from bot.create_bot import bot
from bot.keyboards import start_keyboard
from config import CUTE_IMAGE_SERVICE_NAME
from logger import logger
from . import service


async def get_cute_image(callback: CallbackQuery):
    username = callback.from_user.full_name
    logger.info(f'{username} has chosen cute images service)')
    image = service.get_image()
    chat_id = callback.from_user.id
    photo = InputFile(image)

    await bot.send_photo(chat_id=chat_id, photo=photo)
    await callback.message.answer("Чем займёмся?",
                                  reply_markup=start_keyboard)
    await callback.answer()


def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        get_cute_image,
        lambda callback: CUTE_IMAGE_SERVICE_NAME in callback.data,
        state=None)
