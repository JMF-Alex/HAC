import tkinter as tk

class CustomButton(tk.Button):
    def __init__(self, parent, text, command, bg="#3A3A3A", fg="white", font=("Segoe UI", 10, "bold"), width=10, height=1, x=None, y=None, place_width=None, place_height=None):
        super().__init__(parent, text=text, command=command, bg=bg, fg=fg, font=font, width=width, height=height, relief="flat", activebackground="#555555")
        if x is not None and y is not None:
            place_args = {"x": x, "y": y}
            if place_width is not None:
                place_args["width"] = place_width
            if place_height is not None:
                place_args["height"] = place_height
            self.place(**place_args)
