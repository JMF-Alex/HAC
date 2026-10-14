from tkinter import ttk

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
TEXT_FAINT = "#7F8898"
TEXT_DISABLED = "#4D5462"

# Accent
ACCENT = "#14C8B0"
ACCENT_HOVER = "#33D8C2"
ACCENT_ACTIVE = "#0FAE9A"
ACCENT_TEXT = "#04211D"
ACCENT_SOFT = "#102629"
ACCENT_BADGE = "#17403F"
ACCENT_BADGE_TEXT = "#7CE8D8"
ACCENT_DISABLED = "#1D4A47"
ACCENT_DISABLED_TEXT = "#7FB9B3"

# Danger / warning
DANGER = "#E5484D"
DANGER_HOVER = "#F05A5F"
DANGER_ACTIVE = "#CC3D42"
DANGER_SOFT = "#2A1618"
DANGER_TEXT = "#F2777B"
WARNING = "#F5A524"
WARNING_EDGE = "#7A5410"

# Status badge tints
RUNNING_BG = "#0F2B28"
RUNNING_BORDER = "#195249"
RUNNING_TEXT = "#6EE7D6"
ERROR_BG = "#2A2010"
ERROR_BORDER = "#5A4116"
ERROR_TEXT = "#FBC15E"

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
        foreground=[("disabled", TEXT_DISABLED)],
        background=[("disabled", SURFACE_DISABLED), ("active", SURFACE_HOVER)],
        bordercolor=[("disabled", BORDER), ("focus", ACCENT)],
        lightcolor=[("focus", SURFACE_2)],
        darkcolor=[("focus", SURFACE_2)],
        arrowcolor=[("disabled", TEXT_DISABLED), ("active", TEXT)],
        selectbackground=[("readonly", SURFACE_2)],
        selectforeground=[("readonly", TEXT)],
    )
    style.layout("Vertical.TScrollbar", [
        ("Vertical.Scrollbar.trough", {"sticky": "ns", "children": [
            ("Vertical.Scrollbar.thumb", {"expand": "1", "sticky": "nswe"}),
        ]}),
    ])
    style.configure(
        "Vertical.TScrollbar",
        background=BORDER_STRONG, troughcolor=SURFACE_2, bordercolor=SURFACE_2,
        lightcolor=BORDER_STRONG, darkcolor=BORDER_STRONG, relief="flat", width=10,
    )
    style.map(
        "Vertical.TScrollbar",
        background=[("pressed", TEXT_MUTED), ("active", TEXT_FAINT)],
        lightcolor=[("pressed", TEXT_MUTED), ("active", TEXT_FAINT)],
        darkcolor=[("pressed", TEXT_MUTED), ("active", TEXT_FAINT)],
    )
    root.option_add("*TCombobox*Listbox.background", SURFACE_2)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
    root.option_add("*TCombobox*Listbox.selectForeground", ACCENT_TEXT)
    root.option_add("*TCombobox*Listbox.borderWidth", 0)
    root.option_add("*TCombobox*Listbox.relief", "flat")
    root.option_add("*TCombobox*Listbox.highlightThickness", 0)
