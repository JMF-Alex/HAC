import tkinter as tk
from core.config import save_config

class FileMenu:
    def __init__(self, root, interval_entry, mode_var, key_var, controller):
        self.root = root
        self.interval_entry = interval_entry
        self.mode_var = mode_var
        self.key_var = key_var
        self.controller = controller
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)

        file_menu.add_command(label="Save", command=self.save_config)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def save_config(self):
        try:
            interval = float(self.interval_entry.get())
        except ValueError:
            interval = 0.01

        save_config({
            "interval": interval,
            "hotkey": self.controller.current_hotkey,
            "mode": self.mode_var.get(),
            "target_key": self.key_var.get()
        })
