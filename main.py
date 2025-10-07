import ctypes
import time
import random
import sys
import pyautogui
import os
from datetime import datetime
import threading

# Конфигурация
KEY = 0x20  # Space (0x20)
MIN_PRESS_DUR = 0.04               # Минимальное время нажатия (сек)
MAX_PRESS_DUR = 0.07  # Максимальное время нажатия
MIN_DELAY = 0.01  # Минимальная пауза между кликами
MAX_DELAY = 0.04  # Максимальная пауза
TOGGLE_HOTKEY = 0x09 # Клавиша TAB
EXIT_HOTKEY = 0x10  # Клавиша SHIFT
IMAGEM_BAU = r"D:\1.png"  # Путь к первому изображению
IMAGEM_BAU1 = r"D:\2.png"  # Путь ко второму изображению

# Глобальные переменные
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
running = False
contador = 0
bitcoin_msgs = 0
inicio = time.time()
use_confidence = True  # Флаг для использования confidence

def press_key():
    user32.keybd_event(KEY, 0, 0x0001, 0)  # KEY_DOWN
    time.sleep(random.uniform(MIN_PRESS_DUR, MAX_PRESS_DUR))
    user32.keybd_event(KEY, 0, 0x0002, 0)  # KEY_UP

def mensagem_colorida(texto, cor=False):
    if cor:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"\033[38;2;{r};{g};{b}m{texto}\033[0m"
    else:
        return f"\033[38;2;255;255;255m{texto}\033[0m"

# Всё что иже - не обращай внимания, это визуал, не более
def mensagem_bitcoin():
    global bitcoin_msgs
    bitcoin_msgs += 1
    hora = datetime.now().strftime("%H:%M:%S")
    frases = [
        "инициализация потока майнинга...",
        "подключение",
        "поиск допустимого одноразового номера...",
        "блок проверки 0x24f...a91",
        "SHA-256 параллельное выполнение началось...",
        "проверка целости завершена",
        "отправить принято сетью",
        "синхронизация времени...",
        "хэш-пакет получен и обработан"
    ]
    frase = random.choice(frases)
    valor_btc = f"+0.000000{random.randint(100, 999)} BTC"
    valor_destacado = f"\033[1;93m{valor_btc}\033[0m"
    return (
        mensagem_colorida(hora, cor=False) + " " +
        mensagem_colorida(f"оповещение: {frase} ", cor=True) +
        valor_destacado
    )

def locate_image(image_path):
    """Функция для поиска изображения с обработкой ошибки confidence"""
    global use_confidence
    
    if not os.path.exists(image_path):
        return None
    
    try:
        if use_confidence:
            return pyautogui.locateOnScreen(image_path, confidence=0.7, grayscale=True)
        else:
            return pyautogui.locateOnScreen(image_path, grayscale=True)
    except Exception as e:
        if "confidence" in str(e):
            print("OpenCV не установлен, отключаю confidence...")
            use_confidence = False
            return pyautogui.locateOnScreen(image_path, grayscale=True)
        return None

def clicar_no_bau():
    global contador

    # Пробуем найти первое изображение
    local = None
    image_found = None
    
    try:
        local = locate_image(IMAGEM_BAU)
        if local:
            image_found = IMAGEM_BAU
    except Exception as e:
        print(f"Ошибка при поиске первого изображения: {e}")
    
    # Если первое не найдено, пробуем второе
    if not local:
        try:
            local = locate_image(IMAGEM_BAU1)
            if local:
                image_found = IMAGEM_BAU1
        except Exception as e:
            print(f"Ошибка при поиске второго изображения: {e}")

    if local:
        try:
            centro_bau = pyautogui.center(local)
            # Не перемещаем мышь, сразу кликаем в координаты
            pyautogui.click(centro_bau.x, centro_bau.y)
            
            contador += 1
            texto = f"сундучок подобран! /ᐠ. .ᐟ\\ Ⳋ ({contador}) - {os.path.basename(image_found)}"
            print(mensagem_colorida(texto, cor=True))

            if random.randint(1, 69) == 1:
                print(mensagem_bitcoin())
                
            return True
        except Exception as e:
            print(f"Ошибка при клике: {e}")
            return False
    return False

def listen_hotkeys():
    global running
    while True:
        if user32.GetAsyncKeyState(TOGGLE_HOTKEY) & 0x8000:
            running = not running
            status = 'ВКЛ' if running else 'ВЫКЛ'
            print(f"\n{'-'*20} Состояние: {status} {'-'*20}")
            time.sleep(0.5)
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

    print("\n\n\033[1;36m[ СТАТИСТИКА ]\033[0m")
    print(f"время выполнения: {horas}h {minutos}m {segundos}s")
    print(f"общее количество нажатых сундуков: {contador}")
    print(f"(на это внимание не обращаем): {bitcoin_msgs}")

def test_images():
    """Функция для тестирования распознавания изображений"""
    print("Тестирование распознавания изображений...")
    for i, img_path in enumerate([IMAGEM_BAU, IMAGEM_BAU1], 1):
        if os.path.exists(img_path):
            try:
                location = locate_image(img_path)
                if location:
                    print(f"✅ Изображение {i} ({os.path.basename(img_path)}) найдено на экране!")
                else:
                    print(f"❌ Изображение {i} ({os.path.basename(img_path)}) НЕ найдено на экране.")
            except Exception as e:
                print(f"⚠️ Ошибка при поиске изображения {i}: {e}")
        else:
            print(f"⚠️ Файл изображения {i} не существует: {img_path}")

def main():
    print(f"""Автокликер запущен. Управление:
    Клавиша TAB - Вкл/Выкл
    Клавиша SHIFT - Выход
    """)
    print("ᨐ ฅ добро пожаловать в bongo cat script!\n")

    # Тестируем распознавание изображений при запуске
    test_images()
    print("-" * 50)

    threading.Thread(target=listen_hotkeys, daemon=True).start()

    try:
        while True:
            if running:
                # Проверяем наличие изображения
                if clicar_no_bau():
                    # После клика ждем немного перед возобновлением
                    time.sleep(0.3)
                else:
                    # Если изображения нет, продолжаем спамить пробел
                    press_key()
                    time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            else:
                # Небольшая пауза когда скрипт выключен
                time.sleep(0.1)
    except KeyboardInterrupt:
        show_stats()
        input("нажмите Enter, чтобы закрыть программу...")

if __name__ == "__main__":
    main()