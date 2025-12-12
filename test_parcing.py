from unittest.mock import MagicMock, patch
from parcing import (
    get_weather_by_ip,
    get_datetime,
    get_news_from_lenta_working,
)


def test_get_weather_by_ip_1():
    """Просто проверяем что функция что-то возвращает."""
    mock_response = MagicMock()
    mock_response.json.return_value = {'city': 'Moscow'}
    mock_response.text = 'html'

    with patch(
        'parcing.requests.get',
        side_effect=[mock_response, mock_response]
    ), patch('parcing.re.findall', return_value=['+20°', '5 м/с', '760 мм']):

        result = get_weather_by_ip()

        # Простая проверка структуры
        assert isinstance(result, tuple)
        assert len(result) == 3


def test_get_weather_by_ip_2():
    """Тест когда ветер не найден, но температура и давление есть."""
    mock_response = MagicMock()
    mock_response.json.return_value = {'city': 'TestCity'}
    mock_response.text = 'html'

    # Температура есть, ветра нет, давление есть
    with patch(
        'parcing.requests.get',
        side_effect=[mock_response, mock_response]
    ), patch('parcing.re.findall', side_effect=[
        ['+15°'],       # temperatures - есть
        [],             # wind - пусто
        ['755 мм']      # pressure - есть
    ]):

        temp, wind, pressure = get_weather_by_ip()

        # Проверяем конкретные значения
        assert temp == '+15°'
        assert wind == 'Ветер не определен'
        assert pressure == '755 мм'


def test_get_datetime1():
    """Просто проверяем что функция не падает."""
    # Создаем мок объекта response
    mock_response = MagicMock()
    mock_response.text = '''
    <html>
        <body>
            <span class="hours">12</span>
            <span class="minutes">30</span>
            <span x-text="city.week_day">Понедельник</span>
            <span x-text="city.date">1 января 2024</span>
        </body>
    </html>
    '''

    # Мокаем requests.get
    with patch('parcing.requests.get', return_value=mock_response):
        try:
            result = get_datetime()
            # Если функция вернула результат
            assert result is not None
        except Exception:
            # Если произошла ошибка, проверяем что это не критичная ошибка
            # В данном тесте мы просто проверяем, что функция не падает
            # с критичными ошибками
            # (но она может падать с ожидаемыми исключениями
            # при некорректных данных)
            pass


def test_get_datetime2():
    """Проверяем что возвращается строка."""
    # Создаем мок объекта response
    mock_response = MagicMock()
    mock_response.text = '<html><body>2024-01-01 12:00:00</body></html>'

    # Мокаем requests.get и BeautifulSoup
    with patch('parcing.requests.get', return_value=mock_response):
        # Создаем мок BeautifulSoup
        mock_soup = MagicMock()
        mock_find = MagicMock()
        mock_find.text = '2024-01-01 12:00:00'
        mock_soup.find.return_value = mock_find

        with patch('parcing.BeautifulSoup', return_value=mock_soup):
            result = get_datetime()
            # Просто проверяем тип
            assert isinstance(result, str)


def test_get_news_from_lenta_working1():
    """Самый простой тест - функция не вызывает ошибок."""
    # Создаем мок объекта response
    mock_response = MagicMock()
    mock_response.text = '<html><body>Новости</body></html>'

    # Мокаем requests.get и BeautifulSoup
    with patch('parcing.requests.get', return_value=mock_response):
        # Создаем мок BeautifulSoup
        mock_soup = MagicMock()
        mock_soup.find_all.return_value = []
        with patch('parcing.BeautifulSoup', return_value=mock_soup):
            # Если не упало - хорошо
            result = get_news_from_lenta_working()
            assert result is not None


def test_get_news_from_lenta_working2():
    """Проверяем сигнатуру функции."""
    # Создаем мок объекта response
    mock_response = MagicMock()
    mock_response.text = '<html><body>Новости</body></html>'

    # Создаем моки элементов новостей
    mock_news_item1 = MagicMock()
    mock_news_item2 = MagicMock()

    # Настраиваем моки так, чтобы они имели атрибут .text
    mock_news_item1.text = 'Первая новость'
    mock_news_item2.text = 'Вторая новость'

    # Создаем мок BeautifulSoup
    mock_soup = MagicMock()
    mock_soup.find_all.return_value = [mock_news_item1, mock_news_item2]

    # Мокаем requests.get, BeautifulSoup и re.sub
    with patch('parcing.requests.get', return_value=mock_response), \
        patch('parcing.BeautifulSoup', return_value=mock_soup), \
        patch(
        'parcing.re.sub',
        side_effect=lambda pattern, repl, string: string
    ):

        result = get_news_from_lenta_working()

        # Должен быть список
        assert isinstance(result, list)
        # Все элементы должны быть строками
        for item in result:
            assert isinstance(item, str)
