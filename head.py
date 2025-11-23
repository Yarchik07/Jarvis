import conf
import Beta
import voice
from fuzzywuzzy import fuzz
import parcing
import random
import datetime
import webbrowser
from num2words import num2words


print(f"{conf.va_intro} начал свою работу . . .")
voice.va_speak("Слушаю тебя, красавчик")

def va_respond(voice: str):
    print (voice)
    if voice.startswith(conf.va_name):
        cmd = recognize_cmd(filter_cmd(voice))
        if cmd["cmd"] not in conf.va_cmd.keys():
            voice.va_speak("Что?")
        else:
            execute_cmd(cmd["cmd"])

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


def execute_cmd(cmd: str):
    if cmd == "help":
        text = "Я умею: . . ."
        text += "подсказать время . . ."
        text += "поведать мудрость . . ."
        text += "открывать браузер"
        text += "узнать погоду"
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
        msedge_path = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe %s'
        webbrowser.get(msedge_path).open("https://www.python.org")
    elif cmd == "weather":
        text = "Данные о температуре, скорости ветра и давлении выведены в терминал"
        print(parcing.t)
        voice.va_speak(text)
# начать прослушивание команд
Beta.va_listen(va_respond)