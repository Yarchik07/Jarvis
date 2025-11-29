import conf
import Beta
import voice
from fuzzywuzzy import fuzz
import parcing
import random
import datetime
import webbrowser
from num2words import num2words
import timerwikrutubegooglescreen
from PIL import ImageGrab
import os


print(f"{conf.va_intro} начал свою работу . . .")
voice.va_speak("Слушаю тебя, красавчик")

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
    elif cmd == "open_browser":
        msedge_path = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        webbrowser.get(msedge_path).open("https://www.python.org")
    elif cmd == "weather":
        text = "Данные о температуре, скорости ветра и давлении выведены в терминал"
        print(parcing.t)
        voice.va_speak(text)
    elif cmd == "news":
        text = str(parcing.n)
        print(parcing.n)
        voice.va_speak(text)
    elif cmd == "google_zap":
        text = str(timerwikrutubegooglescreen.g)
        voice.va_speak(text)
    elif cmd == "rutube":
        # Извлекаем поисковый запрос из команды
        filtered_cmd = filter_cmd(voice_text) if voice_text else ""
        
        if filtered_cmd:
            # Убираем ключевые слова rutube из запроса
            search_query = filtered_cmd
            rutube_keywords = ["rutube", "рутьюб", "найди", "поиск", "открой", "рут"]
            for keyword in rutube_keywords:
                search_query = search_query.replace(keyword, "").strip()
            
            if search_query:
                result = timerwikrutubegooglescreen.r
                voice.va_speak(result)
            else:
                voice.va_speak("Что именно вы хотите найти на Rutube?")
        else:
            # Если просто "открой rutube" без запроса - открываем главную страницу
            webbrowser.get(msedge_path).open("https://rutube.ru")
            voice.va_speak("Открываю главную страницу Rutube")
    elif cmd == "screenshot":
        result = screenshot()
        voice.va_speak(result)
def screenshot(): 
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        screens_dir = os.path.join(desktop, "Скрины")
        
        if not os.path.exists(screens_dir):
            os.makedirs(screens_dir)
            print(f"📁 Создана папка: {screens_dir}")
        
        time = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")  # Без двоеточий
        file = os.path.join(screens_dir, f"Скриншот_{time}.png")
        
        print(f"🎯 Целевой файл: {file}")
        
        # Делаем скриншот
        screenshot = ImageGrab.grab()
        print(f"📸 Скриншот сделан, размер: {screenshot.size}")
        
        # Сохраняем с явным указанием формата
        screenshot.save(file, "PNG")
        print("💾 Сохранение завершено")
        
        # Проверяем результат
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            print(f"✅ УСПЕХ! Файл: {file}")
            print(f"📊 Размер: {file_size} байт")
            
            # Автоматически открываем файл
            os.startfile(file)
            return f"Скриншот сохранен и открыт"
        else:
            print("❌ Файл не найден после сохранения!")
            return "Ошибка: файл не создан"
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        return f"Ошибка: {str(e)}"
# начать прослушивание команд
Beta.va_listen(va_respond)