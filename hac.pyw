import ctypes
import threading
import keyboard
import time
import tkinter as tk

clicking = False
SendInput = ctypes.windll.user32.SendInput

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP   = 0x0004

def click():
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def clicker(interval):
    global clicking
    while clicking:
        click()
        if interval > 0:
            time.sleep(interval)

def start_clicking():
    global clicking
    if not clicking:
        clicking = True
        interval = float(interval_entry.get())
        threading.Thread(target=clicker, args=(interval,), daemon=True).start()
        status_label.config(text="Status: Clicking", fg="green")

def stop_clicking():
    global clicking
    clicking = False
    status_label.config(text="Status: Stopped", fg="red")

def toggle_hotkey():
    if clicking:
        stop_clicking()
    else:
        start_clicking()

root = tk.Tk()
root.title("HAC")
root.geometry("400x250")
root.resizable(False, False)

tk.Label(root, text="Interval between clicks (seconds):").pack(pady=5)
interval_entry = tk.Entry(root, justify='center')
interval_entry.insert(0, "0.01")
interval_entry.pack()

tk.Button(root, text="Start", command=start_clicking, bg="#4CAF50").pack(pady=5)
tk.Button(root, text="Stop", command=stop_clicking, bg="#F44336").pack(pady=5)

status_label = tk.Label(root, text="Status: Stopped", fg="red")
status_label.pack(pady=10)

tk.Label(root, text="Hotkey: F6 to start/stop").pack(pady=5)

keyboard.add_hotkey('F6', toggle_hotkey)

root.mainloop()
