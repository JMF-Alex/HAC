import tkinter as tk

from gui import theme


class Keycap(tk.Frame):
    WAITING_TEXT = "Press a key"

    def __init__(self, parent, text: str = "-"):
        super().__init__(parent, bg=theme.KEY_EDGE)
        self._label = tk.Label(
            self, text=text, font=theme.mono(12, "bold"), fg=theme.TEXT, bg=theme.KEY_FACE,
            padx=16, pady=6, bd=0,
        )
        self._label.pack(padx=1, pady=(1, 3))

    def set_text(self, text: str) -> None:
        self._set_waiting(False)
        self._label.configure(text=text)

    def set_waiting(self) -> None:
        self._set_waiting(True)
        self._label.configure(text=self.WAITING_TEXT)

    @property
    def text(self) -> str:
        return self._label.cget("text")

    def _set_waiting(self, waiting: bool) -> None:
        self.configure(bg=theme.WARNING_EDGE if waiting else theme.KEY_EDGE)
        self._label.configure(fg=theme.WARNING if waiting else theme.TEXT)


class StatusPill(tk.Frame):
    KINDS = {
        "running": (theme.SUCCESS, "Running"),
        "stopped": (theme.TEXT_MUTED, "Stopped"),
        "error": (theme.WARNING, "Error"),
    }

    def __init__(self, parent):
        super().__init__(parent, bg=theme.SURFACE, highlightthickness=1, highlightbackground=theme.BORDER)
        self._dot = tk.Label(self, text="●", font=theme.font(9), bg=theme.SURFACE)
        self._dot.pack(side="left", padx=(12, 6), pady=6)
        self._text = tk.Label(self, font=theme.font(10, "bold"), fg=theme.TEXT, bg=theme.SURFACE, width=8, anchor="w")
        self._text.pack(side="left", padx=(0, 14), pady=6)
        self.kind = None
        self.set_kind("stopped")

    def set_kind(self, kind: str) -> None:
        if kind not in self.KINDS:
            raise ValueError(f"Unknown status kind: {kind!r}")
        color, text = self.KINDS[kind]
        self.kind = kind
        self._dot.configure(fg=color)
        self._text.configure(text=text)

    @property
    def text(self) -> str:
        return self._text.cget("text")
