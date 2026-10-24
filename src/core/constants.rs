pub const APP_NAME: &str = "HAutoClicker";

pub const MIN_INTERVAL: f64 = 0.001;
pub const MAX_INTERVAL: f64 = 3600.0;
pub const MAX_JITTER: f64 = 100.0;
pub const MIN_LIMIT_VALUE: f64 = 1.0;
pub const MAX_LIMIT_VALUE: f64 = 1_000_000.0;
pub const MAX_START_DELAY: f64 = 60.0;

pub const MOUSE_KEYS: [&str; 3] = ["mouse_left", "mouse_right", "mouse_middle"];
const SPECIAL_KEYS: [&str; 10] = ["space", "shift", "ctrl", "alt", "enter", "tab", "up", "down", "left", "right"];

pub fn is_key_choice(key: &str) -> bool {
    MOUSE_KEYS.contains(&key)
        || SPECIAL_KEYS.contains(&key)
        || (key.len() == 1 && key.as_bytes()[0].is_ascii_lowercase())
}
