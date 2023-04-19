from aiogram.types import Message, CallbackQuery


def chat_is_private(message: Message):
    return message.from_user.id == message.chat.id


def chat_is_private_callback(callback: CallbackQuery):
    return callback.from_user.id == callback.message.chat.id
