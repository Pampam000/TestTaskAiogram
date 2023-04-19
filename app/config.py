import os

import dotenv

dotenv.load_dotenv()

# Secret tokens

BOT_TOKEN = os.environ["BOT_TOKEN"]

WEATHER_API_TOKEN = os.environ["WEATHER_API_TOKEN"]

CURRENCY_CONVERTER_API_TOKEN = os.environ["CURRENCY_CONVERTER_API_TOKEN"]

# services

WEATHER_SERVICE_NAME = "Погода"

CURRENCY_SERVICE_NAME = "Курс валют"

CUTE_IMAGE_SERVICE_NAME = "Милая картинка"

POLLS_SERVICE_NAME = "Создать опрос"

ALL_SERVICE_NAMES = (WEATHER_SERVICE_NAME, CURRENCY_SERVICE_NAME,
                     CUTE_IMAGE_SERVICE_NAME, POLLS_SERVICE_NAME)


