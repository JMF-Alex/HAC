import logging
import threading

import keyboard

from core.config import save_config
from core.constants import DEFAULT_HOTKEY, DEFAULT_INTERVAL, MAX_INTERVAL, MIN_INTERVAL

logger = logging.getLogger(__name__)

SETTING_KEYS = ("interval", "hotkey", "mode", "target_key")

COLOR_RUNNING = "#4CAF50"
COLOR_STOPPED = "#F44336"
COLOR_ERROR = "#FF9800"
COLOR_WAITING = "#FFC107"
COLOR_IDLE_HINT = "#BBBBBB"


class ClickerController:
    STATUS_POLL_MS = 200

    def __init__(self, root, clicker, config):
        self.root = root
        self.clicker = clicker
        self.view = None
        self.current_hotkey = None
        self.hotkey_waiting = False
        self._initial_hotkey = config["hotkey"]
        self._hotkey_handle = None
        self._last_saved = {k: config[k] for k in SETTING_KEYS}
        self._error = None
        self._shown_status = None
        self._poll_id = None


    def bind_view(self, view):
        """`view` must expose interval_entry, mode_var, key_var, hotkey_label,
        status_label and set_inputs_enabled(bool)."""
        self.view = view
        if not self.set_hotkey(self._initial_hotkey) and self._initial_hotkey != DEFAULT_HOTKEY:
            self.set_hotkey(DEFAULT_HOTKEY)
        if self.current_hotkey is None:
            self.update_hotkey_display()
        self._refresh_status()
        self._poll_id = self.root.after(self.STATUS_POLL_MS, self._poll)


    def toggle(self):
        if self.clicker.is_clicking:
            self.stop()
        else:
            self.start()

    def start(self):
        interval, corrected = self._parse_interval()
        if corrected:
            self._show_interval(interval)
        try:
            self.clicker.start(interval, self.view.mode_var.get(), self.view.key_var.get())
        except Exception as exc:
            logger.exception("Could not start clicking")
            self._error = str(exc) or exc.__class__.__name__
        else:
            self._error = None
            self.save_settings()
        self._refresh_status()

    def stop(self):
        self.clicker.stop()
        self._refresh_status()


    def _on_hotkey(self):
        try:
            self.root.after(0, self.toggle)
        except RuntimeError:
            pass

    def set_hotkey(self, hotkey) -> bool:
        try:
            handle = keyboard.add_hotkey(hotkey, self._on_hotkey)
        except (ValueError, KeyError):
            logger.exception("Invalid hotkey %r", hotkey)
            self._error = f"Invalid hotkey: {hotkey}"
            self._refresh_status()
            return False
        self._remove_hotkey()
        self._hotkey_handle = handle
        self.current_hotkey = hotkey
        self.update_hotkey_display()
        return True

    def _remove_hotkey(self):
        if self._hotkey_handle is not None:
            try:
                keyboard.remove_hotkey(self._hotkey_handle)
            except (KeyError, ValueError):
                pass
            self._hotkey_handle = None

    def update_hotkey_display(self):
        if self.current_hotkey:
            text = f"Hotkey: {self.current_hotkey} to start/stop"
        else:
            text = "No hotkey set - use Change Hotkey"
        self.view.hotkey_label.config(text=text, foreground=COLOR_IDLE_HINT)

    def change_hotkey(self):
        if self.hotkey_waiting:
            return
        self.hotkey_waiting = True
        self.view.hotkey_label.config(text="Press a key...", foreground=COLOR_WAITING)
        captured = threading.Event()

        def on_key(event):
            if event.event_type != "down" or captured.is_set():
                return
            captured.set()
            keyboard.unhook(on_key)
            new_key = event.name.upper()
            try:
                self.root.after(0, lambda: self._apply_new_hotkey(new_key))
            except RuntimeError:
                pass

        keyboard.hook(on_key)

    def _apply_new_hotkey(self, new_key):
        self.hotkey_waiting = False
        if self.set_hotkey(new_key):
            self._error = None
            self.save_settings()
        else:
            self.update_hotkey_display()
        self._refresh_status()


    def _parse_interval(self):
        raw = self.view.interval_entry.get().strip().replace(",", ".")
        try:
            value = float(raw)
        except ValueError:
            return DEFAULT_INTERVAL, True
        clamped = min(MAX_INTERVAL, max(MIN_INTERVAL, value))
        return clamped, clamped != value

    def _show_interval(self, interval):
        entry = self.view.interval_entry
        entry.delete(0, "end")
        entry.insert(0, str(interval))

    def collect_settings(self) -> dict:
        return {
            "interval": self._parse_interval()[0],
            "hotkey": self.current_hotkey,
            "mode": self.view.mode_var.get(),
            "target_key": self.view.key_var.get(),
        }

    def save_settings(self, force=False):
        settings = self.collect_settings()
        if not force and settings == self._last_saved:
            return
        saved = save_config(settings)
        self._last_saved = {k: saved[k] for k in SETTING_KEYS}


    def _poll(self):
        self._refresh_status()
        self._poll_id = self.root.after(self.STATUS_POLL_MS, self._poll)

    def _refresh_status(self):
        running = self.clicker.is_clicking
        error = None if running else (self._error or self.clicker.last_error)
        state = (running, error)
        if state == self._shown_status:
            return
        self._shown_status = state

        label = self.view.status_label
        if running:
            label.config(text="● Running", foreground=COLOR_RUNNING)
        elif error:
            text = f"● Error: {error}"
            label.config(text=text if len(text) <= 46 else text[:45] + "…", foreground=COLOR_ERROR)
        else:
            label.config(text="● Stopped", foreground=COLOR_STOPPED)
        self.view.set_inputs_enabled(not running)


    def shutdown(self):
        if self._poll_id is not None:
            self.root.after_cancel(self._poll_id)
            self._poll_id = None
        self.clicker.stop()
        self.save_settings()
        self._remove_hotkey()
        try:
            keyboard.unhook_all()
        except Exception:
            logger.exception("Could not unhook keyboard")
