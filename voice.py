"""Это код для синтеза речи (Text-to-Speech) на русском языке с использованием модели Silero TTS"""
import torch
import sounddevice as sd
import time
language = "ru"
model_id = "ru_v3"
sample_rate = 48000
speaker = "aidar"
put_accent = True
put_yo = True
device = torch.device("cpu")  # cpu или gpu
text = "Здарова"
model, _ = torch.hub.load(repo_or_dir="snakers4/silero-models",
                          model="silero_tts",
                          language=language,
                          speaker=model_id,)
model.to(device)

def va_speak(what: str):
    """Преобразует текст в речь с использованием модели TTS (Text-to-Speech)
    и воспроизводит полученный аудиопоток с небольшой задержкой.
    :param what: Текст для преобразования в речь
    :type what: str
    :raises ImportError: Если отсутствуют модули TTS или звукового воспроизведения
    :raises Exception: Если возникнут ошибки при синтезе или воспроизведении речи"""
    audio = model.apply_tts(text=what + "..",
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo,)
    sd.play(audio, sample_rate * 1.05)
    time.sleep((len(audio) / sample_rate)+0.5)
    sd.stop()