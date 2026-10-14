import re
import tkinter as tk

from core.constants import KEY_CHOICES, MODES
from gui import theme
from gui.widgets.buttons import FlatButton
from gui.widgets.cards import Card
from gui.widgets.comboboxes import FlatCombobox
from gui.widgets.entries import FlatEntry
from gui.widgets.indicators import Keycap, StatusPill
from gui.widgets.profile_sidebar import ProfileSidebar, ProfileSummary
from gui.widgets.segmented import SegmentedControl

_INTERVAL_RE = re.compile(r"^\d*[.,]?\d*$")
MAX_MESSAGE_CHARS = 70


class LayoutManager:
    APP_NAME = "HAutoClicker"
    PROFILE_NAME = "Default"

    def __init__(self, root, controller, config, version):
        self.root = root
        self.controller = controller
        self.config = config
        self.version = version
        self._hotkey = None
        self._error_text = None
        self._save_reset_id = None
        self.setup_layout()

    @staticmethod
    def _is_valid_interval(proposed: str) -> bool:
        return _INTERVAL_RE.match(proposed) is not None


    def setup_layout(self):
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.sidebar = ProfileSidebar(self.root, self.APP_NAME, self.version)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.set_profiles(
            [ProfileSummary.from_config(self.PROFILE_NAME, self.config)], active=self.PROFILE_NAME
        )
        tk.Frame(self.root, width=1, bg=theme.BORDER).grid(row=0, column=1, sticky="ns")

        main = tk.Frame(self.root, bg=theme.BG)
        main.grid(row=0, column=2, sticky="nsew")
        content = tk.Frame(main, bg=theme.BG)
        content.pack(fill="both", expand=True, padx=32, pady=(28, 26))

        self._build_header(content)
        self._build_cards(content)
        self._build_action(content)

    def _build_header(self, parent):
        header = tk.Frame(parent, bg=theme.BG)
        header.pack(fill="x")
        titles = tk.Frame(header, bg=theme.BG)
        titles.pack(side="left")
        self.title_label = tk.Label(
            titles, text=self.PROFILE_NAME, font=theme.font(20, "bold"), fg=theme.TEXT, bg=theme.BG, anchor="w",
        )
        self.title_label.pack(fill="x")
        tk.Label(
            titles, text="Profile settings", font=theme.font(10), fg=theme.TEXT_MUTED, bg=theme.BG, anchor="w",
        ).pack(fill="x", pady=(2, 0))

        actions = tk.Frame(header, bg=theme.BG)
        actions.pack(side="right")
        self.status_pill = StatusPill(actions)
        self.status_pill.pack(side="right")
        self.save_button = FlatButton(actions, "Save", command=self._on_save, variant="ghost", pady=6)
        self.save_button.pack(side="right", padx=(0, 10))

    def _build_cards(self, parent):
        grid = tk.Frame(parent, bg=theme.BG)
        grid.pack(fill="x", pady=(24, 0))
        grid.grid_columnconfigure((0, 1), weight=1, uniform="cards")
        grid.grid_rowconfigure((0, 1), weight=1, uniform="rows")

        def place(card, row, column):
            card.grid(
                row=row, column=column, sticky="nsew",
                padx=(0, 8) if column == 0 else (8, 0), pady=(0, 16) if row == 0 else 0,
            )
            card.configure(height=124)
            card.pack_propagate(False)

        interval_card = Card(grid, "Interval")
        row = tk.Frame(interval_card.body, bg=theme.SURFACE)
        row.pack(fill="x")
        self.interval_entry = FlatEntry(row, width=9)
        self.interval_entry.insert(0, str(self.config["interval"]))
        self.interval_entry.configure(
            validate="key", validatecommand=(self.root.register(self._is_valid_interval), "%P"),
        )
        self.interval_entry.pack(side="left")
        tk.Label(row, text="seconds", font=theme.font(10), fg=theme.TEXT_MUTED, bg=theme.SURFACE).pack(side="left", padx=(10, 0))
        interval_card.add_hint("Delay between clicks · minimum 0.001")
        place(interval_card, 0, 0)

        mode_card = Card(grid, "Mode")
        self.mode_var = tk.StringVar(value=self.config["mode"])
        self.mode_control = SegmentedControl(mode_card.body, list(MODES), self.mode_var)
        self.mode_control.pack(fill="x")
        mode_card.add_hint("Click repeats · Hold keeps it pressed")
        place(mode_card, 0, 1)

        key_card = Card(grid, "Key / button")
        self.key_var = tk.StringVar(value=self.config["target_key"])
        self.key_combo = FlatCombobox(key_card.body, KEY_CHOICES, self.key_var)
        self.key_combo.pack(fill="x")
        key_card.add_hint("Mouse buttons start with mouse_")
        place(key_card, 1, 0)

        hotkey_card = Card(grid, "Hotkey")
        row = tk.Frame(hotkey_card.body, bg=theme.SURFACE)
        row.pack(fill="x")
        self.hotkey_keycap = Keycap(row, self.config["hotkey"])
        self.hotkey_keycap.pack(side="left")
        self.change_hotkey_button = FlatButton(
            row, "Change", command=self.controller.change_hotkey, variant="ghost", pady=6,
        )
        self.change_hotkey_button.pack(side="right")
        hotkey_card.add_hint("Works from any window")
        place(hotkey_card, 1, 1)

    def _build_action(self, parent):
        self.toggle_button = FlatButton(
            parent, "Start clicking", command=self.controller.toggle, variant="success",
            font=theme.font(12, "bold"), pady=16,
        )
        self.toggle_button.pack(fill="x", pady=(24, 0))
        self.hint_label = tk.Label(
            parent, font=theme.font(9), fg=theme.TEXT_MUTED, bg=theme.BG, anchor="center",
        )
        self.hint_label.pack(fill="x", pady=(12, 0))
        self._render_hint()


    def show_status(self, kind: str, message=None) -> None:
        running = kind == "running"
        self.status_pill.set_kind(kind)
        self.toggle_button.set_text("Stop clicking" if running else "Start clicking")
        self.toggle_button.set_variant("danger" if running else "success")
        self._error_text = message if kind == "error" else None
        self._render_hint()

    def show_hotkey(self, hotkey) -> None:
        self._hotkey = hotkey
        self.hotkey_keycap.set_text(hotkey or "-")
        self._render_hint()

    def show_hotkey_waiting(self) -> None:
        self.hotkey_keycap.set_waiting()

    def set_profile_title(self, name: str) -> None:
        self.title_label.configure(text=name)

    def set_inputs_enabled(self, enabled: bool) -> None:
        self.interval_entry.set_enabled(enabled)
        self.mode_control.set_enabled(enabled)
        self.key_combo.set_enabled(enabled)


    def _render_hint(self):
        if self._error_text:
            text = self._error_text
            if len(text) > MAX_MESSAGE_CHARS:
                text = text[:MAX_MESSAGE_CHARS - 1] + "…"
            self.hint_label.configure(text=text, fg=theme.WARNING)
        elif self._hotkey:
            self.hint_label.configure(text=f"Press {self._hotkey} from any window to start or stop", fg=theme.TEXT_MUTED)
        else:
            self.hint_label.configure(text="No hotkey set. Use Change to pick one", fg=theme.TEXT_MUTED)

    def _on_save(self):
        self.controller.save_settings(force=True)
        if self._save_reset_id is not None:
            self.root.after_cancel(self._save_reset_id)
        self.save_button.set_text("Saved")
        self._save_reset_id = self.root.after(1400, self._reset_save_button)

    def _reset_save_button(self):
        self._save_reset_id = None
        self.save_button.set_text("Save")
