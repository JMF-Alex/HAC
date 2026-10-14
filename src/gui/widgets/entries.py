import tkinter as tk

from gui import theme


class FlatEntry(tk.Entry):
    def __init__(self, parent, **kwargs):
        options = dict(
            bg=theme.SURFACE_2, fg=theme.TEXT, insertbackground=theme.TEXT, insertwidth=1,
            relief="flat", bd=6, highlightthickness=1,
            highlightbackground=theme.BORDER_STRONG, highlightcolor=theme.ACCENT,
            disabledbackground=theme.SURFACE_DISABLED, disabledforeground=theme.TEXT_FAINT,
            selectbackground=theme.ACCENT, selectforeground="#FFFFFF", font=theme.font(11),
        )
        options.update(kwargs)
        super().__init__(parent, **options)

    def set_enabled(self, enabled: bool) -> None:
        self.configure(state="normal" if enabled else "disabled")
