from aiogram.dispatcher.filters.state import StatesGroup, State

class InputData(StatesGroup):
    name = State()
    region = State()
    company = State()
    position = State()
    contact1 = State()
    contact2 = State()
    contact3 = State()
    search = State()

class Passwords(StatesGroup):
    password = State()