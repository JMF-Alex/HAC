import keyboard
import core.clicker as clicker
from core.config import save_config

class ClickerController:
    def __init__(self, interval_entry, mode_var, key_var, hotkey_label, status_label):
        self.interval_entry = interval_entry
        self.mode_var = mode_var
        self.key_var = key_var
        self.hotkey_label = hotkey_label
        self.status_label = status_label
        self.current_hotkey = None
        self.hotkey_waiting = False

    def set_hotkey(self, hotkey):
        self.current_hotkey = hotkey
        keyboard.add_hotkey(hotkey, self.toggle)
        self.update_hotkey_display()

    def toggle(self):
        if clicker.clicking:
            self.stop()
        else:
            self.start()

    def start(self):
        try:
            interval = float(self.interval_entry.get())
        except ValueError:
            interval = 0.01

        mode = self.mode_var.get()
        key = self.key_var.get()

        save_config({
            "interval": interval,
            "hotkey": self.current_hotkey,
            "mode": mode,
            "target_key": key
        })

        clicker.start_clicking(interval, mode, key)
        self.status_label.config(text="● Running", foreground="#4CAF50")

    def stop(self):
        clicker.stop_clicking()
        self.status_label.config(text="● Stopped", foreground="#F44336")

    def update_hotkey_display(self):
        self.hotkey_label.config(text=f"Hotkey: {self.current_hotkey} to start/stop")

    def change_hotkey(self):
        if self.hotkey_waiting:
            return
        self.hotkey_waiting = True
        self.hotkey_label.config(text="Press a key...", foreground="#FFC107")

        def on_key(event):
            new_key = event.name.upper()
            keyboard.unhook_all_hotkeys()
            keyboard.add_hotkey(new_key, self.toggle)
            self.current_hotkey = new_key
            save_config({
                "hotkey": new_key,
                "mode": self.mode_var.get(),
                "interval": float(self.interval_entry.get() or 0.01)
            })
            self.hotkey_waiting = False
            self.update_hotkey_display()
            self.hotkey_label.config(foreground="#BBBBBB")
            keyboard.unhook(on_key)

        keyboard.hook(on_key)
