import threading
from core.input_simulator import InputSimulator

_lock = threading.Lock()
_stop_event = None
_thread = None
_clicking = False
mode = "Click"
simulator = InputSimulator("left")


def is_clicking() -> bool:
    return _clicking


def _clicker_loop(interval: float, stop_event: threading.Event):
    while not stop_event.is_set():
        simulator.click()
        if stop_event.wait(interval):
            break


def start_clicking(interval: float, selected_mode: str, target_key: str):
    global _clicking, _stop_event, _thread, mode
    with _lock:
        if _clicking:
            return
        _clicking = True
        mode = selected_mode
        simulator.set_key(target_key)

        if mode == "Click":
            _stop_event = threading.Event()
            _thread = threading.Thread(
                target=_clicker_loop,
                args=(interval, _stop_event),
                daemon=True,
            )
            _thread.start()
        elif mode == "Hold":
            simulator.press()


def stop_clicking():
    global _clicking, _stop_event, _thread
    with _lock:
        if not _clicking:
            return
        _clicking = False
        thread, event = _thread, _stop_event
        _thread = _stop_event = None

        if mode == "Hold":
            simulator.release()

    if event:
        event.set()
    if thread:
        thread.join(timeout=1)