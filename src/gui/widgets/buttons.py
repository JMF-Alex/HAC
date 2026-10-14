import tkinter as tk

from gui import theme

_STYLES = {
    "primary": dict(bg=theme.ACCENT, hover=theme.ACCENT_HOVER, active=theme.ACCENT_ACTIVE, fg="#FFFFFF", border=None),
    "success": dict(bg=theme.SUCCESS, hover=theme.SUCCESS_HOVER, active=theme.SUCCESS_ACTIVE, fg="#06180F", border=None),
    "danger": dict(bg=theme.DANGER, hover=theme.DANGER_HOVER, active=theme.DANGER_ACTIVE, fg="#FFFFFF", border=None),
    "ghost": dict(bg=None, hover=theme.SURFACE_HOVER, active=theme.SURFACE_2, fg=theme.TEXT, border=theme.BORDER_STRONG),
    "ghost_danger": dict(bg=None, hover=theme.DANGER_SOFT, active=theme.DANGER_SOFT, fg="#F2777B", border=theme.BORDER_STRONG),
    "subtle": dict(bg=theme.SURFACE_2, hover=theme.SURFACE_HOVER, active=theme.SURFACE, fg=theme.TEXT_MUTED, border=None),
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
            bd=0, highlightthickness=1, takefocus=0, **kwargs,
        )
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
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
        if fire and self.command is not None:
            self.command()

    def _paint(self):
        style = _STYLES[self._variant]
        if not self._enabled:
            bg, fg, border = theme.SURFACE_2, theme.TEXT_FAINT, theme.BORDER
        else:
            base = style["bg"] or self._base_bg
            if self._pressed and self._hover:
                bg = style["active"]
            elif self._hover:
                bg = style["hover"]
            else:
                bg = base
            fg = style["fg"]
            border = style["border"] or bg
        self.configure(bg=bg, fg=fg, highlightbackground=border, cursor="hand2" if self._enabled else "arrow")
