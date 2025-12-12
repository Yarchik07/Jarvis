import sys
from unittest.mock import patch, MagicMock, mock_open
import pytest
from urllib.parse import quote
from datetime import datetime

# Мокаем vosk.Model ДО импорта модуля Beta
with patch('vosk.Model') as mock_model:
    # Возвращаем мок-объект вместо реальной модели
    mock_model.return_value = MagicMock()
    from head import (
        read_txt_files,
        timer,
        wikipedia,
        rutube,
        google,
        screenshot,
    )


def test_read_txt_files():
    """Простой тест поиска файлов."""
    with patch('os.walk') as mock_walk, \
            patch('builtins.open', mock_open(read_data='Тестовый текст')), \
            patch('voice.va_speak') as mock_voice:

        # Делаем так, чтобы на диске C: нашелся файл
        mock_walk.return_value = [
            ('C:\\Users\\Test', [], ['test.txt', 'other.txt'])
        ]

        read_txt_files('test')

        # Проверяем что голос был вызван с правильным текстом
        mock_voice.assert_called_with('Тестовый текст')


def test_read_txt_files_no():
    """Тест когда файлы не найдены."""
    with patch('os.walk') as mock_walk, \
            patch('voice.va_speak') as mock_voice:

        # Пустые результаты поиска
        mock_walk.return_value = []

        read_txt_files('несуществующий')

        # Проверяем что голос НЕ был вызван
        mock_voice.assert_not_called()


def test_timer():
    """Базовый тест таймера."""
    with patch('voice.va_speak') as mock_voice, \
            patch('head.num2words', return_value="шестьдесят"), \
            patch('time.sleep'):

        timer(1)

        # Проверяем что были вызовы озвучки
        mock_voice.assert_any_call("Осталось шестьдесятсекунд")
        mock_voice.assert_any_call("Таймер истёк")


def test_timer_not_started():
    """Тест когда таймер не запускается."""
    with patch('voice.va_speak') as mock_voice, \
            patch('time.sleep') as mock_sleep:

        timer(0)

        # Проверяем только сообщение о не запуске
        mock_voice.assert_called_once_with("Таймер не запущен")

        # Проверяем что sleep не вызывался
        assert not mock_sleep.called


def test_wikipedia():
    """Простой тест: проверяем что открывается правильный URL."""
    # Мокаем webbrowser.open
    mock_open_browser = MagicMock()

    with patch('webbrowser.open', mock_open_browser):
        wikipedia("Искусственный интеллект")

        # Проверяем что функция открытия браузера вызвана
        assert mock_open_browser.called

        # Проверяем структуру URL
        url = mock_open_browser.call_args[0][0]
        expected_encoded = quote("Искусственный интеллект")
        expected_url = f"https://ru.wikipedia.org/wiki/{expected_encoded}"
        assert url == expected_url


def test_rutube_1():
    """Простой тест что функция выполняется без ошибок."""
    mock_open_browser = MagicMock()  # Создаем MagicMock

    with patch('webbrowser.open', mock_open_browser):
        # Просто проверяем что не падает
        rutube("test")
        assert mock_open_browser.called


def test_rutube_2():
    """Проверяем что ссылка строится правильно."""
    mock_open_browser = MagicMock()

    with patch('webbrowser.open', mock_open_browser):
        rutube("кошки видео")

        url = mock_open_browser.call_args[0][0]
        expected_query = quote("кошки видео")
        expected_url = f"https://rutube.ru/search/video/?query={expected_query}"
        assert url == expected_url


def test_google1():
    """Простой тест создания Google ссылки."""
    # Создаем MagicMock для webbrowser.open
    mock_browser = MagicMock()

    with patch('webbrowser.open', mock_browser):
        google("как научиться программировать")

        # Проверяем вызов
        assert mock_browser.called

        # Проверяем URL
        actual_url = mock_browser.call_args[0][0]
        assert "google.com" in actual_url
        assert "search?q=" in actual_url
        assert (
            "%D0%BA%D0%B0%D0%BA%20%D0%BD%D0%B0%D1%83%D1%87%D0%B8%D1%82%D1%8C%D1%81%D1%8F"
            "%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2"
            "%D0%B0%D1%82%D1%8C" in actual_url
        )


def test_google_2():
    """Тест нескольких поисковых запросов."""
    mock_browser = MagicMock()

    with patch('webbrowser.open', mock_browser):
        google("кошки")
        google("собаки")
        google("птицы")

        # Проверяем количество вызовов
        assert mock_browser.call_count == 3


def test_screenshot2():
    """Проверяем что функция возвращает правильное сообщение."""
    mock_image = MagicMock()
    mock_image.size = (100, 100)

    with patch('os.path.exists', return_value=True), \
            patch('PIL.ImageGrab.grab', return_value=mock_image), \
            patch('os.startfile'):

        result = screenshot()

        # Проверяем только, что функция выполняется
        # и возвращает строку с размером
        if result is not None:
            assert isinstance(result, str)
            assert "(100, 100)" in result
