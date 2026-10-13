import re
import tkinter as tk
from tkinter import ttk

from core.constants import KEY_CHOICES, MODES
from gui.widgets.buttons import CustomButton
from gui.widgets.comboboxes import CustomCombobox
from gui.widgets.labels import CustomLabel

_INTERVAL_RE = re.compile(r"^\d*[.,]?\d*$")


class LayoutManager:
    def __init__(self, root, controller, config):
        self.root = root
        self.controller = controller
        self.config = config
        self.setup_layout()

    @staticmethod
    def _is_valid_interval(proposed: str) -> bool:
        return _INTERVAL_RE.match(proposed) is not None

    def setup_layout(self):
        CustomLabel(self.root, "Interval between clicks (seconds):").pack(pady=(50, 5))

        self.interval_entry = ttk.Entry(self.root, justify="center", width=10)
        self.interval_entry.insert(0, str(self.config["interval"]))
        self.interval_entry.configure(
            validate="key",
            validatecommand=(self.root.register(self._is_valid_interval), "%P"),
        )
        self.interval_entry.pack(pady=(0, 5))

        self.mode_var = tk.StringVar(value=self.config["mode"])
        self.key_var = tk.StringVar(value=self.config["target_key"])

        button_frame = tk.Frame(self.root, bg="#1E1E1E")
        button_frame.pack(pady=15, padx=10)

        CustomLabel(self.root, "Mode:", x=15, y=15)
        self.mode_combo = CustomCombobox(self.root, list(MODES), self.mode_var, width=10, x=70, y=15)
        CustomLabel(self.root, "Key/Button:", x=220, y=15)
        self.key_combo = CustomCombobox(self.root, list(KEY_CHOICES), self.key_var, width=12, x=300, y=15)

        CustomButton(self.root, "Change Hotkey", self.controller.change_hotkey, x=10, y=260, place_width=120)
        CustomButton(button_frame, "Start", self.controller.start, bg="#4CAF50").pack(side="left", padx=(0, 10))
        CustomButton(button_frame, "Stop", self.controller.stop, bg="#F44336").pack(side="right", padx=(10, 0))

        self.status_label = ttk.Label(self.root, text="● Stopped", foreground="#F44336", font=("Segoe UI", 11, "bold"))
        self.status_label.pack(pady=2)
        self.hotkey_label = ttk.Label(self.root, text=f"Hotkey: {self.config['hotkey']} to start/stop", foreground="#BBBBBB")
        self.hotkey_label.pack(pady=(5, 2))

    def set_inputs_enabled(self, enabled: bool):
        self.interval_entry.config(state="normal" if enabled else "disabled")
        combo_state = "readonly" if enabled else "disabled"
        self.mode_combo.config(state=combo_state)
        self.key_combo.config(state=combo_state)
