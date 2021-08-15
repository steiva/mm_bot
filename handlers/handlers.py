from loader import bot, dp
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command
# from keyboards.default.default_keyboard import phone
from keyboards.inline.inline_keyboard import choice, yes_no
from states.text_states import InputData
from aiogram.dispatcher import FSMContext
import re
from sheets import sheet
from aiogram import types


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

@dp.message_handler(state=InputData.region)
async def get_region(message: Message, state=FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    await message.answer(text='Введите издание. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(Command('next'), state=InputData.region)
async def dont_get_region(message: Message, state=FSMContext):
    answer = ''
    await state.update_data(answer2=answer)
    await message.answer(text='Введите издание. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(state=InputData.company)
async def get_company(message: Message, state=FSMContext):
    answer = message.text
    await state.update_data(answer3=answer)
    await message.answer(text='Введите должность. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(Command('next'), state=InputData.company)
async def dont_get_company(message: Message, state=FSMContext):
    answer = ''
    await state.update_data(answer3=answer)
    await message.answer(text='Введите должность. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(state=InputData.position)
async def get_position(message: Message, state=FSMContext):
    answer = message.text
    await state.update_data(answer4=answer)
    await message.answer(text='Введите контакт №1. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(Command('next'),state=InputData.position)
async def dont_get_position(message: Message, state=FSMContext):
    answer = ''
    await state.update_data(answer4=answer)
    await message.answer(text='Введите контакт №1. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(state=InputData.contact1)
async def get_contact1(message: Message, state=FSMContext):
    answer = message.text
    await state.update_data(answer5=answer)
    await message.answer(text='Введите контакт №2. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(Command('next'), state=InputData.contact1)
async def dont_get_contact1(message: Message, state=FSMContext):
    answer = ''
    await state.update_data(answer5=answer)
    await message.answer(text='Введите контакт №2. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(state=InputData.contact2)
async def get_contact2(message: Message, state=FSMContext):
    answer = message.text
    await state.update_data(answer6=answer)
    await message.answer(text='Введите контакт №3. Если хотите пропустить, нажмите \n /next')
    await InputData.next()

@dp.message_handler(Command('next'), state=InputData.contact2)
async def get_contact2(message: Message, state=FSMContext):
    answer = ''
    await state.update_data(answer6=answer)
    await message.answer(text='Введите контакт №3. Если хотите пропустить, нажмите \n /next')
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
                        \nДолжность: {data['answer4']}\nКонтакт №1: {data['answer5']}\nКонтакт №2: {data['answer6']}\nКонтакт №3: {data['answer7']}",
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
                    \nДолжность: {data['answer4']}\nКонтакт №1: {data['answer5']}\nКонтакт №2: {data['answer6']}\nКонтакт №3: {data['answer7']}",
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


@dp.callback_query_handler(text='find_user')
async def find_user(call: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    await call.message.answer(text="Проведите поиск по ФИО, контактам или другим параметрам.")
    await InputData.search.set()


@dp.message_handler(state=InputData.search)
async def get_info2(message: Message):
    answer = message.text
    cells = sheet.findall(answer)
    if cells:
        for cell in cells:
            found_user = sheet.row_values(cell.row)
            await message.answer(
                text=f"Мы нашли пользователя:\nФИО: {found_user[0]} {found_user[1]}\nРегион: {found_user[2]}\nИздание: {found_user[3]}\
                    \nДолжность: {found_user[4]}\nКонтакт №1: {found_user[5]}\nКонтакт №2: {found_user[6]}\nКонтакт №3: {found_user[7]}")
    else:
        await message.answer(text='Пользователь не найден.')
