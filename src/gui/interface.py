import tkinter as tk
from tkinter import ttk
import keyboard
from core.clicker import start_clicking, stop_clicking

VERSION = "v0.2.0"

def run_app():
    global interval_entry, status_label

    def toggle_hotkey():
        if clicking_status():
            stop()
        else:
            start()

    def start():
        interval = float(interval_entry.get())
        start_clicking(interval)
        status_label.config(text="● Clicking", foreground="#4CAF50")

    def stop():
        stop_clicking()
        status_label.config(text="● Stopped", foreground="#F44336")

    def clicking_status():
        from core.clicker import clicking
        return clicking

    root = tk.Tk()
    root.title("HAC Autoclicker")
    root.geometry("400x260")
    root.resizable(False, False)
    root.configure(bg="#1E1E1E")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Segoe UI", 10))
    style.configure("TEntry", fieldbackground="#2E2E2E", foreground="white", borderwidth=0, relief="flat")
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
    style.map("TButton", background=[("active", "#3A3A3A")], relief=[("pressed", "flat")])

    ttk.Label(root, text="Interval between clicks (seconds):").pack(pady=(20, 5))

    interval_entry = ttk.Entry(root, justify='center', width=10)
    interval_entry.insert(0, "0.01")
    interval_entry.pack(ipady=3)

    button_frame = tk.Frame(root, bg="#1E1E1E")
    button_frame.pack(pady=15)

    start_btn = tk.Button(button_frame, text="Start", command=start, bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", activebackground="#45A049", width=10, height=1)
    start_btn.grid(row=0, column=0, padx=10)

    stop_btn = tk.Button(button_frame, text="Stop", command=stop, bg="#F44336", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", activebackground="#E53935", width=10, height=1)
    stop_btn.grid(row=0, column=1, padx=10)

    status_label = ttk.Label(root, text="● Stopped", foreground="#F44336", font=("Segoe UI", 11, "bold"))
    status_label.pack(pady=10)

    ttk.Label(root, text="Hotkey: F6 to start/stop", foreground="#BBBBBB").pack(pady=5)

    keyboard.add_hotkey('F6', toggle_hotkey)

    version_label = ttk.Label(root, text=f"HAC Autoclicker {VERSION}", foreground="#777777", font=("Segoe UI", 8))
    version_label.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

    root.update_idletasks()
    width, height = 400, 260
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.mainloop()
