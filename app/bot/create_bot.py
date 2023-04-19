from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from config import BOT_TOKEN

bot: Bot = Bot(BOT_TOKEN)
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot, storage=storage)
