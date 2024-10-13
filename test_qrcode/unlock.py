import pyautogui
import time
import random

interval = 5
pyautogui.FAILSAFE=False
try:
    while True:
        pyautogui.press('capslock')
        print("xxss")
        interval = random.randint(5, 20)
        time.sleep(interval)
except KeyboardInterrupt:
    print("overr")