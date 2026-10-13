import json
import logging
import math
import os

from core.constants import (
    DEFAULT_HOTKEY,
    DEFAULT_INTERVAL,
    DEFAULT_TARGET_KEY,
    KEY_CHOICES,
    MAX_INTERVAL,
    MIN_INTERVAL,
    MODE_CLICK,
    MODES,
)
from core.paths import user_data_dir

logger = logging.getLogger(__name__)

CONFIG_VERSION = 2
CONFIG_FILENAME = "config.json"
LEGACY_CONFIG_PATH = os.path.join(os.path.expanduser("~"), "hac_config.json")

DEFAULT_CONFIG = {
    "version": CONFIG_VERSION,
    "interval": DEFAULT_INTERVAL,
    "hotkey": DEFAULT_HOTKEY,
    "mode": MODE_CLICK,
    "target_key": DEFAULT_TARGET_KEY,
}


def config_path() -> str:
    return os.path.join(user_data_dir(), CONFIG_FILENAME)


def _read_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _migrate(data: dict) -> dict:
    """Bring configs written by older versions up to CONFIG_VERSION."""
    data = dict(data)
    if data.get("version", 1) < 2:
        key = data.get("target_key")
        if key in ("left", "right", "middle"):
            data["target_key"] = f"mouse_{key}"
        elif key in ("left_arrow", "right_arrow"):
            data["target_key"] = key.split("_")[0]
    data["version"] = CONFIG_VERSION
    return data


def _sanitize(data: dict) -> dict:
    cfg = dict(DEFAULT_CONFIG)

    interval = data.get("interval")
    if isinstance(interval, (int, float)) and not isinstance(interval, bool) and math.isfinite(interval):
        cfg["interval"] = min(MAX_INTERVAL, max(MIN_INTERVAL, float(interval)))

    if data.get("mode") in MODES:
        cfg["mode"] = data["mode"]

    hotkey = data.get("hotkey")
    if isinstance(hotkey, str) and hotkey.strip():
        cfg["hotkey"] = hotkey.strip()

    if data.get("target_key") in KEY_CHOICES:
        cfg["target_key"] = data["target_key"]

    return cfg


def load_config() -> dict:
    path = config_path()
    if os.path.exists(path):
        data = _read_json(path)
    elif os.path.exists(LEGACY_CONFIG_PATH):
        data = _read_json(LEGACY_CONFIG_PATH)
        data.setdefault("version", 1)
    else:
        data = {}
    return _sanitize(_migrate(data))


def save_config(partial: dict) -> dict:
    config = _sanitize({**load_config(), **partial})
    path = config_path()
    tmp = path + ".tmp"
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        os.replace(tmp, path)
    except OSError:
        logger.exception("Could not save config to %s", path)
    return config
