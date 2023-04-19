from aiogram.dispatcher.filters.state import State, StatesGroup


class Currency(StatesGroup):
    inputt = State()
    amount = State()
    output = State()
