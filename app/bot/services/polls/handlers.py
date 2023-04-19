from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.create_bot import bot
from bot.keyboards import start_keyboard
from bot.services.polls import utils, service
from bot.services.polls.schemas import Poll
from bot.services.polls.states import Polls
from bot.utils import chat_is_private, chat_is_private_callback
from config import POLLS_SERVICE_NAME
from logger import logger


async def get_group_id(message: Message):
    """
    Write the group ID to a file so that the bot can send polls there.
    The '/get_group_id' command must be written to the group chat once when
    setting up the bot for the first time
    """

    msg: str = service.get_group_id(str(message.chat.id))
    logger.info(msg)

    user_id = message.from_user.id
    await bot.send_message(user_id, msg)


async def start_creating_poll(callback: CallbackQuery):
    username = callback.from_user.full_name
    logger.info(f'{username} has chosen polls service')

    await Polls.question.set()
    await callback.message.answer("Введите вопрос")
    await callback.answer()


async def enter_question(message: Message, state: FSMContext):
    username = message.from_user.full_name
    logger.info(f'{username} entered {message.text}')

    async with state.proxy() as data:
        data['question'] = message.text

    await Polls.variant.set()
    await message.answer("Введите 1 вариант ответа")


async def enter_variant(message: Message, state: FSMContext):
    username = message.from_user.full_name
    logger.info(f'{username} entered {message.text})')

    async with state.proxy() as data:
        variant_number = len(data.as_dict().keys())
        data[f'{variant_number}_variant'] = message.text

    await utils.enter_next_variant(message=message, num=1, plus=1,
                                   variant_number=variant_number)


async def create_poll(callback: CallbackQuery, state: FSMContext):
    username = callback.from_user.full_name
    logger.info(f'{username} pressed "{callback.data}" button')

    async with state.proxy() as data:
        poll_info = data.as_dict()
        logger.info(f'{username}: {poll_info}')

    try:
        result: Poll = service.create_poll(poll_info)
    except FileNotFoundError:
        await callback.message.answer(
            "Выполните команду для получения ID группы")
    else:
        await bot.send_poll(chat_id=result.group_id, question=result.question,
                            options=result.variants)
        await callback.message.answer("Чем займёмся?",
                                      reply_markup=start_keyboard)
    finally:
        await state.finish()
        await callback.answer()
        logger.info(await state.get_state())


async def back(message: Message, state: FSMContext):
    username = message.from_user.full_name
    logger.info(f'{username} executed "/back" command')

    current_state: str = await state.get_state()
    logger.info(f'{username}: {current_state}')

    if "question" in current_state:
        await state.finish()
        await message.answer("Чем займёмся?",
                             reply_markup=start_keyboard)
    else:
        await utils.go_back(message=message, state=state)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(get_group_id,
                                lambda x: x.chat.id != x.from_user.id,
                                commands='get_group_id')
    dp.register_message_handler(back, chat_is_private,
                                commands="back", state=Polls.states)
    dp.register_callback_query_handler(
        start_creating_poll, chat_is_private_callback,
        lambda callback: POLLS_SERVICE_NAME in callback.data, state=None)
    dp.register_message_handler(enter_question, chat_is_private,
                                content_types="text", state=Polls.question)
    dp.register_message_handler(enter_variant, chat_is_private,
                                content_types='text', state=Polls.variant)
    dp.register_callback_query_handler(
        create_poll, chat_is_private_callback,
        lambda callback: POLLS_SERVICE_NAME in callback.data,
        state=Polls.variant)
