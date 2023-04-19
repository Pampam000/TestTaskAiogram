from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_bot_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        BotCommand("start", "Запустить бота"),
        BotCommand("back", "Вернуться на шаг назад"),
        BotCommand("mainmenu", "В главное меню")
    ])
