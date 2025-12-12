from unittest.mock import patch, mock_open
from unittest.mock import mock_open
from unittest.mock import call
from head import quick_txt
from head import read_txt_files
from head import timer
from unittest.mock import MagicMock
from head import wikipedia
from head import rutube
from head import google
from urllib.parse import quote
import pytest
import webbrowser



def test_quick_txt_basic():
    """Базовый тест - файл создается"""
    # Мокаем все что нужно
    with patch('os.path.expanduser', return_value='/home/user'), \
         patch('os.path.join', return_value='/home/user/Documents/doc.txt'), \
         patch('builtins.open', mock_open()):
     
        # Просто проверяем, что функция выполняется без ошибок
        result = quick_txt('doc', 'текст')
        assert result == '/home/user/Documents/doc.txt'


def test_quick_txt_writes_correct_content():
    """Проверяем запись правильного содержимого"""
    with patch('os.path.expanduser', return_value='/home/user'), \
         patch('os.path.join', return_value='/home/user/Documents/test.txt'):
        
        # Создаем мок для open
        m = mock_open()
        
        with patch('builtins.open', m):
            quick_txt('test', 'line1\nline2')
        
        # Проверяем что записано
        m.assert_called_once_with('/home/user/Documents/test.txt', 'w', encoding='utf-8')
        handle = m()
        handle.write.assert_called_once_with('line1\nline2')

def test_read_txt_files():
    """Простой тест поиска файлов"""
    with patch('os.walk') as mock_walk, \
         patch('builtins.open', mock_open(read_data='Тестовый текст')), \
         patch('voice.va_speak') as mock_voice:
        
        # Делаем так, чтобы на диске C: нашелся файл
        mock_walk.return_value = [
            ('C:\\Users\\Test', [], ['test.txt', 'other.txt'])
        ]
        
        # Запускаем функцию
        read_txt_files('test')
        
        # Проверяем что голос был вызван с правильным текстом
        mock_voice.assert_called_once_with('Тестовый текст')


def test_read_txt_files_no():
    """Тест когда файлы не найдены"""
    with patch('os.walk') as mock_walk, \
         patch('voice.va_speak') as mock_voice:
        
        # Пустые результаты поиска
        mock_walk.return_value = []
        
        # Запускаем функцию
        read_txt_files('несуществующий')
        
        # Проверяем что голос НЕ был вызван
        mock_voice.assert_not_called()

from unittest.mock import patch

def test_timer():
    """Базовый тест таймера"""
    with patch('voice.va_speak') as mock_voice, \
         patch('num2words', return_value="шестьдесят"), \
         patch('time.sleep'):
        
        # Запускаем таймер на 1 минуту
        timer(1)
        
        # Проверяем что были вызовы озвучки
        mock_voice.assert_any_call("Осталось шестьдесятсекунд")
        mock_voice.assert_any_call("Таймер истёк")


def test_timer_not_started():
    """Тест когда таймер не запускается"""
    with patch('voice.va_speak') as mock_voice, \
         patch('time.sleep') as mock_sleep:
        
        # Запускаем таймер с 0 минут
        timer(0)
        
        # Проверяем только сообщение о не запуске
        mock_voice.assert_called_once_with("Таймер не запущен")
        
        # Проверяем что sleep не вызывался
        assert not mock_sleep.called

from unittest.mock import patch
import webbrowser

def test_wikipedia():
    """Простой тест: проверяем что открывается правильный URL"""
    # Мокаем webbrowser.open
    mock_open = MagicMock()
    
    with patch('webbrowser.open', mock_open):
        # Вызываем функцию с тестовым запросом
        wikipedia("Искусственный интеллект")
        
        # Проверяем что функция открытия браузера вызвана
        assert mock_open.called
        
        # Проверяем структуру URL
        url = mock_open.call_args[0][0]
        assert url.startswith("https://ru.wikipedia.org/wiki/")
        assert "Искусственный%20интеллект" in url

def test_rutube_1():
    """Простой тест что функция выполняется без ошибок"""
    mock_open = MagicMock()  # Создаем MagicMock
    
    with patch('webbrowser.open', mock_open):
        # Просто проверяем что не падает
        rutube("test")
        assert mock_open.called


def test_rutube_2():
    """Проверяем что ссылка строится правильно"""
    mock_open = MagicMock()
    
    with patch('webbrowser.open', mock_open):
        rutube("кошки видео")
        
        url = mock_open.call_args[0][0]
        # Простая проверка
        assert "rutube.ru" in url
        assert "search/video" in url
        assert "query=" in url
        assert "кошки%20видео" in url

def test_google1():
    """Простой тест создания Google ссылки"""
    # Создаем MagicMock для webbrowser.open
    mock_browser = MagicMock()
    
    with patch('webbrowser.open', mock_browser):
        # Вызываем функцию
        google("как научиться программировать")
        
        # Проверяем вызов
        assert mock_browser.called
        
        # Проверяем URL
        actual_url = mock_browser.call_args[0][0]
        assert "google.com" in actual_url
        assert "search?q=" in actual_url
        assert "%D0%BA%D0%B0%D0%BA%20%D0%BD%D0%B0%D1%83%D1%87%D0%B8%D1%82%D1%8C%D1%81%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D1%82%D1%8C" in actual_url


def test_google_2():
    """Тест нескольких поисковых запросов"""
    mock_browser = MagicMock()
    
    with patch('webbrowser.open', mock_browser):
        # Несколько вызовов
        google("кошки")
        google("собаки")
        google("птицы")
        
        # Проверяем количество вызовов
        assert mock_browser.call_count == 3
        
        # Проверяем разные запросы
        calls = mock_browser.call_args_list
        assert "кошки" in quote.decode(calls[0][0][0].split("q=")[1])
        assert "собаки" in quote.decode(calls[1][0][0].split("q=")[1])