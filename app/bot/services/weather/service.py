import httpx

from config import WEATHER_API_TOKEN

params = {'type': 'like',
          'units': 'metric',
          'lang': 'ru',
          'APPID': WEATHER_API_TOKEN}

url = "http://api.openweathermap.org/data/2.5/find"


async def get_city_weather(city_name: str) -> str:
    params['q'] = city_name
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, params=params)

    weather_info = response.json()
    city_name = city_name.capitalize()
    return parse_response(city_name, weather_info)


def parse_response(city_name: str, weather_info: dict) -> str:
    if weather_info['cod'] == 200:
        for city in weather_info['list']:
            if city['name'] == city_name:
                temp = int(round(city['main']['temp'],0))
                feels_like = int(round(city['main']['feels_like'],0))
                pressure = city['main']['pressure']
                humidity = city['main']['humidity']
                wind_speed = city['wind']['speed']
                clouds = city['clouds']['all']
                description = city['weather'][0]['description']

                return f"Погода в городе {city_name}:\n" \
                       f"Температура: {temp}°C\n" \
                       f"Ощущается как: {feels_like}°C\n" \
                       f"Атмосферное давление: {pressure} мм рт.ст.\n" \
                       f"Влажность: {humidity} %\n" \
                       f"Скорость ветра: {wind_speed} м/с\n" \
                       f"Обласность: {clouds} %\n" \
                       f"Описание: {description}"
