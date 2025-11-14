import threading
import time
from core.input_simulator import InputSimulator

clicking = False
mode = "Click"
simulator = InputSimulator("left")

def clicker_loop(interval: float):
    global clicking
    while clicking:
        simulator.click()
        if interval > 0:
            time.sleep(interval)

def start_clicking(interval: float, selected_mode: str, target_key: str):
    global clicking, mode, simulator
    if clicking:
        return
    clicking = True
    mode = selected_mode
    simulator.set_key(target_key)

    if mode == "Click":
        threading.Thread(target=clicker_loop, args=(interval,), daemon=True).start()
    elif mode == "Hold":
        simulator.press()

def stop_clicking():
    global clicking
    if clicking:
        if mode == "Hold":
            simulator.release()
        clicking = False
