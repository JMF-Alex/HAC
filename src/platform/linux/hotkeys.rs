use super::x11;
use std::collections::HashSet;
use std::error::Error;
use std::thread;
use x11rb::connection::{Connection, RequestConnection};
use x11rb::protocol::Event;
use x11rb::protocol::xinput::{self, ConnectionExt as _, EventMask, XIEventMask};
use x11rb::protocol::xproto::Keysym;
use x11rb::rust_connection::RustConnection;

pub fn key_name(keysym: Keysym) -> Option<String> {
    let name = match keysym {
        0xFF08 => "BACKSPACE",
        0xFF09 => "TAB",
        0xFF0D => "ENTER",
        0xFFE1 | 0xFFE2 => "SHIFT",
        0xFFE3 | 0xFFE4 => "CTRL",
        // 0xFE03 is AltGr
        0xFFE9 | 0xFFEA | 0xFE03 => "ALT",
        0xFF13 => "PAUSE",
        0xFFE5 => "CAPS LOCK",
        0xFF1B => "ESC",
        0x20 => "SPACE",
        0xFF55 => "PAGE UP",
        0xFF56 => "PAGE DOWN",
        0xFF57 => "END",
        0xFF50 => "HOME",
        0xFF51 => "LEFT",
        0xFF52 => "UP",
        0xFF53 => "RIGHT",
        0xFF54 => "DOWN",
        0xFF61 => "PRINT SCREEN",
        0xFF63 => "INSERT",
        0xFFFF => "DELETE",
        0xFFEB | 0xFFEC => "WINDOWS",
        0xFF67 => "MENU",
        0xFFB0..=0xFFB9 => return Some(format!("NUM {}", keysym - 0xFFB0)),
        0xFFAA => "NUM *",
        0xFFAB => "NUM +",
        0xFFAD => "NUM -",
        0xFFAE => "NUM .",
        0xFFAF => "NUM /",
        0xFFBE..=0xFFD5 => return Some(format!("F{}", keysym - 0xFFBD)),
        0xFF7F => "NUM LOCK",
        0xFF14 => "SCROLL LOCK",
        _ => {
            let code = match keysym {
                0x21..=0xFF => keysym,
                0x0100_0100..=0x0110_FFFF => keysym - 0x0100_0000,
                _ => return None,
            };
            return char::from_u32(code).filter(|c| !c.is_control()).map(|c| c.to_uppercase().collect());
        }
    };
    Some(name.to_string())
}

fn name_of(keysyms: &[Keysym]) -> Option<String> {
    keysyms.iter().find_map(|&k| key_name(k))
}

pub fn is_valid_hotkey(name: &str) -> bool {
    let wanted = name.to_lowercase();
    x11::conn().is_some_and(|(conn, _)| {
        x11::keymap(conn).iter().any(|(_, syms)| name_of(syms).is_some_and(|n| n.to_lowercase() == wanted))
    })
}

fn listen(on_key: &impl Fn(String)) -> Result<(), Box<dyn Error>> {
    let (conn, screen) = RustConnection::connect(None)?;
    let root = conn.setup().roots[screen].root;
    if conn.extension_information(xinput::X11_EXTENSION_NAME)?.is_none() {
        return Err("the X server has no XInput extension".into());
    }
    conn.xinput_xi_query_version(2, 0)?.reply()?;
    // keys sent by programs (the clicker included) come from the XTEST devices, so they never trigger a hotkey
    let fake: HashSet<_> = conn
        .xinput_xi_query_device(xinput::Device::ALL)?
        .reply()?
        .infos
        .iter()
        .filter(|d| String::from_utf8_lossy(&d.name).contains("XTEST"))
        .map(|d| d.deviceid)
        .collect();
    // raw events on the root window arrive whichever window has focus
    let keys = XIEventMask::RAW_KEY_PRESS | XIEventMask::RAW_KEY_RELEASE;
    let mask = EventMask { deviceid: xinput::Device::ALL_MASTER.into(), mask: vec![keys] };
    conn.xinput_xi_select_events(root, &[mask])?.check()?;

    let mut down = HashSet::new();
    loop {
        match conn.wait_for_event()? {
            Event::XinputRawKeyPress(e) if !fake.contains(&e.sourceid) && down.insert(e.detail) => {
                let syms = x11::keymap(&conn).into_iter().find(|(code, _)| u32::from(*code) == e.detail);
                if let Some(name) = syms.and_then(|(_, syms)| name_of(&syms)) {
                    on_key(name);
                }
            }
            Event::XinputRawKeyRelease(e) => {
                down.remove(&e.detail);
            }
            _ => {}
        }
    }
}

pub fn listen_keys(on_key: impl Fn(String) + Send + 'static, on_failure: impl FnOnce(String) + Send + 'static) {
    thread::spawn(move || {
        if let Err(err) = listen(&on_key) {
            on_failure(err.to_string());
        }
    });
}
