"""
Это код для парсинга информации с разных сайтов.
"""

import requests
from bs4 import BeautifulSoup
import re


def get_weather_by_ip():
    """
    Определяет погоду на основе его IP-адреса, используя сервис определения
    местоположения и Яндекс.Погоду.

    :returns: Кортеж из трех строк: температура, скорость ветра, атмосферное давление
    :rtype: tuple[str, str, str]
    :raises requests.exceptions.RequestException: При ошибках сетевого запроса
    :raises KeyError: Если в ответе API отсутствуют ожидаемые поля
    :raises ValueError: Если не удается распарсить данные о погоде
    :raises Exception: При других ошибках парсинга или обработки данных
    """
    ip_response = requests.get('http://ip-api.com/json/', timeout=5)
    ip_data = ip_response.json()
    city = ip_data['city']
    url = f"https://yandex.ru/pogoda/{city.lower()}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) '
                      'AppleWebKit/605.1.15'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_text = soup.get_text()

    temperatures = re.findall(r'[+-]?\d+°', all_text)
    wind = re.findall(r'\b\d[.,]\d\s*м/с', all_text)
    pressure = re.findall(r'\b\d{3}\s*мм', all_text)

    if temperatures:
        temperatureforaudio = (temperatures[0])
    else:
        temperatureforaudio = ('Температура не определена')

    if wind:
        clean_wind = wind[0].lstrip('0')
        windforaudio = (clean_wind)
    else:
        windforaudio = ('Ветер не определен')

    if pressure:
        pressureforaudio = (pressure[0])
    else:
        pressureforaudio = ('Давление не определено')

    return temperatureforaudio, windforaudio, pressureforaudio


def get_datetime():
    """
    Получает дату и время с внешнего сервера (timeserver.ru) через парсинг
    веб-страницы и извлечения структурированных данных.

    :returns: Строка с отформатированной датой для озвучки (день недели и дата)
    :rtype: str
    :raises requests.exceptions.RequestException: При ошибках сетевого запроса
    :raises AttributeError: Если не найдены ожидаемые HTML-элементы на странице
    :raises Exception: При других ошибках парсинга или обработки данных
    """
    url = "https://www.timeserver.ru/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    hours_elem = soup.find('span', class_='hours')
    minutes_elem = soup.find('span', class_='minutes')

    week_day_elem = soup.find('span', attrs={'x-text': 'city.week_day'})
    date_elem = soup.find('span', attrs={'x-text': 'city.date'})

    timeforaudio = f"{hours_elem.text}:{minutes_elem.text}"
    dateforaudio = f"{week_day_elem.text} {date_elem.text}"

    return dateforaudio


def get_news_from_lenta_working():
    """
    Получает три последние новости с страницы Lenta.ru, фильтруя и очищая
    заголовки для последующего использования.

    :returns: Список из трех строк с заголовками последних новостей
    :rtype: list[str]
    :raises requests.exceptions.RequestException: При ошибках сетевого запроса к Lenta.ru
    :raises AttributeError: Если структура страницы изменилась и элементы не найдены
    :raises Exception: При других ошибках парсинга или обработки данных
    """
    url = "https://lenta.ru"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_links = soup.find_all('a', href=True)

    news_count = 0
    seen_texts = set()
    last_three_news = []

    for link in all_links:
        if news_count >= 3:
            break

        href = link.get('href', '')
        text = link.get_text(strip=True)

        if ('/news/' in href and
            text and len(text) > 20 and len(text) < 120 and
                text not in seen_texts):

            clean_text = re.sub(r'\s*\d{1,2}:\d{2}.*$', '', text)
            clean_text = clean_text.strip()

            if clean_text:
                seen_texts.add(clean_text)
                last_three_news.append(clean_text)
                news_count += 1

    latest_news = last_three_news
    return latest_news


t = get_weather_by_ip()
d = get_datetime()
n = get_news_from_lenta_working()
