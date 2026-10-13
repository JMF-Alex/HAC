import tkinter as tk


class FileMenu:
    def __init__(self, root, controller, on_exit):
        self.root = root
        self.controller = controller
        self.on_exit = on_exit
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)

        file_menu.add_command(label="Save", command=lambda: self.controller.save_settings(force=True))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_exit)

        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)
