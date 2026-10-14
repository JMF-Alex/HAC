import tkinter as tk

from gui import theme


class Card(tk.Frame):
    PAD = 20

    def __init__(self, parent, title: str):
        super().__init__(parent, bg=theme.SURFACE, highlightthickness=1, highlightbackground=theme.BORDER)
        tk.Label(
            self, text=title.upper(), font=theme.font(8, "bold"), fg=theme.TEXT_MUTED,
            bg=theme.SURFACE, anchor="w",
        ).pack(fill="x", padx=self.PAD, pady=(18, 0))
        self.body = tk.Frame(self, bg=theme.SURFACE)
        self.body.pack(fill="x", padx=self.PAD, pady=(12, 0))
        self._hint = None

    def add_hint(self, text: str) -> None:
        if self._hint is None:
            self._hint = tk.Label(
                self, font=theme.font(8), fg=theme.TEXT_FAINT, bg=theme.SURFACE,
                anchor="w", justify="left",
            )
            self._hint.pack(side="bottom", fill="x", padx=self.PAD, pady=(0, 16))
        self._hint.configure(text=text)
