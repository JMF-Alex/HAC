#[cfg(not(windows))]
compile_error!("HAC only supports Windows for now");

pub mod app;
pub mod core;
pub mod platform;
