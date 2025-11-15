from gui.widgets.labels import CustomLabel
from gui.widgets.buttons import CustomButton
from gui.widgets.comboboxes import CustomCombobox
import tkinter as tk
from tkinter import ttk

class LayoutManager:
    def __init__(self, root, controller, config):
        self.root = root
        self.controller = controller
        self.config = config
        self.setup_layout()

    def setup_layout(self):
        CustomLabel(self.root, "Interval between clicks (seconds):", x=None, y=None).pack(pady=(50, 5))

        self.interval_entry = ttk.Entry(self.root, justify='center', width=10)
        self.interval_entry.insert(0, str(self.config.get("interval", 0.01)))
        self.interval_entry.pack(pady=(0, 5))

        self.mode_var = tk.StringVar(value=self.config.get("mode", "Click"))
        self.key_var = tk.StringVar(value=self.config.get("target_key", "left"))

        button_frame = tk.Frame(self.root, bg="#1E1E1E")
        button_frame.pack(pady=15, padx=10)

        CustomLabel(self.root, "Mode:", x=15, y=15)
        CustomCombobox(self.root, ["Click", "Hold"], self.mode_var, width=10, x=70, y=15)
        CustomLabel(self.root, "Key/Button:", x=220, y=15)
        CustomCombobox(self.root, [
            "left","right","middle","space","shift","ctrl","alt",
            "enter","tab","up","down","left_arrow","right_arrow",
            *[chr(i) for i in range(97,123)]
        ], self.key_var, width=12, x=300, y=15)

        CustomButton(self.root, "Change Hotkey", self.controller.change_hotkey, x=10, y=260, place_width=120)
        CustomButton(button_frame, "Start", self.controller.start, bg="#4CAF50").pack(side="left", padx=(0,10))
        CustomButton(button_frame, "Stop", self.controller.stop, bg="#F44336").pack(side="right", padx=(10,0))

        self.status_label = ttk.Label(self.root, text="● Stopped", foreground="#F44336", font=("Segoe UI", 11, "bold"))
        self.status_label.pack(pady=2)
        self.hotkey_label = ttk.Label(self.root, text=f"Hotkey: {self.config.get('hotkey','F6')} to start/stop", foreground="#BBBBBB")
        self.hotkey_label.pack(pady=(5,2))
