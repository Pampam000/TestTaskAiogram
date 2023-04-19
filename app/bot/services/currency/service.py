import json
import os

import httpx

from bot.services.currency.schemas import CurrencyData
from config import CURRENCY_CONVERTER_API_TOKEN

url = f'https://v6.exchangerate-api.com/v6/{CURRENCY_CONVERTER_API_TOKEN}/' \
      f'latest/'


def check_if_currency_exists(name: str) -> bool:
    filename = os.path.basename(__file__)
    filepath = os.path.abspath(__file__).replace(filename, 'names.json')
    with open(filepath, 'r') as file:
        names: list[str] = json.load(file)
        return name in names


async def convert_currency(data: CurrencyData) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url + data.inputt)

    conversion_rates: dict = response.json()['conversion_rates']
    multiplier: float = conversion_rates.get(data.output)
    return round(multiplier * data.amount, 2)


async def get_all_currency_names():
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url + "USD")

    filename = os.path.basename(__file__)
    filepath = os.path.abspath(__file__).replace(filename, 'names.json')

    try:
        with open(filepath, 'r'):
            pass
    except FileNotFoundError:
        with open(filepath, 'w') as file:
            all_currency = list(response.json()['conversion_rates'].keys())
            json.dump(all_currency, file, indent=4)
