use super::x11;
use crate::core::constants::is_char_key;
use crate::core::engine::clicker::Input;
use x11rb::CURRENT_TIME;
use x11rb::connection::Connection;
use x11rb::protocol::xproto::{BUTTON_PRESS_EVENT, BUTTON_RELEASE_EVENT, KEY_PRESS_EVENT, KEY_RELEASE_EVENT};
use x11rb::protocol::xtest::ConnectionExt as _;

struct XTestDevice {
    events: (u8, u8),
    detail: u8,
}

impl XTestDevice {
    fn event(&self, kind: u8) {
        if let Some((conn, screen)) = x11::conn() {
            let _ = conn.xtest_fake_input(kind, self.detail, CURRENT_TIME, screen.root, 0, 0, 0);
            let _ = conn.flush();
        }
    }
}

impl Input for XTestDevice {
    fn press(&mut self) {
        self.event(self.events.0);
    }
    fn release(&mut self) {
        self.event(self.events.1);
    }
}

pub fn input_for(key: &str) -> Result<Box<dyn Input>, String> {
    let button = |detail| Ok(Box::new(XTestDevice { events: (BUTTON_PRESS_EVENT, BUTTON_RELEASE_EVENT), detail }) as _);
    let keysym = match key {
        "mouse_left" => return button(1),
        "mouse_middle" => return button(2),
        "mouse_right" => return button(3),
        "space" => 0x20,
        "shift" => 0xFFE1,
        "ctrl" => 0xFFE3,
        "alt" => 0xFFE9,
        "enter" => 0xFF0D,
        "tab" => 0xFF09,
        "esc" => 0xFF1B,
        "backspace" => 0xFF08,
        "up" => 0xFF52,
        "down" => 0xFF54,
        "left" => 0xFF51,
        "right" => 0xFF53,
        // a lowercase letter's or digit's keysym is its ASCII code
        k if is_char_key(k) => k.as_bytes()[0] as u32,
        _ => return Err(format!("Unknown key: {key}")),
    };
    let (conn, _) = x11::conn().ok_or("Cannot connect to the X server")?;
    let detail = x11::keymap(conn)
        .into_iter()
        .find(|(_, syms)| syms.contains(&keysym))
        .map(|(code, _)| code)
        .ok_or(format!("Key not on the current keyboard layout: {key}"))?;
    Ok(Box::new(XTestDevice { events: (KEY_PRESS_EVENT, KEY_RELEASE_EVENT), detail }))
}
