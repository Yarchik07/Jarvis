import requests
from bs4 import BeautifulSoup
import re
import webbrowser
from urllib.parse import quote
from PIL import ImageGrab
import datetime
import os
import time

def google():
    # Запрос на гугл
    zapros = #это место для ввода данных(голосового, для тебя ярик)(данные должны быть в виде "")
    #Переводим запрос в ссылку, чтобы браузер распозновал
    zaprosurl = quote(zapros)
    #Ссылка на наш запрос
    googleurl = f"https://www.google.com/search?q={zaprosurl}"
    #Открытие браузера с нашим запросом
    webbrowser.open(googleurl)

def wikipedia():
    # Запрос для википедии
    zapros = #это место для ввода данных(голосового, для тебя ярик)(данные должны быть в виде "")
    # Переводим запрос в ссылку, чтобы браузер распознавал
    zaprosurl = quote(zapros)
    # Ссылка на наш запрос в википедии
    wikurl = f"https://ru.wikipedia.org/wiki/{zaprosurl}"
    # Открытие браузера с нашей страницей википедии
    webbrowser.open(wikurl)

def rutube():
    zapros = #это место для ввода данных(голосового, для тебя ярик)(данные должны быть в виде "")
    zaprosurl = quote(zapros)
    # Прямой URL поиска Rutube
    rutubeurl = f"https://rutube.ru/search/video/?query={zaprosurl}"
    webbrowser.open(rutubeurl)

def screenshot(): # скриншот
    # Создание папки, в случае ее отсутствия
    if not os.path.exists("Скрины"):
        os.makedirs("Скрины")
    # Создание имени скрина
    time = datetime.datetime.now().strftime("%d.%m.%Y в %H:%M")
    file = f"Скрины/Скриншот_{time}.png"
    # Сам скриншот
    screenshot = ImageGrab.grab()
    # Сохранения файла
    screenshot.save(file)

def timer():
    #тут сделать озвучку задайте параметры таймера
    hours = #ввод в виде int
    minutes = #ввод в виде int
    seconds = #ввод в виде int 
    total_seconds = hours * 3600 + minutes * 60 + seconds
    if total_seconds <= 0:
        #тут можно сделать озвучку мол таймер не запущен
        return
    # Обратный отсчет
    while total_seconds > 0:
        time.sleep(1)
        total_seconds -= 1 
    #тут сделать озвучку 2-3 раза мол время вышло 