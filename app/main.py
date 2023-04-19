import uvloop
from aiogram.utils import executor

from bot import commands
from bot import handlers as bot_handlers
from bot.create_bot import dp
from bot.services.currency import handlers as currency_handlers
from bot.services.currency import service as currency_service
from bot.services.cute_pictures import handlers as cute_pictures_handlers
from bot.services.cute_pictures import service as cute_image_service
from bot.services.polls import handlers as polls_handlers
from bot.services.weather import handlers as weather_handlers
from logger import logger

bot_handlers.register_handlers(dp)
weather_handlers.register_handlers(dp)
currency_handlers.register_handlers(dp)
cute_pictures_handlers.register_handlers(dp)
polls_handlers.register_handlers(dp)

bot_handlers.register_wrong_handlers(dp)


async def on_startup(_):
    cute_image_service.download_images_from_google(max_num=5)
    await commands.set_bot_commands(dp)
    await currency_service.get_all_currency_names()

    logger.info("LET'S GO!")


if __name__ == '__main__':
    uvloop.install()
    executor.start_polling(dispatcher=dp, skip_updates=True,
                           on_startup=on_startup)
