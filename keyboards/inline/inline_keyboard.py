from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Найти пользователя", callback_data="find_user")
        ],
        [
            InlineKeyboardButton(text="Добавить пользователя", callback_data="add_user")
        ]
    ]
)

yes_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Все верно", callback_data="affirmative"),
            InlineKeyboardButton(text="Ввести заново", callback_data="add_user")
        ]
    ]
)