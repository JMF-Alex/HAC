#[cfg(not(any(windows, target_os = "linux")))]
compile_error!("HAC only supports Windows and Linux for now");

pub mod app;
pub mod core;
pub mod platform;
