import conf
import Beta
import voice
from fuzzywuzzy import fuzz
import parcing
import random
import datetime
import webbrowser
from num2words import num2words
from PIL import ImageGrab
import os
from urllib.parse import quote
import time
import sound



print(f"{conf.va_intro} начал свою работу . . .")

def va_respond(voice: str):
    print(voice)
    if voice.startswith(conf.va_name):
        cmd = recognize_cmd(filter_cmd(voice))
        if cmd["cmd"] not in conf.va_cmd.keys():
            voice.va_speak("Что?")
        else:
            execute_cmd(cmd["cmd"], voice)  # Передаем оригинальный текст команды

def filter_cmd(raw_voice: str):
    cmd = raw_voice
    for x in conf.va_name:
        cmd = cmd.replace(x, "").strip()
    for x in conf.va_tbr:
        cmd = cmd.replace(x, "").strip()
    return cmd


def recognize_cmd(cmd: str):
    rc = {"cmd": "", "percent": 0}
    for c, v in conf.va_cmd.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc["percent"]:
                rc["cmd"] = c
                rc["percent"] = vrt
    return rc


def execute_cmd(cmd: str, voice_text: str = ""):
    if cmd == "help":
        text = "Я умею: . . ."
        text += "подсказать время . . ."
        text += "поведать мудрость . . ."
        text += "открывать браузер"
        text += "узнать погоду"
        text += "искать на рутубе"
        voice.va_speak(text)
        pass
    elif cmd == "ctime":
         now = datetime.datetime.now()
         today_date = parcing.d
         text = "Сей+час " + num2words(now.hour, lang="ru") + ":" + num2words(now.minute, lang="ru") + "      полная дата выведена в терминал"
         print(today_date)
         voice.va_speak(text)
    elif cmd == "mudrost":
        mudrost = ["Сила – не в бабках. Ведь бабки – уже старые.",
                   "В жизни всегда есть две дороги: одна — первая, а другая — вторая.",
                   "Делай, как надо. Как не надо, не делай."]
        voice.va_speak(random.choice(mudrost))
    elif cmd == "weather":
        text = "Данные о температуре, скорости ветра и давлении выведены в терминал"
        print(parcing.t)
        voice.va_speak(text)
    elif cmd == "news":
        text = str(parcing.n)
        print(parcing.n)
        voice.va_speak(text)
    elif cmd == "rutube":
        voice.va_speak("Открываю рутьюб")
        f = str(voice_text)
        rutube_keywords = ["джарвис", "рут", "найди видео о"]
        for keyword in rutube_keywords:
            f = f.replace(keyword, "").strip()
        rutube(f)  
    elif cmd == "screenshot":
        result = screenshot()
        voice.va_speak(result)
    elif cmd == "wiki":
        voice.va_speak("Открываю википедию")
        f = str(voice_text)
        wiki_keywords = ["джарвис", "вики", "найди информацию о"]
        for keyword in wiki_keywords:
            f = f.replace(keyword, "").strip()
        wikipedia(f)
    elif cmd == "google":
        voice.va_speak("Открываю гугл")
        f = str(voice_text)
        google_keywords = ["джарвис", "гугл","гугл запрос", "найти в гугл"]
        for keyword in google_keywords:
            f = f.replace(keyword, "").strip()
        google(f)
    elif cmd == "timer":
        voice.va_speak("На сколько минут засечь время?")
        f = int(input())
        timer(f)
    elif cmd == "read":
        voice.va_speak("Назовите файл для чтения")
        f = str(input())
        read_txt_files(f)
    elif cmd == "open_file":
        voice.va_speak("Назовите файл для открытия")
        f = str(input())
        open_file_or_folder(f)
    elif cmd == "creat_file":
        voice.va_speak("Введите название файла")
        name = str(input())
        voice.va_speak("Введите содержимое файла")
        content = str(input())
        quick_txt(name, content)
    elif cmd == "volume":
        voice.va_speak("Назовите какое значение громкости нужно установить")
        f = int(input())
        sound.Sound.volume_set(f)

def quick_txt(name, content):#сюда голосовой ввод
    path = os.path.join(os.path.expanduser("~"), "Documents", name + '.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def open_file_or_folder(name):
    # Диски для поиска
    drives = ['C:', 'D:', 'E:', 'F:', 'G:']
    
    for drive in drives:
        for root, dirs, files in os.walk(drive + '\\'):
            # Ищем папку
            if name in dirs:
                path = os.path.join(root, name)
                os.startfile(path)
                return True
            
            # Ищем файл
            for file in files:
                if name in file:
                    path = os.path.join(root, file)
                    os.startfile(path)
                    return True
    
    return False

def read_txt_files(name):
    drives = ['C:', 'D:', 'E:']
    
    for drive in drives:
        for root, dirs, files in os.walk(drive + '\\'):
            for file in files:
                #содержит ли файл то что мы сказали и приписывает .txt
                if name in file and file.endswith('.txt'):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        print(text)
                        voice.va_speak(text)
                    
                #функция работает по принципу поиска файлов

def timer(a):
    #тут сделать озвучку задайте параметры таймера
    minutes = a #ввод в виде int 
    total_seconds = minutes * 60
    if total_seconds <= 0:
        voice.va_speak("Таймер не запущен")
        #тут можно сделать озвучку мол таймер не запущен
        return
    # Обратный отсчет
    text = "Осталось " + num2words(total_seconds, lang="ru") + "секунд"
    voice.va_speak(text)
    while total_seconds > 0:
        time.sleep(1)
        total_seconds -= 1 
        if total_seconds == 0:
            voice.va_speak("Таймер истёк")

def google(a):
    # Запрос на гугл
    zapros = a #это место для ввода данных(голосового, для тебя ярик)(данные должны быть в виде "")
    #Переводим запрос в ссылку, чтобы браузер распозновал
    zaprosurl = quote(zapros)
    #Ссылка на наш запрос
    googleurl = f"https://www.google.com/search?q={zaprosurl}"
    #Открытие браузера с нашим запросом
    w = webbrowser.open(googleurl)

def wikipedia(a):
    # Запрос для википедии
    zapros = a #это место для ввода данных(голосового, для тебя ярик)(данные должны быть в виде "")
    # Переводим запрос в ссылку, чтобы браузер распознавал
    zaprosurl = quote(zapros)
    # Ссылка на наш запрос в википедии
    wikurl = f"https://ru.wikipedia.org/wiki/{zaprosurl}"
    # Открытие браузера с нашей страницей википедии
    webbrowser.open(wikurl)

def rutube(a):
    zapros = a #это место для ввода данных(голосового, для тебя ярик)(данные должны быть в виде "")
    zaprosurl = quote(zapros)
    # Прямой URL поиска Rutube
    rutubeurl = f"https://rutube.ru/search/video/?query={zaprosurl}"
    webbrowser.open(rutubeurl)

def screenshot(): 
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        screens_dir = os.path.join(desktop, "Скрины")
        
        if not os.path.exists(screens_dir):
            os.makedirs(screens_dir)
            print(f"Создана папка: {screens_dir}")
        
        time = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")  # Без двоеточий
        file = os.path.join(screens_dir, f"Скриншот_{time}.png")
        
        print(f"файл: {file}")
        
        # Делаем скриншот
        screenshot = ImageGrab.grab()
        print(f"Скриншот сделан, размер: {screenshot.size}")
        
        # Сохраняем с явным указанием формата
        screenshot.save(file, "PNG")
        print("💾 Сохранение завершено")
        
        # Проверяем результат
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            print(f"Файл: {file}")
            print(f"Размер: {file_size} байт")
            
            # Автоматически открываем файл
            os.startfile(file)
            return f"Скриншот сохранен и открыт"
    except:
        print("Ошибка")

# начать прослушивание команд
Beta.va_listen(va_respond)