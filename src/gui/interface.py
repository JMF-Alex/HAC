import os
import sys
import tkinter as tk
from tkinter import ttk
import keyboard
from core.clicker import start_clicking, stop_clicking
from core.config import load_config, save_config

VERSION = "v0.5.0"

def run_app():
    global interval_entry, status_label, hotkey_label, current_hotkey, mode_var, key_var

    config = load_config()
    saved_interval = config.get("interval", 0.01)
    current_hotkey = config.get("hotkey", "F6")
    saved_mode = config.get("mode", "Click")
    saved_target = config.get("target_key", "left")

    def toggle_hotkey():
        if clicking_status():
            stop()
        else:
            start()

    def start():
        try:
            interval = float(interval_entry.get())
        except ValueError:
            interval = 0.01

        selected_mode = mode_var.get()
        selected_key = key_var.get()

        save_config({
            "interval": interval,
            "hotkey": current_hotkey,
            "mode": selected_mode,
            "target_key": selected_key
        })

        start_clicking(interval, selected_mode, selected_key)
        status_label.config(text="● Running", foreground="#4CAF50")

    def stop():
        stop_clicking()
        status_label.config(text="● Stopped", foreground="#F44336")

    def clicking_status():
        from core.clicker import clicking
        return clicking

    def update_hotkey_display():
        hotkey_label.config(text=f"Hotkey: {current_hotkey} to start/stop")

    def change_hotkey():
        nonlocal hotkey_waiting
        if hotkey_waiting:
            return
        hotkey_waiting = True
        hotkey_label.config(text="Press a key...", foreground="#FFC107")

        def on_key(event):
            nonlocal hotkey_waiting
            global current_hotkey
            new_key = event.name.upper()

            keyboard.unhook_all_hotkeys()
            keyboard.add_hotkey(new_key, toggle_hotkey)

            current_hotkey = new_key
            save_config({
                "hotkey": current_hotkey,
                "mode": mode_var.get(),
                "interval": float(interval_entry.get() or 0.01)
            })

            hotkey_waiting = False
            update_hotkey_display()
            hotkey_label.config(foreground="#BBBBBB")
            keyboard.unhook(on_key)

        keyboard.hook(on_key)

    root = tk.Tk()
    root.title("HAC Autoclicker")
    root.geometry("400x300")
    root.resizable(False, False)
    root.configure(bg="#1E1E1E")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Segoe UI", 10))
    style.configure("TEntry", fieldbackground="#2E2E2E", foreground="white", borderwidth=0, relief="flat")
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
    style.map("TButton", background=[("active", "#3A3A3A")], relief=[("pressed", "flat")])
    style.configure("Dark.TCombobox", fieldbackground="#2E2E2E", background="#2E2E2E", foreground="white", arrowcolor="white", borderwidth=0, relief="flat", padding=5, font=("Segoe UI", 10, "bold"))
    style.map("Dark.TCombobox", fieldbackground=[("readonly", "#2E2E2E"), ("focus", "#3A3A3A")])

    ttk.Label(root, text="Mode:").place(x=15, y=15)
    mode_var = tk.StringVar(value=saved_mode)
    mode_combo = ttk.Combobox(root, textvariable=mode_var, values=["Click", "Hold"], width=10, state="readonly", style="Dark.TCombobox")
    mode_combo.place(x=70, y=15)

    ttk.Label(root, text="Interval between clicks (seconds):").pack(pady=(60, 5))
    interval_entry = ttk.Entry(root, justify='center', width=10)
    interval_entry.insert(0, str(saved_interval))
    interval_entry.pack(ipady=3)

    button_frame = tk.Frame(root, bg="#1E1E1E")
    button_frame.pack(pady=15)

    start_btn = tk.Button(button_frame, text="Start", command=start, bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", activebackground="#45A049", width=10, height=1)
    start_btn.grid(row=0, column=0, padx=10)

    stop_btn = tk.Button(button_frame, text="Stop", command=stop, bg="#F44336", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", activebackground="#E53935", width=10, height=1)
    stop_btn.grid(row=0, column=1, padx=10)

    status_label = ttk.Label(root, text="● Stopped", foreground="#F44336", font=("Segoe UI", 11, "bold"))
    status_label.pack(pady=10)

    hotkey_label = ttk.Label(root, text=f"Hotkey: {current_hotkey} to start/stop", foreground="#BBBBBB")
    hotkey_label.pack(pady=(5, 2))

    hotkey_waiting = False
    change_btn = tk.Button(root, text="Change Hotkey", command=change_hotkey, bg="#3A3A3A", fg="white", relief="flat", activebackground="#555555", font=("Segoe UI", 9, "bold"), width=14)
    change_btn.place(relx=0.0, rely=1.0, x=10, y=-10, anchor="sw")

    keyboard.add_hotkey(current_hotkey, toggle_hotkey)

    version_label = ttk.Label(root, text=f"HAC Autoclicker {VERSION}", foreground="#777777", font=("Segoe UI", 8))
    version_label.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

    ttk.Label(root, text="Key/Button:").place(x=220, y=15)
    key_var = tk.StringVar(value=saved_target)
    key_combo = ttk.Combobox(
        root,
        textvariable=key_var,
        values=[
            "left", "right", "middle",
            "space", "shift", "ctrl", "alt",
            "enter", "tab", "up", "down", "left_arrow", "right_arrow",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
            "u", "v", "w", "x", "y", "z"
        ],
        width=12,
        state="readonly",
        style="Dark.TCombobox"
    )
    key_combo.place(x=300, y=15)

    def on_close():
        stop_clicking()
        keyboard.unhook_all_hotkeys()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.update_idletasks()
    width, height = 400, 300
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.iconbitmap(os.path.join(sys._MEIPASS, "assets", "icon.ico"))
    root.mainloop()
