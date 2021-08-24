from loader import bot, dp
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, message
from aiogram.dispatcher.filters import Command
# from keyboards.default.default_keyboard import phone
from keyboards.inline.inline_keyboard import choice, yes_no
from states.text_states import InputData, Passwords
from aiogram.dispatcher import FSMContext
import re
from sheets import sheet
from aiogram import types
from config.config import admin_id, password

users_start = []

@dp.message_handler(lambda message: message.chat.id not in users_start, commands=['start'])
async def some(message: Message):
    await message.answer('У Вас нет прав на выполнение данной команды. Введите пароль.')
    await Passwords.password.set()

@dp.message_handler(state = Passwords.password)
async def check_password(message: Message, state=FSMContext):
    answer = message.text
    print(answer)
    if answer == password:
        users_start.append(message.chat.id)
        await message.answer('Отлично! вы получили доступ к боту.')
        await state.finish()
    else:
        await message.answer('Неправильный пароль!')

@dp.message_handler(Command("start"), state="*")
async def greeting(message: Message, state=FSMContext):
    await state.finish()
    await message.answer("Выберите действие:", reply_markup=choice)


@dp.callback_query_handler(text='add_user', state="*")
async def get_info1(call: CallbackQuery, state=FSMContext):
    await state.finish()
    await bot.answer_callback_query(callback_query_id=call.id)
    await call.message.answer(text="Введите фамилию, а затем имя:")
    await InputData.name.set()

@dp.message_handler(state=InputData.name)
async def get_name(message: Message, state=FSMContext):
    answer = message.text
    answer = answer.split(' ')
    await state.update_data(last_name=answer[0])
    if len(answer) > 1:
        await state.update_data(first_name=answer[1])
        await message.answer(text='Введите регион. Если хотите пропустить, нажмите \n /next')
        await InputData.next()
    else:
        await message.answer(text='Имя введено некорректно. Пожалуйста, попробуйте ввести заново:')

@dp.message_handler(state=InputData.region)
async def get_region(message: Message, state=FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    await message.answer(text='Введите издание. Поле обязательно к заполнению!')
    await InputData.next()

@dp.message_handler(Command('next'), state=InputData.region)
async def dont_get_region(message: Message, state=FSMContext):
    answer = ''
    await state.update_data(answer2=answer)
    await message.answer(text='Введите издание. Поле обязательно к заполнению!')
    await InputData.next()

@dp.message_handler(state=InputData.company)
async def get_company(message: Message, state=FSMContext):
    answer = message.text
    await state.update_data(answer3=answer)
    await message.answer(text='Введите должность. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

# @dp.message_handler(Command('next'), state=InputData.company)
# async def dont_get_company(message: Message, state=FSMContext):
#     answer = ''
#     await state.update_data(answer3=answer)
#     await message.answer(text='Введите должность. Если хотите пропустить, нажмите \n /next')
#     await InputData.next()

@dp.message_handler(state=InputData.position)
async def get_position(message: Message, state=FSMContext):
    answer = message.text
    await state.update_data(answer4=answer)
    await message.answer(text='Введите номер телефона. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(Command('next'),state=InputData.position)
async def dont_get_position(message: Message, state=FSMContext):
    answer = ''
    await state.update_data(answer4=answer)
    await message.answer(text='Введите номер телефона. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(state=InputData.contact1)
async def get_contact1(message: Message, state=FSMContext):
    answer = message.text
    await state.update_data(answer5=answer)
    await message.answer(text='Введите e-mail. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(Command('next'), state=InputData.contact1)
async def dont_get_contact1(message: Message, state=FSMContext):
    answer = ''
    await state.update_data(answer5=answer)
    await message.answer(text='Введите e-mail. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(state=InputData.contact2)
async def get_contact2(message: Message, state=FSMContext):
    answer = message.text
    await state.update_data(answer6=answer)
    await message.answer(text='Введите ссылку на соцсеть / Telegram. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(Command('next'), state=InputData.contact2)
async def get_contact2(message: Message, state=FSMContext):
    answer = ''
    await state.update_data(answer6=answer)
    await message.answer(text='Введите ссылку на соцсеть / Telegram. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(state=InputData.contact3)
async def get_contact3(message: Message, state=FSMContext):
    answer = message.text
    await state.update_data(answer7=answer)
    data = await state.get_data()
    print(data)

    for key, value in data.items():
        if value == '/next':
            data[key] = ''

    await message.answer(text=f"Вы ввели:\nФИО: {data['last_name']} {data['first_name']}\nРегион: {data['answer2']}\nИздание: {data['answer3']}\
                        \nДолжность: {data['answer4']}\nНомер телефона: {data['answer5']}\ne-mail: {data['answer6']}\nСсылка на соцсеть / Telegram: {data['answer7']}",
                        reply_markup=yes_no)

@dp.message_handler(Command('next'),state=InputData.contact3)
async def get_contact3(message: Message, state=FSMContext):
    answer = ''
    await state.update_data(answer7=answer)
    data = await state.get_data()
    print(data)

    for key, value in data.items():
        if value == '/next':
            data[key] = ''

    await message.answer(text=f"Вы ввели:\nФИО: {data['last_name']} {data['first_name']}\nРегион: {data['answer2']}\nИздание: {data['answer3']}\
                        \nДолжность: {data['answer4']}\nНомер телефона: {data['answer5']}\ne-mail: {data['answer6']}\nСсылка на соцсеть / Telegram: {data['answer7']}",
                        reply_markup=yes_no)
# @dp.message_handler(state=InputData.S1)
# async def get_info2(message: Message):
#     answer = message.text
#     global x
#     x = re.findall(r'\b\w+\b', answer)
#     phone_number = x[-1]

#     if phone_number[0] == '7':
#         phone_number = '+' + phone_number
#     global string
#     string = ''
#     for word in x[2:-1]:
#         string += word + ' '
#     string = string[:-1]
#     await message.answer(text=f"Вы ввели:\nИмя: {x[0]} {x[1]}\nПринадлежность: {string}\nНомер телефона: {phone_number}",
#                          reply_markup=yes_no)


# @dp.callback_query_handler(text='enter_again', state=InputData.S1)
# async def get_info1(call: CallbackQuery):
#     await bot.answer_callback_query(callback_query_id=call.id)
#     await call.message.answer(text="Введите Имя, Фамилию, принадлежность и номер телефона.")


@dp.callback_query_handler(text='affirmative', state=InputData.contact3)
async def affirmation(call: CallbackQuery, state=FSMContext):
    await bot.answer_callback_query(callback_query_id=call.id)
    data = await state.get_data()
    for key, value in data.items():
        if value == '/next':
            data[key] = ''
    sheet.insert_row([value for key, value in data.items()], index = 2)
    await state.finish()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(text='Спасибо за ваш вклад в базу! Чтобы вернуть меню, нажмите /start.')


@dp.callback_query_handler(text='find_user')
async def find_user(call: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    await call.message.answer(text="Проведите поиск по ФИО, контактам или другим параметрам.")
    await InputData.search.set()

keys = ['Фамилия', 'Имя', 'Регион', 'Издание', 'Должность', 'Номер телефона', 'e-mail', 'Ссылка на соцсеть / Telegram']
@dp.message_handler(state=InputData.search)
async def get_info2(message: Message):
    answer = message.text
    cells = sheet.findall(re.compile(answer, flags=re.IGNORECASE))
    print(cells)
    if cells:
        row_idxs = []
        for cell in cells:
            if cell.row not in row_idxs:
                row_idxs.append(cell.row)

        for row_idx in row_idxs:
            found_user = sheet.row_values(row_idx)
            result_dict = {}
            for i, element in enumerate(found_user):
                result_dict[keys[i]] = element

            message_text = 'Мы нашли пользователя:\n'
            for k,v in result_dict.items():
                message_text += f'{k}: {v}\n'
            await message.answer(text=message_text)
        await message.answer(text=f'Для поиска другого журналиста просто напишите в чат \U0001F642')
    else:
        await message.answer(text='Пользователь не найден.')
