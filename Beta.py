import vosk
import sys
import sounddevice as sd
import queue

model = vosk.Model("model_small")
samplerate = 16000 #рекомендуют от 8 до 16Hz
device = 1 #id микрофона (тест проводился еще до момента создания Alpha)

q = queue.Queue()

def callblack(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype="int16", channels=1, callback=callblack):
    rec = vosk.KaldiRecognizer(model, samplerate)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())