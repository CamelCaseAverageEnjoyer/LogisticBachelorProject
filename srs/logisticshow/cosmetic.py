"""Переделать файл перед отправкой на РИД"""
from playsound3 import playsound
from gtts import gTTS
import colorama
import random
import os


def my_print(txt: any, color: str = None, if_print: bool = True) -> None:
    """Функция вывода цветного текста
    :param txt: Выводимый текст
    :param color: Цвет текста {b, g, y, r, c, m}
    :param if_print: Флаг вывода для экономии места"""
    color_bar = {"b": colorama.Fore.BLUE, "g": colorama.Fore.GREEN, "y": colorama.Fore.YELLOW, "r": colorama.Fore.RED,
                 "c": colorama.Fore.CYAN, "m": colorama.Fore.MAGENTA, None: colorama.Style.RESET_ALL}
    if if_print and color in color_bar.keys():
        print(color_bar[color] + f"{txt}" + colorama.Style.RESET_ALL)

def real_workload_time(n: int, n_total: int, time_begin, time_now) -> str:
    n_remain = n_total - n
    return f"время: {time_now - time_begin}, оставшееся время: {(time_now - time_begin) * n_remain / n}"

def talk_aloud(txt):
    s = gTTS(txt, lang='ru')
    s.save('talk_file.mp3')
    playsound('talk_file.mp3')
    os.remove('talk_file.mp3')

def talk(cnd=True):
    if cnd:
        talk_aloud(random.choice(['Работай нахуй!', 'Вот хуй!', 'Ща порву тебя нахуй!', 'Йобушки воробушки', 'Пиздец',
                                  'Ебааать', 'Йоб меня в сраку', 'Ебись вертись', 'Мммм хуита', 'Ля ля бля', 'Нихуясе',
                                  'Ебать мой хуй', 'Хуё моё', 'Ебучий случай', 'Писос', 'Йоб проёб', 'Ниибёт',
                                  'Дятел блин', 'Не жопься', 'Сверхебически', 'Мать перемать', 'Не косоёбся',
                                  'Етись крутись']))