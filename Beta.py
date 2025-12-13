"""
Преобразование русской речи (с микрофона) в текст.
"""

import vosk
import sys
import sounddevice as sd
import queue
import json

model = vosk.Model("model_small")
samplerate = 16000  
device = 1  # id микрофона (тест проводился еще до момента создания Alpha)

q = queue.Queue()


def q_callback(indata, frames, time, status):
    """
    Callback-функция для обработки аудиоданных с микрофона в реальном времени.

    Вызывается sounddevice при наличии новых аудиоданных.

    :param indata: Буфер с входными аудиоданными (numpy массив)
    :type indata: numpy.ndarray
    :param frames: Количество кадров (сэмплов) в буфере
    :type frames: int
    :param time: Временная метка (CFFI структура)
    :param status: Статус ошибки (если есть), иначе None
    :type status: sounddevice.CallbackFlags или None
    """
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen(callback):
    """
    Основная функция для непрерывного распознавания речи с микрофона.

    Запускает аудиопоток, обрабатывает данные и вызывает callback
    с распознанным текстом.

    :param callback: Функция, которая будет вызвана при успешном распознавании речи
    :type callback: callable[str] -> None
    """
    with sd.RawInputStream(
        samplerate=samplerate,
        blocksize=8000,
        device=device,
        dtype="int16",
        channels=1,
        callback=q_callback
    ):
        rec = vosk.KaldiRecognizer(model, samplerate)

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"])
