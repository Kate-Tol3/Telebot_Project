import telebot.types

TOKEN = '6800574446:AAG1B5NSyjiX8Y84WbKACBNW6b6VYQyVgpk'

#!/usr/bin/python

from telebot.async_telebot import AsyncTeleBot
bot = AsyncTeleBot(TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(msg):
    welcome_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_add_note = telebot.types.KeyboardButton(text = "Добавить заметку")
    button_delete_note = telebot.types.KeyboardButton(text = "Удалить заметку")
    button_show_list_note = telebot.types.KeyboardButton(text = "Показать список заметок")
    button_special_keyboard = telebot.types.KeyboardButton(text = "Особые возможности")
    welcome_keyboard.add(button_add_note, button_delete_note, button_show_list_note, button_special_keyboard)
    await bot.send_message(msg.chat.id,"HI?", reply_markup=welcome_keyboard )
    state[msg.from_user.id] = 'selecting_action'



def printf(func):
    async def wrapper(msg):
        global state
        await func(msg)
        print(state)
    return wrapper


# from transitions import Machine
#
# class MyStates:
#     states = ['start', 'selecting_action','making_changes', 'saving_changes', 'back_to menu']
#     transitions = [
#         {'trigger': 'select_action', 'source': 'start', 'dest': 'selecting_action'},
#         {'trigger': 'add_note', 'source': 'selecting_action', 'dest': 'making_changes'},
#         {'trigger': 'delete_note', 'source': 'selecting_action', 'dest': 'making_changes'},
#         {'trigger': 'show_list_note', 'source': 'selecting_action', 'dest': 'making_changes'},
#         {'trigger': 'save_note', 'source': 'making_changes', 'dest': 'back_to_menu'},
#         {'trigger': 'go_back', 'source': '*', 'dest': 'start'},
#     ]
#
#     def __init__(self):
#         self.machine = Machine(model=self, states=MyStates.states, transitions=MyStates.transitions, initial='start')

state = {}


@bot.message_handler(func=lambda msg: msg.text == 'Особые возможности' and state[msg.from_user.id] == 'selecting_action' if state[msg.from_user.id] else False)
@printf
async def show_special_keybrd(msg):
    special_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_go_into_mod = telebot.types.KeyboardButton(text="Выбрать мод")
    button_add_key_word = telebot.types.KeyboardButton(text="Добавить ключевое слово")
    button_remind_about_note = telebot.types.KeyboardButton(text="Напомнить о заметке")
    button_not_remind_about_note = telebot.types.KeyboardButton(text="Отменить запоминание о заметке")
    special_keyboard.add(button_go_into_mod, button_add_key_word, button_remind_about_note, button_not_remind_about_note)
    await bot.send_message(msg.chat.id,"a", reply_markup=special_keyboard)


@bot.message_handler(func=lambda msg: msg.text == 'Добавить заметку' and state[msg.from_user.id] == 'selecting_action' if state[msg.from_user.id] else False)
@printf
async def add_note(msg):
    global state
    state[msg.from_user.id] = 'adding_note'
    #user_state.add_note()
    await bot.send_message(msg.chat.id, "Введите заметку" )#if state[msg.from_user.id] else False)
    #state[msg.from_user.id] = 'selecting_action'


@bot.message_handler(func=lambda msg: msg.text == 'Удалить заметку' and state[msg.from_user.id] == 'selecting_action' if state[msg.from_user.id] else False)
@printf
async def delete_note(msg):
    global state
    state[msg.from_user.id] = 'deleting_note'
    #user_state.delete_note()
    await bot.send_message(msg.chat.id, "Выберите заметку")
    state[msg.from_user.id] = 'selecting_action'


@bot.message_handler(func=lambda msg: msg.text == 'Показать список заметок' and state[msg.from_user.id] == 'selecting_action' if state[msg.from_user.id] else False)
@printf
async def show_list_note(msg):
    global state
    state[msg.from_user.id] = 'showing_list_notes'
    #user_state.show_list_note_note()
    await bot.send_message(msg.chat.id, "Список заметок")
    state[msg.from_user.id] = 'selecting_action'


@bot.message_handler(func=lambda msg: msg.text == 'Вернуться в начало'and state[msg.from_user.id] == 'selecting_action' if state[msg.from_user.id] else False)
@printf
async def go_back (msg):
    global state
    state[msg.from_user.id] = 'going_back'
    #user_state.go_back()
    await bot.send_message(msg.chat.id, "/start")
    state[msg.from_user.id] = 'selecting_action'



#adding_notes

@bot.message_handler(func=lambda msg: state[msg.from_user.id] == 'adding_note' if state[msg.from_user.id] else False)
@printf
async def add_note(msg):
    global state
    state[msg.from_user.id] = 'making_note'

    ans_keyboard = telebot.types.InlineKeyboardMarkup()
    button_save = telebot.types.InlineKeyboardButton(text="Сохранить",
                                                     callback_data='save_note')
    button_change = telebot.types.InlineKeyboardButton(text="Изменить",
                                                       callback_data='change_note')
    ans_keyboard.add(button_save, button_change)

    await bot.send_message(msg.chat.id, "Сохранить заметку?", reply_markup=ans_keyboard)# К этому сообщению добавить inline лавиатуру с выбором


@bot.callback_query_handler(func=lambda call: call.data == 'save_note')
@printf
async def save_btn(call):
    global state
    message = call.message
    chat_id = message.chat.id
    state[message.from_user.id] = 'saving_note'
    await bot.send_message(chat_id, f'Данные сохранены')
    state[message.from_user.id] = 'selecting_action'
    print(call)


@bot.callback_query_handler(func=lambda call: call.data == 'change_note')
@printf
async def change_btn(call):
    global state
    message = call.message
    chat_id = message.chat.id
    await bot.send_message(chat_id, f'Введите новую заметку')
    state[call.from_user.id] = 'adding_note'
    print(call)



# @bot.message_handler(func=lambda msg: state[msg.from_user.id] == 'saving_note' if state[msg.from_user.id] else False)
# async def save_note(msg):
#     global state
#     if msg.text == "yes":
#         await bot.send_message(msg.chat.id, "Заметка сохранена")
#     else:
#         await bot.send_message(msg.chat.id, "Заметка не сохранена")
#     state[msg.from_user.id] = 'selecting_action'



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


# state = { }
#
# @bot.message_handlder(func = lambda x: state[user_id]["await_after_button"] if state[user_id] else False)
# def do_something_after_button(msg):
#     global state
#     state[msg.from_user.id]["await_after_button"] = False
#     print("хаха, оно работает")
#
#
# @bot.message_handler(regex=r"Моя кнопка")
# def on_button(msg):
#     global state
#     state[msg.from_user.id]["await_after_button"] = True

import asyncio
asyncio.run(bot.polling())