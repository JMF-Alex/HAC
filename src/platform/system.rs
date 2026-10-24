use windows::Win32::Foundation::POINT;
use windows::Win32::Media::{timeBeginPeriod, timeEndPeriod};
use windows::Win32::System::Diagnostics::Debug::MessageBeep;
use windows::Win32::UI::WindowsAndMessaging::*;

pub fn pointer_and_screen() -> Option<(i32, i32, i32, i32)> {
    let mut point = POINT::default();
    unsafe {
        GetCursorPos(&mut point).ok()?;
        Some((point.x, point.y, GetSystemMetrics(SM_CXSCREEN), GetSystemMetrics(SM_CYSCREEN)))
    }
}

pub fn beep() {
    let _ = unsafe { MessageBeep(MB_OK) };
}

pub fn begin_timer_resolution() {
    unsafe { timeBeginPeriod(1) };
}

pub fn end_timer_resolution() {
    unsafe { timeEndPeriod(1) };
}
