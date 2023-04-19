from aiogram.dispatcher.filters.state import State, StatesGroup

class Weather(StatesGroup):
    enter_city = State()

