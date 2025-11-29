import requests
from bs4 import BeautifulSoup
import re
from num2words import num2words

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
    

    temperatures = re.findall(r'[+-]?\d+°', all_text)
    wind = re.findall(r'\b\d[.,]\d\s*м/с', all_text)
    pressure = re.findall(r'\b\d{3}\s*мм', all_text)

    # Температура, ветер, давление для озвучки
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
    url = "https://www.timeserver.ru/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Парсим время
    hours_elem = soup.find('span', class_='hours')
    minutes_elem = soup.find('span', class_='minutes') 
    
    # Парсим дату
    week_day_elem = soup.find('span', attrs={'x-text': 'city.week_day'})
    date_elem = soup.find('span', attrs={'x-text': 'city.date'})
    
    timeforaudio = f"{hours_elem.text}:{minutes_elem.text}"#время для озвучки
    dateforaudio = f"{week_day_elem.text} {date_elem.text}"#дата для озвучки
    return dateforaudio


def get_news_from_lenta_working():
    url = "https://lenta.ru"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Поиск всех ссылок на новости.
    all_links = soup.find_all('a', href=True)
    
    news_count = 0
    seen_texts = set()
    last_three_news = []
    
    for link in all_links:
        if news_count >= 3:
            break
            
        href = link.get('href', '')
        text = link.get_text(strip=True)
        
        # Фильтрация ссылок и поиск коротких новостей.
        if ('/news/' in href and 
            text and len(text) > 20 and len(text) < 120 and
            text not in seen_texts):
            
            # Уборка лишнего хлама из текста.
            clean_text = re.sub(r'\s*\d{1,2}:\d{2}.*$', '', text)
            clean_text = clean_text.strip()
            
            if clean_text:
                seen_texts.add(clean_text)
                last_three_news.append(clean_text)
                news_count += 1
    
    # Переменная с последними 3 новостями.
    latest_news = last_three_news
    return latest_news
t = get_weather_by_ip()
d = get_datetime()
n = get_news_from_lenta_working()
#print(t)
#print(get_datetime())
#print(get_news_from_lenta_working())