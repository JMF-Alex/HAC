APP_NAME = "HAutoClicker"

MODE_CLICK = "Click"
MODE_HOLD = "Hold"
MODES = (MODE_CLICK, MODE_HOLD)

DEFAULT_INTERVAL = 0.01
MIN_INTERVAL = 0.001
MAX_INTERVAL = 3600.0

DEFAULT_HOTKEY = "F6"
DEFAULT_TARGET_KEY = "mouse_left"

MOUSE_KEYS = ("mouse_left", "mouse_right", "mouse_middle")

# Values offered in the "Key/Button" combobox. Plain "left"/"right" are the
# keyboard arrows; mouse buttons always carry the "mouse_" prefix.
KEY_CHOICES = (
    *MOUSE_KEYS,
    "space", "shift", "ctrl", "alt", "enter", "tab",
    "up", "down", "left", "right",
    *(chr(i) for i in range(ord("a"), ord("z") + 1)),
)
