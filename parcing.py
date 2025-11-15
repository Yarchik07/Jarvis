import requests
from bs4 import BeautifulSoup
import re

def get_weather_by_ip():
    ip_response = requests.get('http://ip-api.com/json/', timeout=5)
    ip_data = ip_response.json()
    city = ip_data['city']
    url = f"https://yandex.ru/pogoda/{city.lower()}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
    }
    # Отправляем запрос на сайт и получаем ответ
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_text = soup.get_text()
    # Поиск значений
    temperatures = re.findall(r'[+-]?\d+°', all_text)
    wind = re.findall(r'\d+[.,]?\d*\s*м/с', all_text)
    pressure = re.findall(r'\d+\s*мм', all_text)
    # Температура, ветер, давление
    if temperatures:
        temperatureforaudio = (f"Текущая температура: {temperatures[0]}")
    else:
        notemperature = ('Температура не определена')
    if wind:
        windforaudio = (f"Ветер: {wind[0]}")
    else:
        nowind = ('Ветер не определен')
    if pressure:
        pressureforaudio = (f"Давление: {pressure[0]}")
    else:
        nopressure = ('Давление не определено')
get_weather_by_ip()