import requests
from bs4 import BeautifulSoup
import re
import webbrowser
from urllib.parse import quote
from PIL import ImageGrab
import datetime
import os
import time
import head

def google():
    # Запрос на гугл
    zapros = head.va_respond()#это место для ввода данных(голосового, для тебя ярик)(данные должны быть в виде "")
    #Переводим запрос в ссылку, чтобы браузер распозновал
    zaprosurl = quote(zapros)
    #Ссылка на наш запрос
    googleurl = f"https://www.google.com/search?q={zaprosurl}"
    #Открытие браузера с нашим запросом
    w = webbrowser.open(googleurl)
    return w

def wikipedia():
    # Запрос для википедии
#    zapros = #это место для ввода данных(голосового, для тебя ярик)(данные должны быть в виде "")
    # Переводим запрос в ссылку, чтобы браузер распознавал
    zaprosurl = quote(zapros)
    # Ссылка на наш запрос в википедии
    wikurl = f"https://ru.wikipedia.org/wiki/{zaprosurl}"
    # Открытие браузера с нашей страницей википедии
    webbrowser.open(wikurl)

def search_on_rutube(search_query: str):
    """Поиск видео на Rutube"""
    search_term = search_query.replace(" ", "+")
    url = f"https://rutube.ru/search/?q={search_term}"
    
    try:
        msedge_path = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
        webbrowser.get(msedge_path).open(url)
        return f"Открываю результаты поиска для '{search_query}' на Rutube"
    except Exception as e:
        return f"Ошибка при открытии Rutube: {str(e)}"

def screenshot(): # скриншот
    try:
        # Создание папки, в случае ее отсутствия
        if not os.path.exists("Скрины"):
            os.makedirs("Скрины")
        
        # Создание имени скрина
        time = datetime.datetime.now().strftime("%d.%m.%Y в %H:%M")
        file = f"Скрины/Скриншот_{time}.png"
        
        # Сам скриншот
        screenshot = ImageGrab.grab()
        
        # Сохранение файла
        screenshot.save(file)
        
        return f"Скриншот сохранен как {file}"
        
    except Exception as e:
        return f"Ошибка при создании скриншота: {str(e)}"

def timer():
    #тут сделать озвучку задайте параметры таймера
#    hours = #ввод в виде int
#    minutes = #ввод в виде int
#    seconds = #ввод в виде int 
    total_seconds = hours * 3600 + minutes * 60 + seconds
    if total_seconds <= 0:
        #тут можно сделать озвучку мол таймер не запущен
        return
    # Обратный отсчет
    while total_seconds > 0:
        time.sleep(1)
        total_seconds -= 1 
    #тут сделать озвучку 2-3 раза мол время вышло 
r = search_on_rutube()