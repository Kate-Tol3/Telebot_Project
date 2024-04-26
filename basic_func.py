# import telebot.types
# from telebot.async_telebot import AsyncTeleBot
#
#
# #decorator for printing satus
# def printf(func):
#     async def wrapper(msg):
#         global users
#         await func(msg)
#         print(users)
#     return wrapper
#
#
#
#
# bot = AsyncTeleBot(TOKEN)
#
#
#
# @bot.message_handler(func=lambda msg: users[msg.from_user.id]['status'] == 'adding_note' if users[msg.from_user.id] else False)
# @printf
# async def add_note(msg):
#     global users
#     users[msg.from_user.id]['status'] = 'making_note'
#
#     ans_keyboard = telebot.types.InlineKeyboardMarkup()
#     button_save = telebot.types.InlineKeyboardButton(text="Сохранить",
#                                                      callback_data='save_note')
#     button_change = telebot.types.InlineKeyboardButton(text="Изменить",
#                                                        callback_data='change_note')
#     ans_keyboard.add(button_save, button_change)
#
#     await bot.send_message(msg.chat.id, "Сохранить заметку?", reply_markup=ans_keyboard)# К этому сообщению добавить inline лавиатуру с выбором
#
#
# @bot.callback_query_handler(func=lambda call: call.data == 'save_note')
# @printf
# async def save_btn(call):
#     global users
#     message = call.message
#     chat_id = message.chat.id
#     users[call.from_user.id]['status'] = 'saving_note'
#     await bot.send_message(chat_id, f'Данные сохранены')
#     users[call.from_user.id]['status'] = 'selecting_action'
#     print(call)
#
#
# @bot.callback_query_handler(func=lambda call: call.data == 'change_note')
# @printf
# async def change_btn(call):
#     global users
#     message = call.message
#     chat_id = message.chat.id
#     await bot.send_message(chat_id, f'Введите новую заметку')
#     users[call.from_user.id]['status'] = 'adding_note'
#     print(call)