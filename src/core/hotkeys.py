import sys

if sys.platform == "win32":
    import keyboard as _kb

    add_hotkey = _kb.add_hotkey
    remove_hotkey = _kb.remove_hotkey
    hook = _kb.hook
    unhook = _kb.unhook
    unhook_all = _kb.unhook_all

else:
    import logging
    import threading
    from types import SimpleNamespace

    from pynput import keyboard as _pk

    logger = logging.getLogger(__name__)

    _lock = threading.RLock()
    _listener = None
    _hotkeys = {}
    _hooks = []
    _down = set()

    def _key_name(key):
        if isinstance(key, _pk.Key):
            return key.name
        char = getattr(key, "char", None)
        return char.lower() if char else None

    def _normalize(hotkey):
        name = hotkey.strip().lower()
        if len(name) == 1 or name in _pk.Key.__members__:
            return name
        raise ValueError(f"Unknown hotkey: {hotkey!r}")

    def _call(fn, *args):
        try:
            fn(*args)
        except Exception:
            logger.exception("Hotkey callback failed")

    def _on_press(key):
        name = _key_name(key)
        if name is None:
            return
        with _lock:
            if name in _down:
                return
            _down.add(name)
            hooks = list(_hooks)
            handles = list(_hotkeys.get(name, ()))
        event = SimpleNamespace(event_type="down", name=name)
        for fn in hooks:
            _call(fn, event)
        for _name, fn in handles:
            _call(fn)

    def _on_release(key):
        name = _key_name(key)
        if name is None:
            return
        with _lock:
            _down.discard(name)
            hooks = list(_hooks)
        event = SimpleNamespace(event_type="up", name=name)
        for fn in hooks:
            _call(fn, event)

    def _ensure_listener():
        global _listener
        with _lock:
            if _listener is None:
                _listener = _pk.Listener(on_press=_on_press, on_release=_on_release)
                _listener.daemon = True
                _listener.start()

    def add_hotkey(hotkey, callback, args=()):
        name = _normalize(hotkey)
        handle = (name, lambda: callback(*args))
        with _lock:
            _hotkeys.setdefault(name, []).append(handle)
        _ensure_listener()
        return handle

    def remove_hotkey(handle):
        name = handle[0]
        with _lock:
            handles = _hotkeys.get(name, [])
            if handle not in handles:
                raise KeyError(handle)
            handles.remove(handle)
            if not handles:
                del _hotkeys[name]

    def hook(callback):
        with _lock:
            _hooks.append(callback)
        _ensure_listener()
        return callback

    def unhook(callback):
        with _lock:
            try:
                _hooks.remove(callback)
            except ValueError:
                pass

    def unhook_all():
        global _listener
        with _lock:
            _hotkeys.clear()
            _hooks.clear()
            _down.clear()
            listener, _listener = _listener, None
        if listener is not None:
            listener.stop()