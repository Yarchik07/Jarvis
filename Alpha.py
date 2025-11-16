import speech_recognition as sr
import os
import time
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

opts = {
    "alias": ("стетхем", "лысый", "брутал", "стэтхэм"), #обращение
    "tbr":("скажи","покажи","расскажи","сколько","произнеси"), 
    "cmds" : {
        "ctime":("который час","сколько времени","текущее время"), #команды
        "music":("включи музыку","вечеринка","танцуем"),
        "mudrost":("расскижи цитату","поведуй мудрость","ты знаешь цитаты")
    }
}
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer, audio): # запись слов
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано:"+ voice)

        if voice.startswith(opts["alias"]):
            cmd = voice

            for x in opts["alias"]:
                cmd = cmd.replace(x, "").strip()
            
            for x in opts["tbr"]:
                cmd = cmd.replace(x, "").strip()

            cmd = recognize_cmd(cmd)
            execute_cmd(cmd["cmd"])

    except sr.UnknownValueError:
        print("[log] Не распознано!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

def recognize_cmd(cmd): #поиск команды
    RC = {"cmd": "", "percent": 0}
    for c,v in opts["cmds"].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC["percent"]:
                RC["cmd"] = c
                RC["percent"] = vrt
    return RC

def execute_cmd(cmd): # преобразовать команду в действие
    if cmd == "ctime":
        now = datetime.datetime.now()

        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == "music":
        os.system("C:\\Alpha\\res\\radio_record.m3u")

    elif cmd == "mudrost":

        speak("Запомни, а то забудешь!")
    
    else:
        print("Команда не распознана!")

r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)
speak_engine = pyttsx3.init()

#voices = speak_engine.getProperty("voices")
#speak_engine.setProperty("voice", voices[4].id)

speak("Добрый день, повелитель, Стетхем к вашим услугам")
speak("Кхм")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1)