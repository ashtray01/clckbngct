import ctypes
import time
import random
import sys
import os
from datetime import datetime
import threading

# Устанавливаем UTF-8 кодировку для вывода
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Для старых версий Python
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Конфигурация - Virtual-Key Codes
# Буквы A-Z (0x41-0x5A)
KEY_A = 0x41  # A
KEY_B = 0x42  # B
KEY_C = 0x43  # C
KEY_D = 0x44  # D
KEY_E = 0x45  # E
KEY_F = 0x46  # F
KEY_G = 0x47  # G
KEY_H = 0x48  # H
KEY_I = 0x49  # I
KEY_J = 0x4A  # J
KEY_K = 0x4B  # K
KEY_L = 0x4C  # L
KEY_M = 0x4D  # M
KEY_N = 0x4E  # N
KEY_O = 0x4F  # O
KEY_P = 0x50  # P
KEY_Q = 0x51  # Q
KEY_R = 0x52  # R
KEY_S = 0x53  # S
KEY_T = 0x54  # T
KEY_U = 0x55  # U
KEY_V = 0x56  # V
KEY_W = 0x57  # W
KEY_X = 0x58  # X
KEY_Y = 0x59  # Y
KEY_Z = 0x5A  # Z

# Цифры 0-9 (0x30-0x39)
KEY_0 = 0x30  # 0
KEY_1 = 0x31  # 1
KEY_2 = 0x32  # 2
KEY_3 = 0x33  # 3
KEY_4 = 0x34  # 4
KEY_5 = 0x35  # 5
KEY_6 = 0x36  # 6
KEY_7 = 0x37  # 7
KEY_8 = 0x38  # 8
KEY_9 = 0x39  # 9

# Функциональные клавиши
KEY_SPACE = 0x20  # Space
KEY_TAB = 0x09    # TAB
KEY_SHIFT = 0x10  # SHIFT
KEY_ENTER = 0x0D  # ENTER
KEY_ESC = 0x1B    # ESCAPE
KEY_BACKSPACE = 0x08  # BACKSPACE
KEY_DELETE = 0x2E  # DELETE
KEY_INSERT = 0x2D  # INSERT
KEY_HOME = 0x24    # HOME
KEY_END = 0x23     # END
KEY_PGUP = 0x21    # PAGE UP
KEY_PGDN = 0x22    # PAGE DOWN

# Клавиши со специальными символами
KEY_MINUS = 0xBD    # - (минус)
KEY_EQUAL = 0xBB    # = (равно)
KEY_LBRACKET = 0xDB # [ (левая скобка)
KEY_RBRACKET = 0xDD # ] (правая скобка)
KEY_SEMICOLON = 0xBA # ; (точка с запятой)
KEY_APOSTROPHE = 0xDE # ' (апостроф)
KEY_COMMA = 0xBC    # , (запятая)
KEY_PERIOD = 0xBE   # . (точка)
KEY_SLASH = 0xBF    # / (слеш)
KEY_BACKSLASH = 0xDC # \ (обратный слеш)
KEY_TILDE = 0xC0    # ` (тильда)

# Настройки кликера
MIN_PRESS_DUR = 0.02  # Минимальное время нажатия (сек)
MAX_PRESS_DUR = 0.04  # Максимальное время нажатия
MIN_DELAY = 0.01      # Минимальная пауза между кликами
MAX_DELAY = 0.04      # Максимальная пауза
TOGGLE_HOTKEY = KEY_TAB  # Клавиша TAB для вкл/выкл
EXIT_HOTKEY = KEY_SHIFT  # Клавиша SHIFT для выхода

# Глобальные переменные
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
running = False
contador = 0
inicio = time.time()

def press_key():
    """Функция нажатия всех клавиш одновременно"""
    # Нажимаем все клавиши
    user32.keybd_event(KEY_SPACE, 0, 0x0001, 0)
    
    # Цифры
    user32.keybd_event(KEY_0, 0, 0x0001, 0)
    user32.keybd_event(KEY_1, 0, 0x0001, 0)
    user32.keybd_event(KEY_2, 0, 0x0001, 0)
    user32.keybd_event(KEY_3, 0, 0x0001, 0)
    user32.keybd_event(KEY_4, 0, 0x0001, 0)
    user32.keybd_event(KEY_5, 0, 0x0001, 0)
    user32.keybd_event(KEY_6, 0, 0x0001, 0)
    user32.keybd_event(KEY_7, 0, 0x0001, 0)
    user32.keybd_event(KEY_8, 0, 0x0001, 0)
    user32.keybd_event(KEY_9, 0, 0x0001, 0)
    
    # Буквы A-Z
    user32.keybd_event(KEY_A, 0, 0x0001, 0)
    user32.keybd_event(KEY_B, 0, 0x0001, 0)
    user32.keybd_event(KEY_C, 0, 0x0001, 0)
    user32.keybd_event(KEY_D, 0, 0x0001, 0)
    user32.keybd_event(KEY_E, 0, 0x0001, 0)
    user32.keybd_event(KEY_F, 0, 0x0001, 0)
    user32.keybd_event(KEY_G, 0, 0x0001, 0)
    user32.keybd_event(KEY_H, 0, 0x0001, 0)
    user32.keybd_event(KEY_I, 0, 0x0001, 0)
    user32.keybd_event(KEY_J, 0, 0x0001, 0)
    user32.keybd_event(KEY_K, 0, 0x0001, 0)
    user32.keybd_event(KEY_L, 0, 0x0001, 0)
    user32.keybd_event(KEY_M, 0, 0x0001, 0)
    user32.keybd_event(KEY_N, 0, 0x0001, 0)
    user32.keybd_event(KEY_O, 0, 0x0001, 0)
    user32.keybd_event(KEY_P, 0, 0x0001, 0)
    user32.keybd_event(KEY_Q, 0, 0x0001, 0)
    user32.keybd_event(KEY_R, 0, 0x0001, 0)
    user32.keybd_event(KEY_S, 0, 0x0001, 0)
    user32.keybd_event(KEY_T, 0, 0x0001, 0)
    user32.keybd_event(KEY_U, 0, 0x0001, 0)
    user32.keybd_event(KEY_V, 0, 0x0001, 0)
    user32.keybd_event(KEY_W, 0, 0x0001, 0)
    user32.keybd_event(KEY_X, 0, 0x0001, 0)
    user32.keybd_event(KEY_Y, 0, 0x0001, 0)
    user32.keybd_event(KEY_Z, 0, 0x0001, 0)
    
    # Специальные клавиши
    user32.keybd_event(KEY_ENTER, 0, 0x0001, 0)
    user32.keybd_event(KEY_ESC, 0, 0x0001, 0)
    user32.keybd_event(KEY_BACKSPACE, 0, 0x0001, 0)
    user32.keybd_event(KEY_DELETE, 0, 0x0001, 0)
    user32.keybd_event(KEY_INSERT, 0, 0x0001, 0)
    user32.keybd_event(KEY_HOME, 0, 0x0001, 0)
    user32.keybd_event(KEY_END, 0, 0x0001, 0)
    user32.keybd_event(KEY_PGUP, 0, 0x0001, 0)
    user32.keybd_event(KEY_PGDN, 0, 0x0001, 0)
    
    # Символы
    user32.keybd_event(KEY_MINUS, 0, 0x0001, 0)
    user32.keybd_event(KEY_EQUAL, 0, 0x0001, 0)
    user32.keybd_event(KEY_LBRACKET, 0, 0x0001, 0)
    user32.keybd_event(KEY_RBRACKET, 0, 0x0001, 0)
    user32.keybd_event(KEY_SEMICOLON, 0, 0x0001, 0)
    user32.keybd_event(KEY_APOSTROPHE, 0, 0x0001, 0)
    user32.keybd_event(KEY_COMMA, 0, 0x0001, 0)
    user32.keybd_event(KEY_PERIOD, 0, 0x0001, 0)
    user32.keybd_event(KEY_SLASH, 0, 0x0001, 0)
    user32.keybd_event(KEY_BACKSLASH, 0, 0x0001, 0)
    user32.keybd_event(KEY_TILDE, 0, 0x0001, 0)
    
    # Держим нажатыми случайное время
    time.sleep(random.uniform(MIN_PRESS_DUR, MAX_PRESS_DUR))
    
    # Отпускаем все клавиши
    user32.keybd_event(KEY_SPACE, 0, 0x0002, 0)
    
    # Цифры
    user32.keybd_event(KEY_0, 0, 0x0002, 0)
    user32.keybd_event(KEY_1, 0, 0x0002, 0)
    user32.keybd_event(KEY_2, 0, 0x0002, 0)
    user32.keybd_event(KEY_3, 0, 0x0002, 0)
    user32.keybd_event(KEY_4, 0, 0x0002, 0)
    user32.keybd_event(KEY_5, 0, 0x0002, 0)
    user32.keybd_event(KEY_6, 0, 0x0002, 0)
    user32.keybd_event(KEY_7, 0, 0x0002, 0)
    user32.keybd_event(KEY_8, 0, 0x0002, 0)
    user32.keybd_event(KEY_9, 0, 0x0002, 0)
    
    # Буквы A-Z
    user32.keybd_event(KEY_A, 0, 0x0002, 0)
    user32.keybd_event(KEY_B, 0, 0x0002, 0)
    user32.keybd_event(KEY_C, 0, 0x0002, 0)
    user32.keybd_event(KEY_D, 0, 0x0002, 0)
    user32.keybd_event(KEY_E, 0, 0x0002, 0)
    user32.keybd_event(KEY_F, 0, 0x0002, 0)
    user32.keybd_event(KEY_G, 0, 0x0002, 0)
    user32.keybd_event(KEY_H, 0, 0x0002, 0)
    user32.keybd_event(KEY_I, 0, 0x0002, 0)
    user32.keybd_event(KEY_J, 0, 0x0002, 0)
    user32.keybd_event(KEY_K, 0, 0x0002, 0)
    user32.keybd_event(KEY_L, 0, 0x0002, 0)
    user32.keybd_event(KEY_M, 0, 0x0002, 0)
    user32.keybd_event(KEY_N, 0, 0x0002, 0)
    user32.keybd_event(KEY_O, 0, 0x0002, 0)
    user32.keybd_event(KEY_P, 0, 0x0002, 0)
    user32.keybd_event(KEY_Q, 0, 0x0002, 0)
    user32.keybd_event(KEY_R, 0, 0x0002, 0)
    user32.keybd_event(KEY_S, 0, 0x0002, 0)
    user32.keybd_event(KEY_T, 0, 0x0002, 0)
    user32.keybd_event(KEY_U, 0, 0x0002, 0)
    user32.keybd_event(KEY_V, 0, 0x0002, 0)
    user32.keybd_event(KEY_W, 0, 0x0002, 0)
    user32.keybd_event(KEY_X, 0, 0x0002, 0)
    user32.keybd_event(KEY_Y, 0, 0x0002, 0)
    user32.keybd_event(KEY_Z, 0, 0x0002, 0)
    
    # Специальные клавиши
    user32.keybd_event(KEY_ENTER, 0, 0x0002, 0)
    user32.keybd_event(KEY_ESC, 0, 0x0002, 0)
    user32.keybd_event(KEY_BACKSPACE, 0, 0x0002, 0)
    user32.keybd_event(KEY_DELETE, 0, 0x0002, 0)
    user32.keybd_event(KEY_INSERT, 0, 0x0002, 0)
    user32.keybd_event(KEY_HOME, 0, 0x0002, 0)
    user32.keybd_event(KEY_END, 0, 0x0002, 0)
    user32.keybd_event(KEY_PGUP, 0, 0x0002, 0)
    user32.keybd_event(KEY_PGDN, 0, 0x0002, 0)
    
    # Символы
    user32.keybd_event(KEY_MINUS, 0, 0x0002, 0)
    user32.keybd_event(KEY_EQUAL, 0, 0x0002, 0)
    user32.keybd_event(KEY_LBRACKET, 0, 0x0002, 0)
    user32.keybd_event(KEY_RBRACKET, 0, 0x0002, 0)
    user32.keybd_event(KEY_SEMICOLON, 0, 0x0002, 0)
    user32.keybd_event(KEY_APOSTROPHE, 0, 0x0002, 0)
    user32.keybd_event(KEY_COMMA, 0, 0x0002, 0)
    user32.keybd_event(KEY_PERIOD, 0, 0x0002, 0)
    user32.keybd_event(KEY_SLASH, 0, 0x0002, 0)
    user32.keybd_event(KEY_BACKSLASH, 0, 0x0002, 0)
    user32.keybd_event(KEY_TILDE, 0, 0x0002, 0)
    
    global contador
    contador += 1

def listen_hotkeys():
    global running
    while True:
        if user32.GetAsyncKeyState(TOGGLE_HOTKEY) & 0x8000:
            running = not running
            status = 'ВКЛ' if running else 'ВЫКЛ'
            print(f"\n{'-'*20} Состояние: {status} {'-'*20}")
            time.sleep(0.5)  # Защита от множественных срабатываний
        if user32.GetAsyncKeyState(EXIT_HOTKEY) & 0x8000:
            print("\nВыход...")
            show_stats()
            os._exit(0)
        time.sleep(0.01)

def show_stats():
    fim = time.time()
    tempo_total = fim - inicio
    horas = int(tempo_total // 3600)
    minutos = int((tempo_total % 3600) // 60)
    segundos = int(tempo_total % 60)
    
    print("\n" + "="*40)
    print(" СТАТИСТИКА ".center(40, "="))
    print("="*40)
    print(f"Время работы: {horas}ч {minutos}м {segundos}с")
    print(f"Всего нажатий: {contador}")
    if tempo_total > 0:
        print(f"Скорость: {contador / tempo_total:.2f} нажатий/сек")
    print("="*40)

def main():
    print("="*50)
    print("КЛАВИАТУРНЫЙ КЛИКЕР".center(50))
    print("="*50)
    print("Управление:")
    print("  TAB   - Вкл/Выкл клики")
    print("  SHIFT - Выход из программы")
    print("\nНажимаются все клавиши одновременно:")
    print("  • Буквы A-Z")
    print("  • Цифры 0-9")
    print("  • Специальные клавиши (Enter, Esc, Backspace, Delete, Insert, Home, End, PgUp, PgDn)")
    print("  • Символы (- = [ ] ; ' , . / \\ `)")
    print("  • Пробел")
    print("="*50)
    print("Добро пожаловать в клавиатурный кликер!\n")

    # Запускаем поток для отслеживания горячих клавиш
    threading.Thread(target=listen_hotkeys, daemon=True).start()

    try:
        while True:
            if running:
                press_key()
                # Случайная пауза между нажатиями
                time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            else:
                # Небольшая пауза когда скрипт выключен
                time.sleep(0.1)
    except KeyboardInterrupt:
        show_stats()
        input("\nНажмите Enter, чтобы закрыть программу...")

if __name__ == "__main__":
    main()
