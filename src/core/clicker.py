import ctypes
import threading
import time

SendInput = ctypes.windll.user32.SendInput
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP   = 0x0004

clicking = False

def click():
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def clicker_loop(interval: float):
    global clicking
    while clicking:
        click()
        if interval > 0:
            time.sleep(interval)

def start_clicking(interval: float):
    global clicking
    if not clicking:
        clicking = True
        threading.Thread(target=clicker_loop, args=(interval,), daemon=True).start()

def stop_clicking():
    global clicking
    clicking = False
