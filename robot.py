import telebot
from telebot import types
from pprint import pprint
import configparser

from statistic import get_stats, show_users, tag_all, get_data

config = configparser.ConfigParser()
config.read("config.ini")

token = config['Telegram']['token']
bot = telebot.TeleBot(token)

keyboard = types.InlineKeyboardMarkup()
key_show_user = types.InlineKeyboardButton(text='Список участников', callback_data='show_user')
key_tag_all = types.InlineKeyboardButton(text='Всеобщий тэг', callback_data='tag_all')
key_show_stats = types.InlineKeyboardButton(text='Показать статистику', callback_data='show_stats')
key_karma = types.InlineKeyboardButton(text='Управление кармой', callback_data='karma')
keyboard.add(key_show_user)
keyboard.add(key_tag_all)
keyboard.add(key_show_stats)
keyboard.add(key_karma)

keyboard_karma = types.InlineKeyboardMarkup()
key_increase = types.InlineKeyboardButton(text='Повысить карму', callback_data='increase_karma')
key_decrease = types.InlineKeyboardButton(text='Понизить карму', callback_data='decrease_karma')
key_return = types.InlineKeyboardButton(text='Вернуться в основное меню', callback_data='return')
keyboard_karma.add(key_increase)
keyboard_karma.add(key_decrease)
keyboard_karma.add(key_return)

def get_user_keybord(direction):
    direction_dict = {
        'increase': 'повышена',
        'decrease': 'понижена',
    }
    keybord = types.InlineKeyboardMarkup()
    call_dict = {}
    user_list = show_users(print)
    for user in user_list:
        keybord.add(types.InlineKeyboardButton(text=user['name'], callback_data=direction + str(user['id'])))
        call_dict[direction + str(user['id'])] = lambda call: bot.send_message(
            call.message.chat.id, f"Карма игрока {user['name']} {direction_dict[direction]}", reply_markup=keyboard_karma)
    key_return = types.InlineKeyboardButton(text='Вернуться к управлению кармой', callback_data='karma')
    keybord.add(key_return)
    return keybord, call_dict

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # print(message)
    
    if message.text == "/stats":
        # bot.send_message(message.chat.id, "Выполняю расчет статистики")
        # get_stats(lambda x: bot.send_message(message.chat.id, x))
        bot.send_message(message.chat.id, 'Юра, прекрати!')
        # get_stats(print)
    elif message.text == "/users":
        show_users(lambda x: bot.send_message(message.chat.id, x))
    elif message.text == "/tag_all":
        tag_all(lambda x: bot.send_message(message.chat.id, x))
    elif message.text == "/help":
        bot.send_message(message.chat.id, 'Список доступных действий', reply_markup=keyboard)

                        #  """
                        #     Список команд:
                        #     \r\nДля получения отчета по статистике напиши /stats;
                        #     \r\nДля получения списка участников напиши /users;
                        #     \r\nДля массового тега напиши /tag_all;
                        #     """
                         

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    increase_keyboard, increase_dict = get_user_keybord('increase')
    decrease_keyboard, decrease_dict = get_user_keybord('decrease')
    
    call_dict ={
        'show_user': lambda call: show_users(lambda x: bot.send_message(call.message.chat.id, x, reply_markup=keyboard)),
        'tag_all':  lambda call: tag_all(lambda x: bot.send_message(call.message.chat.id, x, reply_markup=keyboard)),
        'show_stats': lambda call: get_stats(lambda x: bot.send_message(call.message.chat.id, x, reply_markup=keyboard, parse_mode='HTML')),
        'karma': lambda call: bot.send_message(call.message.chat.id, 'Управление кармой', reply_markup=keyboard_karma),
        'return': lambda call: bot.send_message(call.message.chat.id, 'Список доступных действий', reply_markup=keyboard),
        'increase_karma': lambda call: bot.send_message(call.message.chat.id, 'Повысить карму', reply_markup=increase_keyboard),
        'decrease_karma': lambda call: bot.send_message(call.message.chat.id, 'Понизить карму', reply_markup=decrease_keyboard),
    }
    
    call_dict.update(increase_dict)
    call_dict.update(decrease_dict)
    # pprint(call_dict)
    call_dict[call.data](call)
        
bot.polling(none_stop=True, interval=0)
