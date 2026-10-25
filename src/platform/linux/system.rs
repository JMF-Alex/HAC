use super::x11;
use x11rb::connection::Connection;
use x11rb::protocol::xproto::ConnectionExt;

pub fn pointer_and_screen() -> Option<(i32, i32, i32, i32)> {
    let (conn, screen) = x11::conn()?;
    let pointer = conn.query_pointer(screen.root).ok()?.reply().ok()?;
    Some((pointer.root_x.into(), pointer.root_y.into(), screen.width_in_pixels.into(), screen.height_in_pixels.into()))
}

pub fn beep() {
    if let Some((conn, _)) = x11::conn() {
        let _ = conn.bell(0);
        let _ = conn.flush();
    }
}
