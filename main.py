import json

import vk_api
from vk_api.upload import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from decouple import config

from services import get_filename_list, get_schedule_for_teacher, get_schedule_for_group


def sender(id, text):
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


def button_send(id,text):
    vk_session.method('messages.send', {'user_id': id, 'message' : text, 'keyboard': str(keyboard.get_keyboard()), 'random_id': 0})


def clear_keyboard():
    keyboard.lines = [[]]
    keyboard.keyboard['buttons'] = keyboard.lines


def set_value(key, value, id):
    return vk_session.method('storage.set', {'key': key, 'value': value, 'user_id': id})


def get_value(key, id):
    return vk_session.method('storage.get', {'key': key, 'user_id': id})

def send_schedule_teacher(data, id, file_name, find_obj):
    carousel_elements = []
    count = 0
    for _, item in data.items():

        if count == 10:
            break
        count += 1

        subject_name = ' '.join(item['Предмет и преподаватель: '].split()[:-2])
        title = item['Время: ']  # Получаем время из данных
        # Собираем остальные данные в описание
        description = f"{item['Кабинет: ']}\n{subject_name}"[:80]
        carousel_elements.append({
            'title': title,  # Время в заголовке
            'description': description.strip(),  # Описание с остальными данными
            # 'action': {'type': 'open_link', 'link': 'https://vk.com'},  # Действие при нажатии на карточку
            'buttons': [{'action': {'type': 'text', 'label': item['Группа: ']}}]  # Кнопка под карточкой
        })

    carousel_template = {
        'type': 'carousel',
        'elements': carousel_elements
    }

    vk_session.method("messages.send", {
        "user_id": id,
        "message": f"Расписание на {file_name} для {find_obj}",
        "template": json.dumps(carousel_template),  # Преобразуем структуру карусели в JSON-строку
        "random_id": 0
    })


def send_schedule_group(data, id, file_name, find_obj):
    carousel_elements = []
    count = 0
    for _, item in data.items():

        if count == 10:
            break
        count += 1

        if item['Предмет и преподаватель: '] not in ('None', None, '', ' '):

            teacher = item['Предмет и преподаватель: '].split()[-2]
            subject_name = ' '.join(item['Предмет и преподаватель: '].split()[:-2])
            title = item['Время: ']  # Получаем время из данных
            # Собираем остальные данные в описание
            description = f"{item['Кабинет: ']}\n{subject_name}"[:80]
        else:
            teacher = 'Хрр..'
            title = item['Время: ']  # Получаем время из данных
            # Собираем остальные данные в описание
            description = f"Пусто"

        carousel_elements.append({
            'title': title,  # Время в заголовке
            'description': description.strip(),  # Описание с остальными данными
            # 'action': {'type': 'open_link', 'link': 'https://vk.com'},  # Действие при нажатии на карточку
            'buttons': [{'action': {'type': 'text', 'label': teacher}}]  # Кнопка под карточкой
        })

    carousel_template = {
        'type': 'carousel',
        'elements': carousel_elements
    }

    vk_session.method("messages.send", {
        "user_id": id,
        "message": f"Расписание на {file_name} для {find_obj}",
        "template": json.dumps(carousel_template),  # Преобразуем структуру карусели в JSON-строку
        "random_id": 0
    })


vk_session = vk_api.VkApi(token=config('vk_token'))
longpoll = VkBotLongPoll(vk_session, config('bot_id'))
session_api = vk_session.get_api()
keyboard = VkKeyboard() # inline = True для отображения кнопки в сообщении бота, one_time = True скрытия клавиатуры после нажатия

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_user:

            msg = event.object['message']['text'].lower()
            id = event.object['message']['from_id']

            if msg == 'начать':
                if get_value('user_states', id) == 'start':
                    clear_keyboard()
                    keyboard.add_button('Расписание', color=VkKeyboardColor.POSITIVE)
                    user_get = session_api.users.get(user_ids=(id,))
                    button_send(id, f'Привет {user_get[0]["first_name"]}!\nНапиши "Расписание"')
                    continue
                else:
                    sender(id, 'Вы ввели некорректные данные')
                    set_value('user_states', 'start', id)
                    continue

            if msg in ('расписание', 'назад'):
                    set_value('user_states', 'start', id)
                    clear_keyboard()
                    count = 0
                    for i in get_filename_list()[:-1]:
                        keyboard.add_button(i, color=VkKeyboardColor.PRIMARY)
                        count += 1
                        if count == 2:
                            count = 0
                            keyboard.add_line()
                    button_send(id, 'Выбери дату:')
                    continue

            if msg in get_filename_list()[:-1]:
                    set_value('file_name', msg, id)
                    clear_keyboard()
                    keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
                    set_value('user_states', 'enter_date', id)
                    button_send(id, 'Введите номер группы или фамилию преподавателя:')
                    continue

            if msg:
                if get_value('user_states', id) == 'enter_date':
                    if len(msg) <= 4 and msg[:3].isdigit():
                        schedules = get_schedule_for_group(get_value('file_name', id) + '.xlsx', msg)
                        if schedules:
                            send_schedule_group(schedules, id, get_value('file_name', id), msg)
                            sender(id, 'Можете продолжить поиск')
                        else:
                            button_send(id, 'Ничего не найдено')
                        # set_value('user_states', 'start', id)
                        # continue
                    else:
                        file_name = get_value('file_name', id)
                        schedules = get_schedule_for_teacher(file_name+'.xlsx', msg.title())
                        if schedules:
                            send_schedule_teacher(schedules, id, file_name, msg.title())
                            sender(id, 'Можете продолжить поиск')
                            continue
                        else:
                            button_send(id, 'Ничего не найдено')
                        # set_value('user_states', 'start', id)
                        # continue
                else:
                    sender(id, 'Вы ввели некорректные данные')
                    set_value('user_states', 'start', id)
                    continue

    elif event.type == VkBotEventType.MESSAGE_EVENT:
        payload = event.object.payload
        if payload is not None and 'command' in payload:
            if payload['command'] == 'button_pressed':
                # Обрабатываем нажатие на кнопку
                print("Пользователь нажал на кнопку!")

