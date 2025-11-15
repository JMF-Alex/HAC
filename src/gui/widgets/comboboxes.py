from tkinter import ttk

class CustomCombobox(ttk.Combobox):
    def __init__(self, parent, values, variable, width=10, style="Dark.TCombobox", x=None, y=None):
        super().__init__(parent, values=values, textvariable=variable, width=width, state="readonly", style=style)
        if x is not None and y is not None:
            self.place(x=x, y=y)
