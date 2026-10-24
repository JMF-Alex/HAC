use crate::core::engine::clicker::Input;
use windows::Win32::UI::Input::KeyboardAndMouse::*;

enum Target {
    Mouse(MOUSE_EVENT_FLAGS, MOUSE_EVENT_FLAGS),
    Key(VIRTUAL_KEY, bool),
}

struct SendInputDevice(Target);

fn send(input: INPUT) {
    unsafe { SendInput(&[input], size_of::<INPUT>() as i32) };
}

impl SendInputDevice {
    fn event(&self, down: bool) {
        match self.0 {
            Target::Mouse(press, release) => send(INPUT {
                r#type: INPUT_MOUSE,
                Anonymous: INPUT_0 {
                    mi: MOUSEINPUT { dwFlags: if down { press } else { release }, ..Default::default() },
                },
            }),
            Target::Key(vk, extended) => {
                let mut flags = if down { KEYBD_EVENT_FLAGS(0) } else { KEYEVENTF_KEYUP };
                if extended {
                    flags |= KEYEVENTF_EXTENDEDKEY;
                }
                // games often read scan codes, so send both
                let scan = unsafe { MapVirtualKeyW(vk.0 as u32, MAPVK_VK_TO_VSC) } as u16;
                send(INPUT {
                    r#type: INPUT_KEYBOARD,
                    Anonymous: INPUT_0 { ki: KEYBDINPUT { wVk: vk, wScan: scan, dwFlags: flags, ..Default::default() } },
                })
            }
        }
    }
}

impl Input for SendInputDevice {
    fn press(&mut self) {
        self.event(true);
    }
    fn release(&mut self) {
        self.event(false);
    }
}

pub fn input_for(key: &str) -> Result<Box<dyn Input>, String> {
    let target = match key {
        "mouse_left" => Target::Mouse(MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
        "mouse_right" => Target::Mouse(MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP),
        "mouse_middle" => Target::Mouse(MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP),
        "space" => Target::Key(VK_SPACE, false),
        "shift" => Target::Key(VK_SHIFT, false),
        "ctrl" => Target::Key(VK_CONTROL, false),
        "alt" => Target::Key(VK_MENU, false),
        "enter" => Target::Key(VK_RETURN, false),
        "tab" => Target::Key(VK_TAB, false),
        "up" => Target::Key(VK_UP, true),
        "down" => Target::Key(VK_DOWN, true),
        "left" => Target::Key(VK_LEFT, true),
        "right" => Target::Key(VK_RIGHT, true),
        k if k.len() == 1 && k.as_bytes()[0].is_ascii_lowercase() => {
            Target::Key(VIRTUAL_KEY(k.as_bytes()[0].to_ascii_uppercase() as u16), false)
        }
        _ => return Err(format!("Unknown key: {key}")),
    };
    Ok(Box::new(SendInputDevice(target)))
}
