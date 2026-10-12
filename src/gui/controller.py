import keyboard
import core.clicker as clicker
from core.config import save_config


class ClickerController:
    def __init__(self, root, interval_entry, mode_var, key_var, hotkey_label, status_label):
        self.root = root
        self.interval_entry = interval_entry
        self.mode_var = mode_var
        self.key_var = key_var
        self.hotkey_label = hotkey_label
        self.status_label = status_label
        self.current_hotkey = None
        self.hotkey_waiting = False

    def _on_hotkey(self):
        self.root.after(0, self.toggle)

    def set_hotkey(self, hotkey):
        self.current_hotkey = hotkey
        keyboard.add_hotkey(hotkey, self._on_hotkey)
        self.update_hotkey_display()

    def toggle(self):
        if clicker.is_clicking():
            self.stop()
        else:
            self.start()

    def _read_interval(self):
        try:
            return float(self.interval_entry.get())
        except ValueError:
            return 0.01

    def start(self):
        interval = self._read_interval()
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
            if event.event_type != "down":
                return
            keyboard.unhook(on_key)
            new_key = event.name.upper()
            self.root.after(0, lambda: self._apply_new_hotkey(new_key))

        keyboard.hook(on_key)

    def _apply_new_hotkey(self, new_key):
        keyboard.unhook_all_hotkeys()
        self.set_hotkey(new_key)
        save_config({
            "interval": self._read_interval(),
            "hotkey": new_key,
            "mode": self.mode_var.get(),
            "target_key": self.key_var.get()
        })
        self.hotkey_waiting = False
        self.hotkey_label.config(foreground="#BBBBBB")