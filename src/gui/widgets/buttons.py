import tkinter as tk

from gui import theme

_STYLES = {
    "primary": dict(bg=theme.ACCENT, hover=theme.ACCENT_HOVER, active=theme.ACCENT_ACTIVE, fg=theme.ACCENT_TEXT, border=None),
    "danger": dict(bg=theme.DANGER, hover=theme.DANGER_HOVER, active=theme.DANGER_ACTIVE, fg="#FFFFFF", border=None),
    "ghost": dict(bg=None, hover=theme.SURFACE_HOVER, active=theme.SURFACE_2, fg=theme.TEXT, border=theme.BORDER_STRONG),
    "subtle": dict(bg=theme.SURFACE_2, hover=theme.SURFACE_HOVER, active=theme.SURFACE, fg=theme.TEXT_MUTED, hover_fg=theme.TEXT, border=None),
    "quiet": dict(bg=None, hover=theme.SURFACE_HOVER, active=theme.SURFACE_2, fg=theme.TEXT_MUTED, hover_fg=theme.TEXT, border=None),
    "quiet_danger": dict(bg=None, hover=theme.DANGER_SOFT, active=theme.DANGER_SOFT, fg=theme.TEXT_MUTED, hover_fg=theme.DANGER_TEXT, border=None),
}


class FlatButton(tk.Label):
    def __init__(self, parent, text, command=None, variant="ghost", font=None, padx=14, pady=7, **kwargs):
        if variant not in _STYLES:
            raise ValueError(f"Unknown button variant: {variant!r}")
        self.command = command
        self._variant = variant
        self._enabled = True
        self._hover = False
        self._pressed = False
        self._base_bg = parent.cget("bg")
        super().__init__(
            parent, text=text, font=font or theme.font(10, "bold"), padx=padx, pady=pady,
            bd=0, highlightthickness=1, highlightcolor=theme.TEXT, takefocus=1, **kwargs,
        )
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Key-space>", self._on_key)
        self.bind("<Key-Return>", self._on_key)
        self._paint()


    def set_text(self, text: str) -> None:
        self.configure(text=text)

    def set_variant(self, variant: str) -> None:
        if variant not in _STYLES:
            raise ValueError(f"Unknown button variant: {variant!r}")
        self._variant = variant
        self._paint()

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = bool(enabled)
        if not self._enabled:
            self._hover = self._pressed = False
        self.configure(takefocus=1 if self._enabled else 0)
        self._paint()


    def _on_enter(self, _event):
        self._hover = True
        self._paint()

    def _on_leave(self, _event):
        self._hover = False
        self._paint()

    def _on_press(self, _event):
        if self._enabled:
            self._pressed = True
            self._paint()

    def _on_release(self, _event):
        fire = self._pressed and self._hover and self._enabled
        self._pressed = False
        self._paint()
        if fire:
            self._invoke()

    def _on_key(self, _event):
        if self._enabled:
            self._invoke()
        return "break"

    def _invoke(self):
        if self.command is not None:
            self.command()

    def _paint(self):
        style = _STYLES[self._variant]
        base = style["bg"] or self._base_bg
        if not self._enabled:
            flat = style["bg"] is None and style["border"] is None
            bg = base if flat else theme.SURFACE_2
            fg = theme.TEXT_DISABLED
            border = base if flat else theme.BORDER
        else:
            if self._pressed and self._hover:
                bg = style["active"]
            elif self._hover:
                bg = style["hover"]
            else:
                bg = base
            fg = style.get("hover_fg", style["fg"]) if self._hover else style["fg"]
            border = style["border"] or bg
        self.configure(bg=bg, fg=fg, highlightbackground=border, cursor="hand2" if self._enabled else "arrow")
