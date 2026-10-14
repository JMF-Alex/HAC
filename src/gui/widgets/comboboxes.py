from tkinter import ttk

from gui import theme


class FlatCombobox(ttk.Combobox):
    def __init__(self, parent, values, variable, width=12, **kwargs):
        super().__init__(
            parent, values=list(values), textvariable=variable, width=width,
            state="readonly", style="Flat.TCombobox", font=theme.font(10), **kwargs,
        )
        self.bind("<<ComboboxSelected>>", lambda _e: self.selection_clear(), add="+")

    def set_enabled(self, enabled: bool) -> None:
        self.configure(state="readonly" if enabled else "disabled")
