import tkinter as tk
from dataclasses import dataclass

from gui import theme
from gui.widgets.buttons import FlatButton


def format_interval(seconds: float) -> str:
    return f"{seconds * 1000:g} ms" if seconds < 1 else f"{seconds:g} s"


@dataclass(frozen=True)
class ProfileSummary:
    name: str
    hotkey: str
    interval: float
    mode: str
    key: str

    @classmethod
    def from_config(cls, name: str, config: dict) -> "ProfileSummary":
        return cls(name, config["hotkey"], config["interval"], config["mode"], config["target_key"])

    @property
    def subtitle(self) -> str:
        return " · ".join((self.hotkey, self.mode, self.key, format_interval(self.interval)))


def _is_inside(widget, container) -> bool:
    return widget is not None and (str(widget) == str(container) or str(widget).startswith(str(container) + "."))


class ProfileItem(tk.Frame):
    def __init__(self, parent, summary: ProfileSummary, selected: bool, on_click):
        super().__init__(parent, bg=theme.SIDEBAR, cursor="hand2")
        self.summary = summary
        self.selected = selected
        self._hover = False
        self._on_click = on_click

        self._bar = tk.Frame(self, width=3, bg=theme.SIDEBAR)
        self._bar.pack(side="left", fill="y")
        text_box = tk.Frame(self, bg=theme.SIDEBAR)
        text_box.pack(side="left", fill="both", expand=True, padx=(12, 10), pady=9)
        self._name = tk.Label(text_box, text=summary.name, font=theme.font(10, "bold"), anchor="w")
        self._name.pack(fill="x")
        self._sub = tk.Label(text_box, text=summary.subtitle, font=theme.font(8), anchor="w")
        self._sub.pack(fill="x", pady=(2, 0))
        self._text_box = text_box

        self._bind_tree(self)
        self._paint()

    def set_selected(self, selected: bool) -> None:
        self.selected = selected
        self._paint()

    def _bind_tree(self, widget):
        widget.bind("<Enter>", self._on_enter, add="+")
        widget.bind("<Leave>", self._on_leave, add="+")
        widget.bind("<ButtonRelease-1>", self._on_release, add="+")
        for child in widget.winfo_children():
            self._bind_tree(child)

    def _on_enter(self, _event):
        self._hover = True
        self._paint()

    def _on_leave(self, _event):
        self.after(15, self._sync_hover)

    def _sync_hover(self):
        try:
            under_pointer = self.winfo_containing(*self.winfo_pointerxy())
        except (tk.TclError, KeyError):
            return
        hover = _is_inside(under_pointer, self)
        if hover != self._hover:
            self._hover = hover
            self._paint()

    def _on_release(self, _event):
        if self._on_click is not None:
            self._on_click(self.summary.name)

    def _paint(self):
        if self.selected:
            bg, bar = theme.ACCENT_SOFT, theme.ACCENT
            name_fg, sub_fg = theme.TEXT, theme.TEXT_MUTED
        elif self._hover:
            bg, bar = theme.SURFACE, theme.SIDEBAR
            name_fg, sub_fg = theme.TEXT, theme.TEXT_MUTED
        else:
            bg, bar = theme.SIDEBAR, theme.SIDEBAR
            name_fg, sub_fg = theme.TEXT_SOFT, theme.TEXT_FAINT
        self.configure(bg=bg)
        self._bar.configure(bg=bar)
        self._text_box.configure(bg=bg)
        self._name.configure(bg=bg, fg=name_fg)
        self._sub.configure(bg=bg, fg=sub_fg)


class ProfileSidebar(tk.Frame):
    WIDTH = 260

    def __init__(self, parent, app_name: str, version: str,
                 on_select=None, on_add=None, on_rename=None, on_delete=None):
        super().__init__(parent, bg=theme.SIDEBAR, width=self.WIDTH)
        self.pack_propagate(False)
        self._on_select = on_select
        self._on_add = on_add
        self._on_rename = on_rename
        self._on_delete = on_delete
        self._active = None
        self._items = {}

        self._build_header(app_name, version)
        self._divider().pack(fill="x")
        self._build_caption()

        self._list = tk.Frame(self, bg=theme.SIDEBAR)
        self._list.pack(fill="x", padx=10)
        self._empty = tk.Label(
            self._list, text="No profiles yet", font=theme.font(9), fg=theme.TEXT_FAINT,
            bg=theme.SIDEBAR, anchor="w",
        )

        self._build_footer()


    @property
    def profile_names(self):
        return list(self._items)

    @property
    def active(self):
        return self._active

    def set_profiles(self, profiles, active=None) -> None:
        for item in self._items.values():
            item.destroy()
        self._items = {}
        self._empty.pack_forget()
        profiles = list(profiles)
        self._active = active if active in {p.name for p in profiles} else None
        for profile in profiles:
            item = ProfileItem(self._list, profile, profile.name == self._active, self._handle_select)
            item.pack(fill="x", pady=1)
            self._items[profile.name] = item
        if not profiles:
            self._empty.pack(fill="x", padx=12, pady=8)
        self._sync_footer()

    def set_active(self, name) -> None:
        self._active = name if name in self._items else None
        for item_name, item in self._items.items():
            item.set_selected(item_name == self._active)
        self._sync_footer()


    def _divider(self):
        return tk.Frame(self, height=1, bg=theme.BORDER)

    def _build_header(self, app_name, version):
        header = tk.Frame(self, bg=theme.SIDEBAR)
        header.pack(fill="x", padx=18, pady=(22, 18))
        tk.Label(
            header, text="H", font=theme.font(14, "bold"), fg="#FFFFFF", bg=theme.ACCENT, width=2, pady=3,
        ).pack(side="left")
        titles = tk.Frame(header, bg=theme.SIDEBAR)
        titles.pack(side="left", padx=(12, 0))
        tk.Label(titles, text=app_name, font=theme.font(12, "bold"), fg=theme.TEXT, bg=theme.SIDEBAR, anchor="w").pack(fill="x")
        tk.Label(titles, text=version, font=theme.font(8), fg=theme.TEXT_FAINT, bg=theme.SIDEBAR, anchor="w").pack(fill="x")

    def _build_caption(self):
        caption = tk.Frame(self, bg=theme.SIDEBAR)
        caption.pack(fill="x", padx=18, pady=(18, 8))
        tk.Label(
            caption, text="PROFILES", font=theme.font(8, "bold"), fg=theme.TEXT_MUTED, bg=theme.SIDEBAR,
        ).pack(side="left")
        self.add_button = FlatButton(
            caption, "+", command=self._handle_add, variant="subtle",
            font=theme.font(11, "bold"), padx=9, pady=0,
        )
        self.add_button.pack(side="right")

    def _build_footer(self):
        footer = tk.Frame(self, bg=theme.SIDEBAR)
        footer.pack(side="bottom", fill="x")
        self._divider().pack(in_=footer, fill="x")
        buttons = tk.Frame(footer, bg=theme.SIDEBAR)
        buttons.pack(fill="x", padx=18, pady=16)
        buttons.grid_columnconfigure((0, 1), weight=1, uniform="footer")
        self.rename_button = FlatButton(buttons, "Rename", command=self._handle_rename, variant="ghost", pady=6)
        self.rename_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.delete_button = FlatButton(buttons, "Delete", command=self._handle_delete, variant="ghost_danger", pady=6)
        self.delete_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def _sync_footer(self):
        has_selection = self._active is not None
        self.rename_button.set_enabled(has_selection)
        self.delete_button.set_enabled(has_selection)


    def _handle_select(self, name):
        if self._on_select is not None:
            self._on_select(name)

    def _handle_add(self):
        if self._on_add is not None:
            self._on_add()

    def _handle_rename(self):
        if self._on_rename is not None and self._active is not None:
            self._on_rename(self._active)

    def _handle_delete(self):
        if self._on_delete is not None and self._active is not None:
            self._on_delete(self._active)
