"""
Программа для управления громкостью звука в Windows.
Позволяет регулировать уровень звука, включать и выключать его
через простое текстовое меню.
"""

from datetime import date
from sound import Sound


def print_header():
    """Выводит заголовок программы."""
    print("")
    print("Windows Sound Manager (Python 3)")
    print("Copyright (c) 2014 - %d | Paradoxis" % date.today().year)
    print("")


def print_menu():
    """Выводит меню выбора опций."""
    print("Choose an option:")
    print("1] Mute / Unmute volume")
    print("2] Increase volume")
    print("3] Decrease volume")
    print("4] Set volume to 0")
    print("5] Set volume to 100")
    print("6] Set volume to ...")
    print("7] Print sound settings")
    print("8] Quit")


def print_sound_settings():
    """Выводит текущие настройки звука."""
    print("Current volume | %s" % str(Sound.current_volume()))
    print("Sound muted    | %s" % str(Sound.is_muted()))
    print("----------------------")
    print("")


def main():
    """Основная функция программы."""
    print_header()

    while True:
        print_menu()
        option = input("> ")
        print("")

        if option == "1":
            Sound.mute()
            continue

        if option == "2":
            Sound.volume_up()
            continue

        if option == "3":
            Sound.volume_down()
            continue

        if option == "4":
            Sound.volume_min()
            continue

        if option == "5":
            Sound.volume_max()
            continue

        if option == "6":
            try:
                volume = int(input("Volume (0 - 100): "))
                Sound.volume_set(volume)
            except ValueError:
                print("Error: Please enter a valid number.")
            continue

        if option == "7":
            print_sound_settings()
            continue

        if option == "8":
            exit(0)


if __name__ == "__main__":
    main()
