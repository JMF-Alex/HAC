use std::collections::HashSet;
use std::thread;
use windows::Win32::Foundation::{HANDLE, HWND, LPARAM, LRESULT, WPARAM};
use windows::Win32::System::LibraryLoader::GetModuleHandleW;
use windows::Win32::UI::Input::KeyboardAndMouse::*;
use windows::Win32::UI::Input::*;
use windows::Win32::UI::WindowsAndMessaging::*;
use windows::core::w;

pub fn key_name(vk: u32) -> Option<String> {
    let name = match vk {
        0x08 => "BACKSPACE",
        0x09 => "TAB",
        0x0D => "ENTER",
        0x10 | 0xA0 | 0xA1 => "SHIFT",
        0x11 | 0xA2 | 0xA3 => "CTRL",
        0x12 | 0xA4 | 0xA5 => "ALT",
        0x13 => "PAUSE",
        0x14 => "CAPS LOCK",
        0x1B => "ESC",
        0x20 => "SPACE",
        0x21 => "PAGE UP",
        0x22 => "PAGE DOWN",
        0x23 => "END",
        0x24 => "HOME",
        0x25 => "LEFT",
        0x26 => "UP",
        0x27 => "RIGHT",
        0x28 => "DOWN",
        0x2C => "PRINT SCREEN",
        0x2D => "INSERT",
        0x2E => "DELETE",
        0x5B | 0x5C => "WINDOWS",
        0x5D => "MENU",
        0x60..=0x69 => return Some(format!("NUM {}", vk - 0x60)),
        0x6A => "NUM *",
        0x6B => "NUM +",
        0x6D => "NUM -",
        0x6E => "NUM .",
        0x6F => "NUM /",
        0x70..=0x87 => return Some(format!("F{}", vk - 0x6F)),
        0x90 => "NUM LOCK",
        0x91 => "SCROLL LOCK",
        _ => {
            // letters, digits and layout keys (º, ñ, ...) are named by the character they type
            let mapped = unsafe { MapVirtualKeyW(vk, MAPVK_VK_TO_CHAR) } & 0xFFFF;
            return char::from_u32(mapped).filter(|c| *c != '\0' && !c.is_control()).map(|c| c.to_uppercase().collect());
        }
    };
    Some(name.to_string())
}

pub fn is_valid_hotkey(name: &str) -> bool {
    let wanted = name.to_lowercase();
    (1..=254).any(|vk| key_name(vk).is_some_and(|n| n.to_lowercase() == wanted))
}

unsafe extern "system" fn window_proc(hwnd: HWND, msg: u32, wparam: WPARAM, lparam: LPARAM) -> LRESULT {
    unsafe { DefWindowProcW(hwnd, msg, wparam, lparam) }
}

fn read_key(lparam: LPARAM) -> Option<(u32, bool)> {
    let mut raw = RAWINPUT::default();
    let mut size = size_of::<RAWINPUT>() as u32;
    let header = size_of::<RAWINPUTHEADER>() as u32;
    let read = unsafe {
        GetRawInputData(HRAWINPUT(lparam.0 as _), RID_INPUT, Some(&mut raw as *mut _ as _), &mut size, header)
    };
    // keys sent by programs (the clicker included) have no device, so they never trigger a hotkey
    if read == u32::MAX || raw.header.dwType != RIM_TYPEKEYBOARD.0 || raw.header.hDevice == HANDLE::default() {
        return None;
    }
    let keyboard = unsafe { raw.data.keyboard };
    // 0xFF is a filler Windows sends around keys like Pause, not a real key
    if keyboard.VKey == 0xFF {
        return None;
    }
    Some((keyboard.VKey as u32, keyboard.Flags as u32 & RI_KEY_BREAK == 0))
}

pub fn listen_keys(on_key: impl Fn(String) + Send + 'static, on_failure: impl FnOnce(String) + Send + 'static) {
    thread::spawn(move || {
        let window = unsafe {
            let instance = GetModuleHandleW(None).unwrap_or_default().into();
            let class = WNDCLASSW {
                lpfnWndProc: Some(window_proc),
                hInstance: instance,
                lpszClassName: w!("HacHotkeys"),
                ..Default::default()
            };
            RegisterClassW(&class);
            CreateWindowExW(
                WINDOW_EX_STYLE::default(),
                w!("HacHotkeys"),
                w!(""),
                WINDOW_STYLE::default(),
                0,
                0,
                0,
                0,
                Some(HWND_MESSAGE),
                None,
                Some(instance),
                None,
            )
        };
        let registered = window.and_then(|hwnd| {
            // usage page 1, usage 6 = keyboards; INPUTSINK = also while another window has focus
            let keyboards = RAWINPUTDEVICE { usUsagePage: 0x01, usUsage: 0x06, dwFlags: RIDEV_INPUTSINK, hwndTarget: hwnd };
            unsafe { RegisterRawInputDevices(&[keyboards], size_of::<RAWINPUTDEVICE>() as u32) }
        });
        if let Err(err) = registered {
            on_failure(err.message());
            return;
        }

        let mut down = HashSet::new();
        let mut msg = MSG::default();
        while unsafe { GetMessageW(&mut msg, None, 0, 0) }.as_bool() {
            if msg.message == WM_INPUT
                && let Some((vk, is_down)) = read_key(msg.lParam)
            {
                if !is_down {
                    down.remove(&vk);
                } else if down.insert(vk)
                    && let Some(name) = key_name(vk)
                {
                    on_key(name);
                }
            }
            // WM_INPUT must still reach DefWindowProc so Windows can free the input
            unsafe { DispatchMessageW(&msg) };
        }
    });
}
