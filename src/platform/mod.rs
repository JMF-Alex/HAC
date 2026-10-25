#[cfg_attr(target_os = "linux", path = "linux/hotkeys.rs")]
pub mod hotkeys;
#[cfg_attr(target_os = "linux", path = "linux/input.rs")]
pub mod input;
#[cfg_attr(target_os = "linux", path = "linux/system.rs")]
pub mod system;
#[cfg(target_os = "linux")]
#[path = "linux/x11.rs"]
mod x11;
