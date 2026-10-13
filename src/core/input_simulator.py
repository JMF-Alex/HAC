import ctypes

import keyboard

from core.constants import MOUSE_KEYS

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040

_MOUSE_FLAGS = {
    "mouse_left": (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
    "mouse_right": (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP),
    "mouse_middle": (MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP),
}
assert set(_MOUSE_FLAGS) == set(MOUSE_KEYS)


class InputSimulator:
    def __init__(self, key: str):
        self.key = key.strip().lower()
        self.is_mouse = self.key in _MOUSE_FLAGS
        if not self.is_mouse:
            keyboard.key_to_scan_codes(self.key)

    def press(self):
        if self.is_mouse:
            self._mouse_event(down=True)
        else:
            keyboard.press(self.key)

    def release(self):
        if self.is_mouse:
            self._mouse_event(down=False)
        else:
            keyboard.release(self.key)

    def click(self):
        self.press()
        self.release()

    def _mouse_event(self, down: bool):
        down_flag, up_flag = _MOUSE_FLAGS[self.key]
        ctypes.windll.user32.mouse_event(down_flag if down else up_flag, 0, 0, 0, 0)
