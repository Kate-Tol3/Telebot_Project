import telebot.types
from database import DB_connect
import re
import datetime
import time

TOKEN = '6809084128:AAHVeXjueYraL-GwbFrYqgOdmQ89itI9Z_c'

# !/usr/bin/python

users = {}
messages = {}
names = {}
times = {}
db_conn = DB_connect()

# decorator for printing satus
def printf(func):
    async def wrapper(msg):
        global users
        await func(msg)
        print(users)

    return wrapper


# Add bot
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(TOKEN)

# /* KEYBOARDS */
# welcome keyboard

welcome_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_add_note = telebot.types.KeyboardButton(text="Добавить заметку")
button_delete_note = telebot.types.KeyboardButton(text="Удалить заметку")
button_show_list_note = telebot.types.KeyboardButton(text="Показать список заметок")
button_special_keyboard = telebot.types.KeyboardButton(text="Особые возможности")
welcome_keyboard.add(button_add_note, button_delete_note, button_show_list_note, button_special_keyboard)

# special features keyboard

special_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_go_into_mod = telebot.types.KeyboardButton(text="Выбрать мод")
button_add_key_word = telebot.types.KeyboardButton(text="Добавить ключевое слово")
button_remind_about_note = telebot.types.KeyboardButton(text="Добавить напоминание о заметке")
button_not_remind_about_note = telebot.types.KeyboardButton(text="Отменить напоминание о заметке")
button_create_todo_list = telebot.types.KeyboardButton(text="Создать список дел")
button_go_back = telebot.types.KeyboardButton(text="Назад")
special_keyboard.add( button_remind_about_note, button_not_remind_about_note,
                     button_create_todo_list, button_go_back)

# naming_note_keyboard

naming_note_keyboard = telebot.types.InlineKeyboardMarkup()
button_yes_naming = telebot.types.InlineKeyboardButton(text="Да", callback_data='naming')
button_no_naming = telebot.types.InlineKeyboardButton(text="Нет", callback_data='not_naming')
naming_note_keyboard.add(button_no_naming, button_yes_naming)

# save/change
ans_keyboard = telebot.types.InlineKeyboardMarkup()
button_save = telebot.types.InlineKeyboardButton(text="Сохранить", callback_data='save_note')
button_change = telebot.types.InlineKeyboardButton(text="Изменить", callback_data='change_note')
ans_keyboard.add(button_save, button_change)

# confirm
confirm_keyboard = telebot.types.InlineKeyboardMarkup()
button_delete = telebot.types.InlineKeyboardButton(text="Удалить", callback_data='delete_note')
button_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data='go_back')
confirm_keyboard.add(button_delete, button_back)

# show_note_keyboard

show_note_keyboard = telebot.types.InlineKeyboardMarkup()
button_yes_show = telebot.types.InlineKeyboardButton(text="Да", callback_data='show')
button_no_show = telebot.types.InlineKeyboardButton(text="Нет", callback_data='not_show')
show_note_keyboard.add(button_no_show, button_yes_show)

# reminder_note_keyboard

reminder_note_keyboard = telebot.types.InlineKeyboardMarkup()
button_yes_show = telebot.types.InlineKeyboardButton(text="Да", callback_data='reminder')
button_no_show = telebot.types.InlineKeyboardButton(text="Нет", callback_data='no_reminder')
reminder_note_keyboard.add(button_no_show, button_yes_show)

# regular_note_keyboard
regular_note_keyboard = telebot.types.InlineKeyboardMarkup()
button_yes_regular = telebot.types.InlineKeyboardButton(text="Да", callback_data='regular')
button_no_regular = telebot.types.InlineKeyboardButton(text="Нет", callback_data='no_regular')
reminder_note_keyboard.add(button_no_regular, button_yes_regular)

''' /* MAIN BOT */'''

async def send_notification():
    list = db_conn.check_notification()
    for user_id, message in list:
        try:
            await bot.send_message(user_id, " НАПОМИНАЮ!!!\n" + message)
        except Exception as e:
            print(e)

def convert(date_time):
    format = '%b %d %Y %I:%M:%p'
    datetime_str = datetime.datetime.strptime(date_time, format)

    return datetime_str

@bot.message_handler(commands=['help', 'start'])
@printf
async def send_welcome(msg):
    global users
    print(msg)
    db_conn.add_user(msg.from_user.id, msg.from_user.username, msg.from_user.first_name, msg.from_user.last_name)
    await bot.send_message(msg.chat.id, "Выберите действие", reply_markup=welcome_keyboard)
    users[msg.from_user.id] = {'status': 'selecting_action'}


# users[msg.from_user.id] = {'status': 'selecting_action', 'data': {}}


@bot.message_handler(
    func=lambda msg: users[msg.from_user.id] == {'status': 'going_back'} if users[msg.from_user.id] else False)
async def send_welcome_menu(msg):
    global users
    await bot.send_message(msg.chat.id, " ", reply_markup=welcome_keyboard)
    users[msg.from_user.id] = {'status': 'selecting_action'}


@bot.message_handler(
    func=lambda msg: msg.text == 'Особые возможности' and users[msg.from_user.id] == {'status': 'selecting_action'} if
    users[msg.from_user.id] else False)
@printf
async def show_special_keyboard(msg):
    await bot.send_message(msg.chat.id, "Что вы хотите сделать?", reply_markup=special_keyboard)


@bot.message_handler(
    func=lambda msg: msg.text == 'Добавить заметку' and users[msg.from_user.id] == {'status': 'selecting_action'} if
    users[msg.from_user.id] else False)
@printf
async def add_note(msg):
    global users
    # users[msg.from_user.id] = {'status':'naming_note'}
    await bot.send_message(msg.chat.id, "Будете наименовать заметку?", reply_markup=naming_note_keyboard)

    # users[msg.from_user.id]== {'status':'selecting_action'}


@bot.message_handler(
    func=lambda msg: msg.text == 'Удалить заметку' and users[msg.from_user.id] == {'status': 'selecting_action'} if
    users[msg.from_user.id] else False)
@printf
async def delete_note(msg):
    global users
    users[msg.from_user.id] = {'status': 'deleting_note'}
    # user_users.delete_note()
    await bot.send_message(msg.chat.id, "Выберите заметку")
    # users[msg.from_user.id] = {'status': 'selecting_action'}


@bot.message_handler(func=lambda msg: msg.text == 'Показать список заметок' and users[msg.from_user.id][
    'status'] == 'selecting_action' if users[msg.from_user.id] else False)
@printf
async def show_list_note(msg):
    global users
    users[msg.from_user.id] = {'status': 'showing_list_notes'}
    # user_users.show_list_note_note()
    await bot.send_message(msg.chat.id, "Список заметок:")
    list = db_conn.get_list(msg.from_user.id)
    for el in list:
        await bot.send_message(msg.chat.id, el)
    await bot.send_message(msg.chat.id, "Хотите посмотреть содержание какой-либо заметки? ",
                           reply_markup=show_note_keyboard)


# @bot.message_handler(func=lambda msg: msg.text == 'Вернуться в начало'and users[msg.from_user.id]['status'] == 'selecting_action' if users[msg.from_user.id] else False)
# @printf
# async def go_back (msg):
#     global users
#     users[msg.from_user.id] = {'status': 'going_back'}
#     #user_users.go_back()
#     await bot.send_message(msg.chat.id, "/start")
#     users[msg.from_user.id] = {'status': 'selecting_action'}


# adding_notes

@bot.callback_query_handler(func=lambda call: call.data == 'naming')
@printf
async def save_btn(call):
    global users
    message = call.message
    chat_id = message.chat.id
    users[call.from_user.id] = {'status': 'add_name'}
    await bot.send_message(message.chat.id, "Введите название заметки:")

    # await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id)


# @bot.callback_query_handler(func=lambda call: call.data == 'add_name')
# @printf
# async def save_btn(call):
#    global users
#    message = call.message
#    chat_id = message.chat.id
#    await bot.send_message(chat_id, f'Название заметки сохранено')
#    users[call.from_user.id] = {'status': 'adding_note'}
#    await bot.send_message(message.chat.id, "Введите заметку")

#
@bot.message_handler(
    func=lambda msg: users[msg.from_user.id] == {'status': 'add_name'} if users[msg.from_user.id] else False)
@printf
async def add_note(msg):
    global users
    # users[msg.from_user.id] = {'status': 'making_note'}
    await bot.send_message(msg.chat.id, "Название заметки сохранено")
    # await bot.send_message(chat_id, f'Название заметки сохранено')
    users[msg.from_user.id] = {'status': 'adding_note'}
    names[msg.from_user.id] = msg.text
    await bot.send_message(msg.chat.id, "Введите заметку")
    # await bot.send_message(msg.chat.id, "Сохранить заметку?", reply_markup=ans_keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'not_naming')
@printf
async def save_btn(call):
    global users
    message = call.message
    chat_id = message.chat.id
    names[call.from_user.id] = " "
    users[call.from_user.id] = {'status': 'adding_note'}
    await bot.send_message(message.chat.id, "Введите заметку")


@bot.message_handler(
    func=lambda msg: users[msg.from_user.id] == {'status': 'adding_note'} if users[msg.from_user.id] else False)
@printf
async def add_note(msg):
    global users
    messages[msg.from_user.id] = msg.text
    await bot.send_message(msg.chat.id, "Сохранить заметку?", reply_markup=ans_keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'save_note')
@printf
async def save_btn(call):
    global users
    message = call.message
    chat_id = message.chat.id
    db_conn.add_note(names[call.from_user.id], call.from_user.id, messages[call.from_user.id])
    # users[call.from_user.id] = {'status': 'saving_note'}
    # await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id)
    await bot.send_message(chat_id, "Заметка сохранена")
    await bot.send_message(chat_id, 'Хотите добавить напоминание для этой заметки?', reply_markup=reminder_note_keyboard)
    # users[call.from_user.id] = {'status': 'selecting_action'}
    # print(call)


@bot.callback_query_handler(func=lambda call: call.data == 'reminder')
@printf
async def change_btn(call):
    global users
    message = call.message
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Ваше напоминание регулярное?',
                           reply_markup=regular_note_keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'regular')
@printf
async def change_btn(call):
    global users
    message = call.message
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Введите время напоминания в формате дд.мм.гггг чч:мм")
    users[call.from_user.id] = {'status': 'setting_time'}


@bot.callback_query_handler(func=lambda call: call.data == 'no_regular')
@printf
async def change_btn(call):
    global users
    message = call.message
    chat_id = message.chat.id


    await bot.send_message(msg.chat.id, f'Напоминание о заметке добавлено. Выберите следующее действие.')
    users[msg.from_user.id] = {'status': 'selecting_action'}


@bot.callback_query_handler(func=lambda call: call.data == 'no_reminder')
@printf
async def change_btn(call):
    global users
    #message = call.message
    #chat_id = message.chat.id
    await bot.send_message(call.message.chat.id, "Выберете следующее действие")
    users[call.from_user.id] = {'status': 'selecting_action'}
    #await bot.send_message(chat_id, f'Выберите следующее действие.')



@bot.callback_query_handler(func=lambda call: call.data == 'change_note')
@printf
async def change_btn(call):
    global users
    message = call.message
    chat_id = message.chat.id
    await bot.send_message(chat_id, f'Введите новую заметку')
    users[call.from_user.id] = {'status': 'adding_note'}


# deleting_notes

@bot.message_handler(
    func=lambda msg: users[msg.from_user.id]['status'] == 'deleting_note' if users[msg.from_user.id] else False)
@printf
async def delete_note(msg):
    global users
    names[msg.from_user.id] = msg.text
    users[msg.from_user.id] = {'status': 'confirming_delete'}
    await bot.send_message(msg.chat.id, "Точно хотите удалить заметку?", reply_markup=confirm_keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'delete_note')
@printf
async def del_btn(call):
    global users
    users[call.from_user.id] = {'status': 'removing_note'}
    db_conn.delete_note(names[call.from_user.id], call.from_user.id)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id)
    await bot.send_message(call.message.chat.id, f'Заметка удалена. Выберите следующее действие.')
    users[call.from_user.id] = {'status': 'selecting_action'}


@bot.callback_query_handler(func=lambda call: call.data == 'go_back')
@printf
async def del_btn(call):
    global users
    await bot.send_message(call.message.chat.id, f'Выберите следующее действие')
    # await bot.send_message(call.message.chat.id, "Выберите заметку")
    users[call.from_user.id] = {'status': 'selecting_action'}


# showing list

@bot.message_handler(func=lambda msg: msg.text == 'Показать список заметок' and users[msg.from_user.id][
    'status'] == 'showing_list_notes' if users[msg.from_user.id] else False)
@printf
async def show_list_note(msg):
    global users
    users[msg.from_user.id] = {'status': 'choosing_note'}
    # user_users.show_list_note_note()

    # users[msg.from_user.id] = {'status': 'selecting_action'}


@bot.callback_query_handler(func=lambda call: call.data == 'show')
@printf
async def show_btn(call):
    global users
    await bot.send_message(call.message.chat.id, "Выберите заметку")
    #УСЛОВИЕ НА СУЩЕСТВОВАНИЕ ЗАМЕТКИ
    #if 1==0:
    #    users[call.from_user.id] = {'status': 'showing_note'}
    #else:
    #    await bot.send_message(call.message.chat.id, "Такой заметки нет. Выберите следующее действие")
    #    users[call.from_user.id] = {'status': 'selecting_action'}
    users[call.from_user.id] = {'status': 'showing_note'} #СТАРАЯ ВЕРСИЯ

@bot.message_handler(func=lambda msg: users[msg.from_user.id] == {'status': 'showing_note'} if users[
    msg.from_user.id] else False)  # msg.text in note_list and
@printf
async def show_note(msg):
    global users
    names[msg.from_user.id] = msg.text
    await bot.send_message(msg.chat.id, "Самые подходящие заметки: ")
    text = db_conn.get_note_text(msg.text, msg.from_user.id)
    for el in text:
        await bot.send_message(msg.chat.id, el[0] + "\n" + el[1])
    await bot.send_message(msg.chat.id, "Выберите следующее действие")
    users[msg.from_user.id] = {'status': 'selecting_action'}


@bot.callback_query_handler(func=lambda call: call.data == 'not_show')
@printf
async def not_show_btn(call):
    global users
    # await bot.send_message(message.chat.id, "Ваша заметка ")
    await bot.send_message(call.message.chat.id, "Выберите следующее действие")
    users[call.from_user.id] = {'status': 'selecting_action'}


@bot.message_handler(func=lambda msg: users[msg.from_user.id] == 'saving_note' if users[msg.from_user.id] else False)
async def save_note(msg):
    global users
    if msg.text == "yes":
        await bot.send_message(msg.chat.id, "Заметка сохранена")
    else:
        await bot.send_message(msg.chat.id, "Заметка не сохранена")
    users[msg.from_user.id] = 'selecting_action'


@bot.message_handler(func=lambda msg: users[msg.from_user.id] == 'saving_note' if users[msg.from_user.id] else False)
async def save_note(msg):
    global users
    if msg.text == "yes":
        await bot.send_message(msg.chat.id, "Заметка сохранена")
    else:
        await bot.send_message(msg.chat.id, "Заметка не сохранена")
    users[msg.from_user.id] = 'selecting_action'


# bot.message_handler(func=lambda msg: users[msg.from_user.id] == 'add_name' if users[msg.from_user.id] else False)
# async def adding_name(msg):
#    global users
#    if msg.text == "yes":
#        await bot.send_message(msg.chat.id, "Заметка сохранена")
#    else:
#       await bot.send_message(msg.chat.id, "Заметка не сохранена")
#    users[msg.from_user.id] = 'selecting_action'


# @bot.message_handler(commands=['start'])
# def welcome(msg):
#     chat_id = msg.chat.id
#     button_support = telebot.types.KeyboardButton(text="Написать в поддержку")
#     keyboard.add(button_support)
#     await bot.send_message(chat_id,
#                      'Добро пожаловать в бота сбора обратной связи',
#                      reply_markup=keyboard)

# @bot.message_handler(func=lambda msg: True)
# async def echo_message(msg):
#     await bot.reply_to(msg, msg.text)
# # Handle all other messages with content_type 'text' (content_types defaults to ['text'])


# users= { }
#
# @bot.message_handlder(func = lambda x: users[user_id]["await_after_button"] if users[user_id] else False)
# def do_something_after_button(msg):
#     global users
#     users[msg.from_user.id]["await_after_button"] = False
#     print("хаха, оно работает")
#
#
# @bot.message_handler(regex=r"Моя кнопка")
# def on_button(msg):
#     global users
#     users[msg.from_user.id]["await_after_button"] = True

# special

@bot.message_handler(
    func=lambda msg: msg.text == 'Создать список дел' and users[msg.from_user.id]['status'] == 'selecting_action' if
    users[msg.from_user.id] else False)
@printf
async def add_note(msg):
    global users
    users[msg.from_user.id] = {'status': 'creating_list'}
    await bot.send_message(msg.chat.id, "Выберите день : (сегодня/завтра)")


@bot.message_handler(
    func=lambda msg: users[msg.from_user.id] == {'status': 'creating_list'} if users[msg.from_user.id] else False)
@printf
async def show_list_note(msg):
    global users
    await bot.send_message(msg.chat.id, "Список дел:")

    await bot.send_message(msg.chat.id, "Выберите следующее действие")
    users[msg.from_user.id] = {'status': 'selecting_action'}


@bot.message_handler(func=lambda msg: msg.text == 'Отменить напоминание о заметке' and users[msg.from_user.id][
    'status'] == 'selecting_action' if users[msg.from_user.id] else False)
@printf
async def add_note(msg):
    global users
    await bot.send_message(msg.chat.id, "Выберите заметку")
    # УСЛОВИЕ НА СУЩЕСТВОВАНИЕ ЗАМЕТКИ
    #if 1==1:
    #    users[msg.from_user.id] = {'status': 'deleting_reminder'}
    #else:
    #    await bot.send_message(msg.chat.id, "Такой заметки нет. Выберите следующее действие")
    #    users[msg.from_user.id] = {'status': 'selecting_action'}
    users[msg.from_user.id] = {'status': 'deleting_reminder'}  # СТАРАЯ ВЕРСИЯ


@bot.message_handler(
    func=lambda msg: users[msg.from_user.id] == {'status': 'deleting_reminder'} if users[msg.from_user.id] else False)
@printf
async def show_list_note(msg):
    global users
    await bot.send_message(msg.chat.id, "Напоминание о заметке удалено. Выберите следующее действие")
    users[msg.from_user.id] = {'status': 'selecting_action'}

@bot.message_handler(
    func=lambda msg: msg.text == 'Назад' and users[msg.from_user.id]['status'] == 'selecting_action' if users[msg.from_user.id] else False)
@printf
async def send_welcome(msg):
    global users
    await bot.send_message(msg.chat.id, "Выберете действие", reply_markup=welcome_keyboard)
    users[msg.from_user.id] = {'status': 'selecting_action'}


@bot.message_handler(func=lambda msg: msg.text == 'Добавить напоминание о заметке' and users[msg.from_user.id]['status'] == 'selecting_action' if users[msg.from_user.id] else False)
@printf
async def add_note(msg):
    global users
    users[msg.from_user.id] = {'status': 'adding_reminder'}
    await bot.send_message(msg.chat.id, "Выберите заметку")


@bot.message_handler(
    func=lambda msg: users[msg.from_user.id] == {'status': 'adding_reminder'} if users[msg.from_user.id] else False)
@printf
async def show_list_note(msg):
    global users
    names[msg.from_user.id] = msg.text
    users[msg.from_user.id] = {'status': 'setting_time'}
    await bot.send_message(msg.chat.id, "Время напоминания:")


@bot.message_handler(
    func=lambda msg: users[msg.from_user.id] == {'status': 'setting_time'} if users[msg.from_user.id] else False)
@printf
async def show_list_note(msg):
    global users
    if (re.find(r"[0-3][0-9]\.[0-1][0-9]\.[0-9]{4}\S*[0-2][0-9]:[0-5][0-9]:[0-5][0-9", msg.text)):
        date_time = convert(msg.text)
        db_conn.set_notification(names[msg.from_user.id],msg.from_user.id, date_time)

    await bot.send_message(msg.chat.id, "Время напоминания установлено. Выберите следующее действие")
    users[msg.from_user.id] = {'status': 'selecting_action'}


@bot.message_handler(
    func=lambda msg: msg.text == 'Назад' and users[msg.from_user.id]['status'] == 'time_installed' if users[
        msg.from_user.id] else False)
@printf
async def send_welcome_after(msg):
    global users
    await bot.send_message(msg.chat.id, "Выберете действие", reply_markup=welcome_keyboard)
    users[msg.from_user.id] = {'status': 'selecting_action'}


import asyncio
from update import UpdateManager

async def UpdateProccesses():
    update = UpdateManager()
    await update.addSignalCronListener("* * * * *", "SEND_NOTIFICATION", send_notification)
    await update.startSignalListener()

async def start():
    # Coroutine's functions list
    subSystemsTasks: list = []
    loop: asyncio.AbstractEventLoop

    # Infinity check/update something from system/modules/updater

   # subSystemsTasks.append()
    task1 = UpdateProccesses()
    # Telegram Infinity Polling

    task2 = bot.infinity_polling()
    #asyncio.run(bot.polling())
    await asyncio.gather(task1, task2)
    #subSystemsTasks.append(telegram)

    # Start infinity await
    #waiter = asyncio.wait(subSystemsTasks)

  #  await waiter
    #return waiter

asyncio.run(start())



