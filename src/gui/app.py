import os
import sys
import tkinter as tk
from tkinter import ttk
from core.config import load_config
from gui.controller import ClickerController
from gui.menu.file_menu import FileMenu
from gui.layout import LayoutManager

class HACApp:
    VERSION = "v0.6.0"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HAutoClicker")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg="#1E1E1E")
        self.apply_styles()
        self.config = load_config()
        self.layout = None
        self.controller = None
        self.init_app()

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Segoe UI", 10))
        style.configure("TEntry", fieldbackground="#2E2E2E", foreground="white", borderwidth=0, relief="flat")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.map("TButton", background=[("active", "#3A3A3A")], relief=[("pressed", "flat")])
        style.configure("Dark.TCombobox", fieldbackground="#2E2E2E", background="#2E2E2E", foreground="white", arrowcolor="white", borderwidth=0, relief="flat", padding=5, font=("Segoe UI", 10, "bold"))
        style.map("Dark.TCombobox", fieldbackground=[("readonly", "#2E2E2E"), ("focus", "#3A3A3A")])

    def init_app(self):
        self.controller = ClickerController(None, None, None, None, None)

        self.layout = LayoutManager(self.root, self.controller, self.config)

        self.controller.interval_entry = self.layout.interval_entry
        self.controller.mode_var = self.layout.mode_var
        self.controller.key_var = self.layout.key_var
        self.controller.hotkey_label = self.layout.hotkey_label
        self.controller.status_label = self.layout.status_label

        self.controller.set_hotkey(self.config.get("hotkey", "F6"))

        self.layout.controller = self.controller

        FileMenu(self.root, self.layout.interval_entry, self.layout.mode_var, self.layout.key_var, self.controller)

        version_label = ttk.Label(self.root, text=f"HAC Autoclicker {self.VERSION}", foreground="#777777", font=("Segoe UI", 8))
        version_label.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

        self.center_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def center_window(self):
        self.root.update_idletasks()
        width, height = 400, 300
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def on_close(self):
        self.controller.stop()
        self.root.destroy()

    def run(self):
        try:
            self.root.iconbitmap(os.path.join(sys._MEIPASS, "assets", "icon.ico"))
        except Exception:
            pass
        self.root.mainloop()
