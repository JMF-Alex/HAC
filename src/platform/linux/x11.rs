use std::sync::OnceLock;
use x11rb::connection::Connection;
use x11rb::protocol::xproto::{ConnectionExt, Keycode, Keysym, Screen};
use x11rb::rust_connection::RustConnection;

pub fn conn() -> Option<(&'static RustConnection, &'static Screen)> {
    static CONN: OnceLock<Option<(RustConnection, usize)>> = OnceLock::new();
    let (conn, screen) = CONN.get_or_init(|| RustConnection::connect(None).ok()).as_ref()?;
    Some((conn, &conn.setup().roots[*screen]))
}

pub fn keymap(conn: &RustConnection) -> Vec<(Keycode, Vec<Keysym>)> {
    let (min, max) = (conn.setup().min_keycode, conn.setup().max_keycode);
    let Some(map) = conn.get_keyboard_mapping(min, max - min + 1).ok().and_then(|c| c.reply().ok()) else {
        return Vec::new();
    };
    let per = (map.keysyms_per_keycode as usize).max(1);
    (min..=max).zip(map.keysyms.chunks(per)).map(|(code, syms)| (code, syms.to_vec())).collect()
}
