<h1 align="center"><p>ВК Бот расписания </p></h1>

<br/>

![Python Version](https://img.shields.io/badge/Python-3.11-blue)
![Code Style](https://img.shields.io/badge/code_style-pep8-orange)
___



## Запуск проекта на локальном компьютере

**1. Скачайте проект на локальный компьютер**
```
git clone https://github.com/kenunq/vk_bot_schedule.git
```

**2. Создайте виртуальное окружение**
```
python -m venv venv
```

**3. Активируйте виртуальное окружение**

*macOS*
```
. venv/bin/activate
```

*linux*
```
source venv/bin/activate
```

*windows*
```
venv\Scripts\activate
```

**4. Обновите пакетный установщик pip**
```
python -m pip install --upgrade pip
```

**5. Зайдите в рабочую директорию проекта(все дальнейшие действия будут осуществляется в ней)**
```
cd vk_bot_schedule/
```

**6. Установите зависимости необходимые для запуска проекта**
```
pip install -r requirements.txt
```

**7. Создайте файл `.env` и заполните его по примеру**
```
vk_token = 'vk_token'
bot_id = 'bot_id'
```

**8.Запустите бота**
```
python main.py
```

**Для остановки сервера нажмите `CTRL+C` или `CMD+C`(для mac)**
