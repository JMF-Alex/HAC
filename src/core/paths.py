import os
import sys

from core.constants import APP_NAME


def user_data_dir() -> str:
    """Folder for the config file and the log. HAC_CONFIG_DIR overrides it."""
    override = os.environ.get("HAC_CONFIG_DIR")
    if override:
        return override
    if sys.platform == "win32":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    else:
        base = os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, APP_NAME)


def resource_path(*parts: str) -> str:
    """Path to a bundled resource, both from source and from a PyInstaller build."""
    base = getattr(sys, "_MEIPASS", None)
    if base is None:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *parts)
