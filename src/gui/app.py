import logging
import tkinter as tk
from tkinter import ttk

from core import timer_resolution
from core.clicker import Clicker
from core.config import load_config
from core.paths import resource_path
from gui.controller import ClickerController
from gui.layout import LayoutManager
from gui.menu.file_menu import FileMenu

logger = logging.getLogger(__name__)


class HACApp:
    VERSION = "v0.6.3"
    WIDTH, HEIGHT = 400, 300

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HAutoClicker")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg="#1E1E1E")
        self.root.report_callback_exception = self._log_tk_exception
        self.apply_styles()
        self.config = load_config()
        self._timer_resolution_on = timer_resolution.begin(1)
        self.clicker = Clicker()
        self.controller = None
        self.layout = None
        self.init_app()

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Segoe UI", 10))
        style.configure("TEntry", fieldbackground="#2E2E2E", foreground="white", borderwidth=0, relief="flat")
        style.map("TEntry", fieldbackground=[("disabled", "#252525")], foreground=[("disabled", "#777777")])
        style.configure("Dark.TCombobox", fieldbackground="#2E2E2E", background="#2E2E2E", foreground="white", arrowcolor="white", borderwidth=0, relief="flat", padding=5, font=("Segoe UI", 10, "bold"))
        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", "#2E2E2E"), ("focus", "#3A3A3A"), ("disabled", "#252525")],
            foreground=[("disabled", "#777777")],
        )
        self.root.option_add("*TCombobox*Listbox.background", "#2E2E2E")
        self.root.option_add("*TCombobox*Listbox.foreground", "white")
        self.root.option_add("*TCombobox*Listbox.selectBackground", "#4CAF50")
        self.root.option_add("*TCombobox*Listbox.selectForeground", "white")

    def init_app(self):
        self.controller = ClickerController(self.root, self.clicker, self.config)
        self.layout = LayoutManager(self.root, self.controller, self.config)
        self.controller.bind_view(self.layout)

        FileMenu(self.root, self.controller, on_exit=self.on_close)

        version_label = ttk.Label(self.root, text=f"HAC Autoclicker {self.VERSION}", foreground="#777777", font=("Segoe UI", 8))
        version_label.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

        self.center_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.HEIGHT // 2)
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

    def on_close(self):
        self.controller.shutdown()
        if self._timer_resolution_on:
            timer_resolution.end(1)
            self._timer_resolution_on = False
        self.root.destroy()

    def _set_icon(self):
        try:
            self.root.iconbitmap(resource_path("assets", "icon.ico"))
        except tk.TclError:
            logger.warning("Window icon not found or unsupported on this platform")

    @staticmethod
    def _log_tk_exception(exc_type, exc, tb):
        logger.error("Unhandled error in a Tk callback", exc_info=(exc_type, exc, tb))

    def run(self):
        self._set_icon()
        self.root.mainloop()
