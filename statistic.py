import json
from collections import Counter, OrderedDict
from pprint import pprint

from parser import get_files, get_users, get_messages

def get_data(path):
    with open(path) as file:
        return json.load(file)
    
def show_users(callback):
    get_users(print)
    user_data = get_data('channel_users.json')
    user_list = [{'name': f"{user['first_name']} {user['last_name'] or ''}- [ {user['user'] or ''} ]", 'id': user['id']} 
                  for user in user_data]
    callback('Список участников:\n\n' + '\n'.join([user['name'] for user in user_list]))
    return user_list

def tag_all(callback):
    get_users(print)
    user_data = get_data('channel_users.json')
    callback(', '.join([f"@{user['user'] or user['first_name']}" for user in user_data]))

def get_stats(callback):
    # callback('Выполняю расчет статистики')
    get_files(callback)
    message_dict = Counter()
    user_dict = {}
    user_data = get_data('channel_users.json')
    message_data = get_data('channel_messages.json')

    for user in user_data:
        user_dict[user['id']] = f"{user['first_name']} {user['last_name'] or ''}- [ {user['user'] or ''} ]"
    
    total_count = len(message_data)
    callback(f'Всего сообщений: {total_count}')
    for msg in message_data:
        message_dict[msg['from_id']] += 1

    result_dict = {}
    for user_id, user in user_dict.items():
        result_dict[user] = message_dict.get(user_id, 0)

    callback('\n'.join([f'{number + 1}. {user} - <b>{count} шт. - {round(100 * count / total_count, 2)}%</b>' 
                    for number, (user, count) in enumerate(sorted(result_dict.items(), key=lambda x: x[1], reverse=True))]))


