from aiogram.dispatcher.filters.state import State, StatesGroup


class Polls(StatesGroup):
    question = State()
    variant = State()
