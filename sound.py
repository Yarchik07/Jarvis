"""
Этот код позволяет управлять громкостью звука в Windows.
"""

from keyboard import Keyboard


class Sound:
    """
    Класс Sound (Звук)
    :author: Paradoxis <luke@paradoxis.nl>

    Позволяет управлять громкостью звука в Windows.
    При первом вызове любого метода класса системная громкость полностью сбрасывается.
    Это активирует отслеживание звука и состояния отключения звука.
    """

    # Current volume, we will set this to 100 once initialized
    __current_volume = None

    @staticmethod
    def current_volume():
        """
        Получить текущую громкость.

        :return: текущий уровень громкости (целое число)
        :rtype: int
        """
        if Sound.__current_volume is None:
            return 0
        else:
            return Sound.__current_volume

    @staticmethod
    def __set_current_volume(volume):
        """
        Установить текущую громкость.

        Предотвращает установку значений больше 100 и меньше 0.

        :param volume: уровень громкости для установки
        :type volume: int
        """
        if volume > 100:
            Sound.__current_volume = 100
        elif volume < 0:
            Sound.__current_volume = 0
        else:
            Sound.__current_volume = volume

    # The sound is not muted by default, better tracking should be made
    __is_muted = False

    @staticmethod
    def is_muted():
        """
        Получить состояние отключения звука.

        :return: отключен ли звук
        :rtype: bool
        """
        return Sound.__is_muted

    @staticmethod
    def __track():
        """Начать отслеживание настроек звука и отключения звука."""
        if Sound.__current_volume is None:
            Sound.__current_volume = 0
            for i in range(0, 50):
                Sound.volume_up()

    @staticmethod
    def mute():
        """
        Отключить или включить системные звуки.

        Выполняется путем имитации нажатия клавиши VK_VOLUME_MUTE.
        """
        Sound.__track()
        Sound.__is_muted = (not Sound.__is_muted)
        Keyboard.key(Keyboard.VK_VOLUME_MUTE)

    @staticmethod
    def volume_up():
        """
        Увеличить громкость системы.

        Выполняется путем имитации нажатия клавиши VK_VOLUME_UP.
        """
        Sound.__track()
        Sound.__set_current_volume(Sound.current_volume() + 2)
        Keyboard.key(Keyboard.VK_VOLUME_UP)

    @staticmethod
    def volume_down():
        """
        Уменьшить громкость системы.

        Выполняется путем имитации нажатия клавиши VK_VOLUME_DOWN.
        """
        Sound.__track()
        Sound.__set_current_volume(Sound.current_volume() - 2)
        Keyboard.key(Keyboard.VK_VOLUME_DOWN)

    @staticmethod
    def volume_set(amount):
        """
        Установить громкость на конкретное значение.

        Ограничено четными числами. Это связано с тем, что событие
        VK_VOLUME_UP/VK_VOLUME_DOWN изменяет громкость на два деления каждый раз.

        :param amount: уровень громкости для установки (целое число)
        :type amount: int
        """
        Sound.__track()

        if Sound.current_volume() > amount:
            for i in range(0, int((Sound.current_volume() - amount) / 2)):
                Sound.volume_down()
        else:
            for i in range(0, int((amount - Sound.current_volume()) / 2)):
                Sound.volume_up()

    @staticmethod
    def volume_min():
        """Установить минимальную громкость (0)."""
        Sound.volume_set(0)

    @staticmethod
    def volume_max():
        """Установить максимальную громкость (100)."""
        Sound.volume_set(100)
