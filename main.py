import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from decouple import config

def sender(id, text):
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})

def button_send(id,text):
    vk_session.method('messages.send', {'user_id': id, 'message' : text, 'keyboard': str(keyboard.get_keyboard()), 'random_id': 0})

vk_session = vk_api.VkApi(token=config('vk_token'))
longpoll = VkLongPoll(vk_session)
session_api = vk_session.get_api()
keyboard = VkKeyboard(one_time=True)

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me and event.from_user:

            msg = event.text.lower()
            id = event.user_id

            if msg == 'начать':
                user_get = session_api.users.get(user_ids=(id,))
                sender(id, f'Привет {user_get[0]["first_name"]}!\nНапиши "Расписание"')

            if msg == 'расписание':
                keyboard.add_button('привет', color=VkKeyboardColor.PRIMARY)
                button_send(id, 'Выбери дату:')
