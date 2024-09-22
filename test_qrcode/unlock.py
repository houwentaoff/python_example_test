import pyautogui
import time

interval = 5

try:
    while True:
        pyautogui.press('capslock')
        print("xxss")
        time.sleep(interval)
except KeyboardInterrupt:
    print("overr")