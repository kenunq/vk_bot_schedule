import os
import shutil
from urllib.parse import urlencode
from urllib.request import urlopen
from zipfile import ZipFile

import requests
from openpyxl import load_workbook


def get_schedule_for_teacher(filename, find):
    """Функция для создания JSON объекта путем парсинга excel таблицы"""

    book = load_workbook(filename=f'{os.getcwd()}/static/schedule/Pасписание/' + filename)
    ws = book.active
    # namep = (os.path.basename(filename))
    masstime = []
    masssur = []
    massgr = []
    masskb = []
    find = find
    for i in range(1, 18):
        for j in range(2, 34):
            lol = ws.cell(row=j, column=i).value
            if lol is None:
                lol = '@'
            if isinstance(lol, str):
                if find in lol:
                    if 3 <= j <= 8:
                        qaz = ws.cell(row=2, column=i).value
                    elif 10 <= j <= 15:
                        qaz = ws.cell(row=9, column=i).value
                    elif 17 <= j <= 22:
                        qaz = ws.cell(row=16, column=i).value
                    elif 24 <= j <= 29:
                        qaz = ws.cell(row=23, column=i).value
                    masstime.insert(0, ws.cell(row=j, column=2).value)
                    masssur.insert(0, lol.strip().replace('\n', ' '))
                    massgr.insert(0, qaz)
                    masskb.insert(0, ws.cell(row=j, column=i + 1).value)

    lenght = len(masstime)

    pre_result = {}
    #заполняем словарь данными
    for i in range(lenght):
        pre_result[i] = {'Время: ': str(masstime[i]), 'Предмет и преподаватель: ': str(masssur[i]),
                         'Группа: ': str(massgr[i]), 'Кабинет: ': str(masskb[i])}

    #сортируем спарсенные данные по времени
    sotr_dict_key = sorted(pre_result, key=lambda x: int(pre_result[x]['Время: '].split('.')[0]))

    #перезаписываем отсортированные данные в словарь
    result = {}
    for i in range(lenght):
        result[i] = {'Время: ': str(masstime[sotr_dict_key[i]]), 'Предмет и преподаватель: ': str(masssur[sotr_dict_key[i]]),
                     'Группа: ': str(massgr[sotr_dict_key[i]]), 'Кабинет: ': str(masskb[sotr_dict_key[i]])}

    return result



def download_exel(url: str) -> None:
    """Функция для скачивания excel таблиц с расписанием"""

    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    public_key = url

    # Получаем загрузочную ссылку
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']
    to_url = os.path.dirname(os.path.abspath(__file__))

    # записываем в переменную бинарные данные
    filedata = urlopen(download_url)
    datatowrite = filedata.read()

    # переводим бинарные данные в зип файл
    with open(to_url + '/static/schedule/qwe.zip', 'wb') as f:
        f.write(datatowrite)

    # разархивируем архив
    with ZipFile(to_url + '/static/schedule/qwe.zip', 'r') as zip_file:
        zip_file.extractall(to_url + '/static/schedule')
        os.remove(to_url + '/static/schedule/qwe.zip')

    file_list = os.walk(os.getcwd() + '/static/schedule/Pасписание')
    for root, dirs, files in file_list:
        for file in files:
            file_path = os.path.join(root, file)
            new_file_name = file[:-5].rstrip() + '.xlsx'
            new_file_path = os.path.join(root, new_file_name)
            os.rename(file_path, new_file_path)


def get_filename_list() -> list[str]:
    """Функция для получения доступных расписаний занятий"""
    
    list_name = os.listdir(os.getcwd() + '/static/schedule/Pасписание')

    result = []
    for i in list_name:
        result.append(i.replace('.xlsx', '').strip())

    return result


def del_from_folder():
    """Функция для удаления папки с расписаниями"""

    try:
        list = os.listdir(os.getcwd() + "/static/schedule/Pасписание")
        if list:
            shutil.rmtree(os.getcwd() + "/static/schedule/Pасписание")
    except:
        print("Folder not found")


download_exel('https://disk.yandex.ru/d/VNdnX6hmveqJuw')
