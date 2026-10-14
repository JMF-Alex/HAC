import tkinter as tk

from gui import theme


class SegmentedControl(tk.Frame):
    def __init__(self, parent, options, variable, font=None):
        super().__init__(parent, bg=theme.SURFACE_2, highlightthickness=1, highlightbackground=theme.BORDER_STRONG)
        self._variable = variable
        self._enabled = True
        self._hovered = None
        self._segments = {}
        for column, option in enumerate(options):
            segment = tk.Label(self, text=option, font=font or theme.font(10, "bold"), padx=14, pady=6, bd=0)
            segment.grid(row=0, column=column, sticky="nsew", padx=2, pady=2)
            self.grid_columnconfigure(column, weight=1, uniform="segments")
            segment.bind("<Enter>", lambda _e, o=option: self._set_hover(o))
            segment.bind("<Leave>", lambda _e: self._set_hover(None))
            segment.bind("<ButtonRelease-1>", lambda _e, o=option: self._choose(o))
            self._segments[option] = segment

        self._trace_id = variable.trace_add("write", lambda *_: self._paint())
        self.bind("<Destroy>", self._on_destroy, add="+")
        self._paint()

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = bool(enabled)
        self._hovered = None
        self._paint()

    def _on_destroy(self, event):
        if event.widget is self:
            try:
                self._variable.trace_remove("write", self._trace_id)
            except Exception:
                pass

    def _set_hover(self, option):
        self._hovered = option
        self._paint()

    def _choose(self, option):
        if self._enabled:
            self._variable.set(option)

    def _paint(self):
        selected = self._variable.get()
        for option, segment in self._segments.items():
            if option == selected:
                if self._enabled:
                    bg, fg = theme.ACCENT, theme.ACCENT_TEXT
                else:
                    bg, fg = theme.ACCENT_DISABLED, theme.ACCENT_DISABLED_TEXT
            elif not self._enabled:
                bg, fg = theme.SURFACE_2, theme.TEXT_DISABLED
            elif option == self._hovered:
                bg, fg = theme.SURFACE_HOVER, theme.TEXT
            else:
                bg, fg = theme.SURFACE_2, theme.TEXT_MUTED
            segment.configure(bg=bg, fg=fg, cursor="hand2" if self._enabled else "arrow")
