from tkinter import ttk

class CustomLabel(ttk.Label):
    def __init__(self, parent, text, x=None, y=None, **kwargs):
        super().__init__(parent, text=text, **kwargs)
        if x is not None and y is not None:
            self.place(x=x, y=y)
