"""
Главный файл, после запуска которого запускается Джарвис.
"""

import conf
import Beta
import voice
import parcing
import random
import datetime
import webbrowser
import os
import time
import sound

from fuzzywuzzy import fuzz
from num2words import num2words
from PIL import ImageGrab
from urllib.parse import quote


print(f"{conf.va_intro} начал свою работу . . .")


def va_respond(voice: str):
    """
    Основная функция-обработчик голосовых команд ассистента.

    Анализирует распознанную речь, определяет команды и выполняет
    соответствующие действия.

    :param voice: Распознанный текст голосовой команды
    :type voice: str
    :raises KeyError: Если команда не найдена в конфигурации
    :raises Exception: При ошибках выполнения команды
    """
    print(voice)

    if voice.startswith(conf.va_name):
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd["cmd"] not in conf.va_cmd.keys():
            voice.va_speak("Что?")
        else:
            # Передаем оригинальный текст команды
            execute_cmd(cmd["cmd"], voice)


def filter_cmd(raw_voice: str):
    """
    Очищает распознанную голосовую команду от имени ассистента и стоп-слов.

    Подготавливает текст для дальнейшего анализа и распознавания команд.

    :param raw_voice: Исходный распознанный текст голосовой команды
    :type raw_voice: str
    :returns: Очищенная команда без обращения и лишних слов
    :rtype: str
    """
    cmd = raw_voice

    for x in conf.va_name:
        cmd = cmd.replace(x, "").strip()

    for x in conf.va_tbr:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    """
    Определяет наиболее вероятную команду на основе сравнения текста
    с эталонными шаблонами команд.

    :param cmd: Очищенный текст команды (после filter_cmd)
    :type cmd: str
    :returns: Словарь с идентификатором команды и процентом совпадения
    :rtype: dict[str, Union[str, int]]
    """
    rc = {"cmd": "", "percent": 0}

    for c, v in conf.va_cmd.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc["percent"]:
                rc["cmd"] = c
                rc["percent"] = vrt

    return rc


def execute_cmd(cmd: str, voice_text: str = ""):
    """
    Выполняет конкретную команду голосового ассистента на основе
    распознанного идентификатора.

    Обрабатывает различные категории команд и взаимодействует с пользователем.

    :param cmd: Идентификатор команды для выполнения
    :type cmd: str
    :param voice_text: Оригинальный текст голосовой команды
                      (для извлечения параметров)
    :type voice_text: str
    :raises ValueError: При некорректном вводе числовых параметров
    :raises Exception: При ошибках выполнения конкретных команд
    """
    if cmd == "help":
        text = "Я умею: . . ."
        text += "подсказать время и дату"
        text += "поведать мудрость . . ."
        text += "узнать погоду и новости"
        text += "искать на рутубе, в википедии и гугле"
        text += "настраивать громкость, выключать компьютер"
        text += "устанавливать таймер"
        text += "делать скриншот"
        text += "озвучить содержимое файла а также открыть его и создать новый"
        voice.va_speak(text)

    elif cmd == "ctime":
        now = datetime.datetime.now()
        today_date = parcing.d
        text = (
            "Сей+час " + num2words(now.hour, lang="ru") + ":" +
            num2words(now.minute, lang="ru") +
            "      полная дата выведена в терминал"
        )
        print(today_date)
        voice.va_speak(text)

    elif cmd == "mudrost":
        mudrost = [
            "Сила – не в бабках. Ведь бабки – уже старые.",
            "В жизни всегда есть две дороги: одна — первая, а другая — вторая.",
            "Делай, как надо. Как не надо, не делай.",
        ]
        voice.va_speak(random.choice(mudrost))

    elif cmd == "weather":
        text = (
            "Данные о температуре, скорости ветра и давлении "
            "выведены в терминал"
        )
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
        google_keywords = [
            "джарвис", "гугл", "гугл запрос", "найти в гугл"
        ]

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

    elif cmd == "off":
        off_system()


def off_system():
    """
    Выполняет команду выключения системы через 10 секунд,
    предварительно уведомляя пользователя голосовым сообщением.

    :returns: None
    :type: None
    :raises OSError: Если возникнут проблемы с выполнением системной команды.
    :raises Exception: Если возникнут проблемы с голосовым синтезом.
    """
    voice.va_speak("Система отключится через десять секунд")
    os.system("shutdown /s /t 10")


def quick_txt(name, content):
    """
    Быстро создает текстовый файл в папке Documents пользователя
    с заданным именем и содержимым.

    :param name: Имя файла
    :type name: str
    :param content: Cодержимое файла
    :type content: str
    :returns: Полный путь к созданному файлу
    :rtype: str
    :raises OSError: Если возникнут проблемы с созданием файла
                     или доступом к папке Documents
    :raises UnicodeEncodeError: Если возникнут проблемы с кодировкой текста в UTF-8
    """
    path = os.path.join(
        os.path.expanduser("~"),
        "Documents",
        name + '.txt'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    return path


def open_file_or_folder(name):
    """
    Поиск файла или папки по имени на нескольких дисках
    и открытие файла средствами операционной системы.

    :param name: Имя файла или папки
    :type name: str
    :returns: True, если файл или папка найдены и успешно открыты, иначе False
    :rtype: bool
    :raises OSError: Если возникнут проблемы с доступом к дискам или файловой системе
    :raises PermissionError: Если нет доступа к некоторым директориям
    :raises Exception: Если возникнут другие ошибки при открытии файла
    """
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
    """
    Осуществляет поиск файлов (.txt) по имени на нескольких дисках,
    читает их содержимое и воспроизводит голосом.

    :param name: Часть имени файла для поиска (без расширения .txt)
    :type name: str
    :returns: None
    :rtype: None
    :raises OSError: Если возникнут проблемы с доступом к дискам или файловой системе
    :raises FileNotFoundError: Если найденный файл не существует
    :raises PermissionError: Если нет доступа к файлу
    :raises UnicodeDecodeError: Если возникнут проблемы с декодированием файла в UTF-8
    :raises Exception: Если возникнут ошибки при чтении файла или голосовом воспроизведении
    """
    drives = ['C:', 'D:', 'E:']

    for drive in drives:
        for root, dirs, files in os.walk(drive + '\\'):
            for file in files:
                # содержит ли файл то что мы сказали и приписывает .txt
                if name in file and file.endswith('.txt'):
                    path = os.path.join(root, file)

                    with open(path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        print(text)
                        voice.va_speak(text)


def timer(a):
    """
    Запускает таймер по минутам с оповещением о запуске и завершении.

    :param a: Количество минут для таймера
    :type a: int
    :returns: None
    :rtype: None
    :raises ValueError: Если переданный параметр не является положительным числом
    :raises Exception: Если возникнут ошибки при голосовом воспроизведении
    :raises ImportError: Если модуль num2words не установлен
    """
    minutes = a  
    total_seconds = minutes * 60

    if total_seconds <= 0:
        voice.va_speak("Таймер не запущен")
        return

    text = "Осталось " + num2words(total_seconds, lang="ru") + "секунд"
    voice.va_speak(text)

    while total_seconds > 0:
        time.sleep(1)
        total_seconds -= 1

        if total_seconds == 0:
            voice.va_speak("Таймер истёк")


def google(a):
    """
    Выполняет поиск в Google по заданному запросу через открытие браузера
    с автоматически сформированной поисковой ссылкой.

    :param a: Поисковый запрос
    :type a: str
    :returns: None
    :rtype: bool
    :raises webbrowser.Error: Если возникнут проблемы с открытием браузера
    :raises ImportError: Если модули urllib.parse или webbrowser не доступны
    """
    zapros = a

    # Переводим запрос в ссылку, чтобы браузер распознавал
    zaprosurl = quote(zapros)

    # Ссылка на наш запрос
    googleurl = f"https://www.google.com/search?q={zaprosurl}"

    # Открытие браузера с нашим запросом
    webbrowser.open(googleurl)


def wikipedia(a):
    """
    Открывает статью в Википедии по запросу через автоматическое
    открытие браузера по ссылке.

    :param a: Поисковый запрос для Википедии
    :type a: str
    :returns: None
    :rtype: None
    :raises webbrowser.Error: Если возникнут проблемы с открытием браузера
    :raises ImportError: Если модуль urllib.parse или webbrowser не доступен
    """
    zapros = a

    # Переводим запрос в ссылку, чтобы браузер распознавал
    zaprosurl = quote(zapros)

    # Ссылка на наш запрос в википедии
    wikurl = f"https://ru.wikipedia.org/wiki/{zaprosurl}"

    # Открытие браузера с нашей страницей википедии
    webbrowser.open(wikurl)


def rutube(a):
    """
    Выполняет поиск видео на Rutube по запросу через открытие браузера по ссылке.

    :param a: Поисковый запрос
    :type a: str
    :returns: None
    :rtype: None
    :raises webbrowser.Error: Если возникнут проблемы с открытием браузера
    :raises ImportError: Если модуль urllib.parse или webbrowser не доступен
    """
    zapros = a
    zaprosurl = quote(zapros)

    # Прямой URL поиска Rutube
    rutubeurl = f"https://rutube.ru/search/video/?query={zaprosurl}"

    webbrowser.open(rutubeurl)


def screenshot():
    """
    Создает скриншот экрана, сохраняет его на рабочем столе и
    открывает сохраненный файл.

    :returns: Сообщение о результате операции или сообщение об ошибке
    :rtype: str
    :raises ImportError: Если отсутствует модуль PIL (Pillow)
    :raises OSError: Если возникнут проблемы с доступом к файловой системе
    :raises PermissionError: Если нет прав на создание папки или сохранение файла
    :raises Exception: Если возникнут другие ошибки при создании скриншота
    """
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        screens_dir = os.path.join(desktop, "Скрины")

        if not os.path.exists(screens_dir):
            os.makedirs(screens_dir)
            print(f"Создана папка: {screens_dir}")

        current_time = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
        file = os.path.join(screens_dir, f"Скриншот_{current_time}.png")

        print(f"файл: {file}")

        # Делаем скриншот
        screenshot_image = ImageGrab.grab()
        print(f"Скриншот сделан, размер: {screenshot_image.size}")

        # Сохраняем с указанием формата
        screenshot_image.save(file, "PNG")

        # Проверяем результат
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            print(f"Файл: {file}")
            print(f"Размер: {file_size} байт")

            # Автоматически открываем файл
            os.startfile(file)
            return "Скриншот сохранен и открыт"

    except Exception:
        print("Ошибка")


# начать прослушивание команд
#Beta.va_listen(va_respond)
