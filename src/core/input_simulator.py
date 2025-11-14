import ctypes
import keyboard

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP   = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP   = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP   = 0x0040

class InputSimulator:
    def __init__(self, target_key="left"):
        self.set_key(target_key)

    def set_key(self, key: str):
        self.key = key.lower()
        if self.key in ["left", "right", "middle"]:
            self.is_mouse = True
        else:
            self.is_mouse = False

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
        event = 0
        if self.key == "left":
            event = MOUSEEVENTF_LEFTDOWN if down else MOUSEEVENTF_LEFTUP
        elif self.key == "right":
            event = MOUSEEVENTF_RIGHTDOWN if down else MOUSEEVENTF_RIGHTUP
        elif self.key == "middle":
            event = MOUSEEVENTF_MIDDLEDOWN if down else MOUSEEVENTF_MIDDLEUP

        ctypes.windll.user32.mouse_event(event, 0, 0, 0, 0)
