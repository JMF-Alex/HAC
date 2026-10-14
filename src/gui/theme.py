from tkinter import ttk

# Surfaces, darkest to lightest
BG = "#0E1014"
SIDEBAR = "#12151B"
SURFACE = "#171B22"
SURFACE_2 = "#1E232C"
SURFACE_HOVER = "#262C38"
SURFACE_DISABLED = "#14171D"

# Lines
BORDER = "#262C37"
BORDER_STRONG = "#343B49"

# Text
TEXT = "#E8EAF0"
TEXT_SOFT = "#C9CDD6"
TEXT_MUTED = "#8B93A3"
TEXT_FAINT = "#5D6574"

# Accent (selection, focus)
ACCENT = "#7C6BFF"
ACCENT_HOVER = "#8D7FFF"
ACCENT_ACTIVE = "#6A59EB"
ACCENT_SOFT = "#1B1A33"
ACCENT_DISABLED = "#3A3764"
ACCENT_DISABLED_TEXT = "#9A98C4"

# State colors
SUCCESS = "#2FBF71"
SUCCESS_HOVER = "#3AD07F"
SUCCESS_ACTIVE = "#27A862"
DANGER = "#E5484D"
DANGER_HOVER = "#F05A5F"
DANGER_ACTIVE = "#CC3D42"
DANGER_SOFT = "#2A1618"
WARNING = "#F5A524"
WARNING_EDGE = "#7A5410"

# Keycap
KEY_FACE = "#262C38"
KEY_EDGE = "#07080B"

FONT_FAMILY = "Segoe UI"
MONO_FAMILY = "Consolas"


def font(size: int = 10, weight: str = "normal"):
    return (FONT_FAMILY, size, weight)


def mono(size: int = 11, weight: str = "bold"):
    return (MONO_FAMILY, size, weight)


def apply_ttk_styles(root) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(
        "Flat.TCombobox",
        fieldbackground=SURFACE_2,
        background=SURFACE_2,
        foreground=TEXT,
        arrowcolor=TEXT_MUTED,
        bordercolor=BORDER_STRONG,
        lightcolor=SURFACE_2,
        darkcolor=SURFACE_2,
        borderwidth=1,
        relief="flat",
        padding=(10, 7),
        selectbackground=SURFACE_2,
        selectforeground=TEXT,
    )
    style.map(
        "Flat.TCombobox",
        fieldbackground=[("disabled", SURFACE_DISABLED), ("readonly", SURFACE_2)],
        foreground=[("disabled", TEXT_FAINT)],
        background=[("disabled", SURFACE_DISABLED), ("active", SURFACE_HOVER)],
        bordercolor=[("disabled", BORDER), ("focus", ACCENT)],
        lightcolor=[("focus", SURFACE_2)],
        darkcolor=[("focus", SURFACE_2)],
        arrowcolor=[("disabled", TEXT_FAINT), ("active", TEXT)],
        selectbackground=[("readonly", SURFACE_2)],
        selectforeground=[("readonly", TEXT)],
    )
    root.option_add("*TCombobox*Listbox.background", SURFACE_2)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
    root.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")
    root.option_add("*TCombobox*Listbox.borderWidth", 0)
    root.option_add("*TCombobox*Listbox.relief", "flat")
