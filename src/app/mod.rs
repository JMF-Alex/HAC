pub mod commands;
pub mod format;

use crate::core::engine::clicker::Clicker;
use crate::core::engine::failsafe::corner_hit;
use crate::core::storage::config::{self, Config, Failsafe};
use crate::platform::{hotkeys, input, system};
use format::clicks_text;
use serde::Serialize;
use std::sync::{Mutex, MutexGuard};
use std::thread;
use std::time::{Duration, Instant};
use tauri::{AppHandle, Emitter, Manager};

const MONITOR_INTERVAL: Duration = Duration::from_millis(50);
const SAVE_DELAY: Duration = Duration::from_millis(400);

#[derive(Serialize, Clone, PartialEq, Debug)]
pub struct Status {
    kind: &'static str,
    message: Option<String>,
    locked: bool,
    capturing: bool,
    clicks: u64,
    elapsed: f64,
    countdown: f64,
}

#[derive(Serialize)]
pub struct Snapshot {
    config: Config,
    status: Status,
}

struct Inner {
    config: Config,
    shown_config: Config,
    unsaved_since: Option<Instant>,
    error: Option<String>,
    note: Option<String>,
    capturing: bool,
    dialog_open: bool,
    shown: Option<Status>,
    was_active: bool,
}

impl Inner {
    fn blocked(&self) -> bool {
        self.capturing || self.dialog_open
    }
}

pub struct Controller {
    inner: Mutex<Inner>,
    clicker: Clicker,
    app: AppHandle,
}

impl Controller {
    pub fn new(app: AppHandle) -> Self {
        let mut config = config::load();
        let mut error = None;
        for profile in config.profiles.values_mut() {
            if !profile.hotkey.is_empty() && !hotkeys::is_valid_hotkey(&profile.hotkey) {
                error = Some(format!("Invalid hotkey: {}", profile.hotkey));
                profile.hotkey.clear();
            }
        }
        let controller = Controller {
            inner: Mutex::new(Inner {
                shown_config: config.clone(),
                unsaved_since: None,
                config,
                error,
                note: None,
                capturing: false,
                dialog_open: false,
                shown: None,
                was_active: false,
            }),
            clicker: Clicker::new(Box::new(input::input_for)),
            app,
        };
        let on_top = controller.lock().config.settings.always_on_top;
        controller.set_always_on_top(on_top);
        controller
    }

    fn lock(&self) -> MutexGuard<'_, Inner> {
        self.inner.lock().unwrap()
    }

    fn set_always_on_top(&self, on: bool) {
        if let Some(window) = self.app.get_webview_window("main") {
            let _ = window.set_always_on_top(on);
        }
    }

    fn commit(&self, inner: &mut Inner) {
        if inner.config != inner.shown_config {
            let _ = self.app.emit("config", &inner.config);
            inner.shown_config = inner.config.clone();
            inner.unsaved_since = Some(Instant::now());
        }
        self.refresh(inner);
    }

    fn save(inner: &mut Inner) {
        if inner.unsaved_since.take().is_some() {
            config::save(&inner.config);
        }
    }

    fn status(&self, inner: &Inner) -> Status {
        let c = &self.clicker;
        // the window shows live numbers from the fields below, so a run carries no message
        let (kind, message) = if c.is_clicking() {
            (if c.is_waiting() { "waiting" } else { "running" }, None)
        } else if let Some(error) = &inner.error {
            ("error", Some(error.clone()))
        } else if let Some(note) = &inner.note {
            ("done", Some(note.clone()))
        } else if c.limit_reached() {
            let clicks = c.click_count();
            let text = if clicks > 0 {
                format!("Finished after {}", clicks_text(clicks))
            } else {
                "Finished · time limit reached".to_string()
            };
            ("done", Some(text))
        } else {
            ("stopped", None)
        };
        Status {
            kind,
            message,
            locked: kind == "running" || kind == "waiting",
            capturing: inner.capturing,
            clicks: c.click_count(),
            // tenths are enough for the screen and keep identical statuses from being re-sent
            elapsed: (c.elapsed() * 10.0).floor() / 10.0,
            countdown: (c.delay_remaining() * 10.0).ceil() / 10.0,
        }
    }

    fn refresh(&self, inner: &mut Inner) {
        let status = self.status(inner);
        let active = status.kind == "running";
        if active != inner.was_active {
            inner.was_active = active;
            if inner.config.settings.sound {
                system::beep();
            }
        }
        if inner.shown.as_ref() != Some(&status) {
            let _ = self.app.emit("status", &status);
            inner.shown = Some(status);
        }
    }

    fn start(&self, inner: &mut Inner) {
        match self.clicker.start(inner.config.active()) {
            Ok(_) => {
                inner.error = None;
                inner.note = None;
            }
            Err(err) => inner.error = Some(err),
        }
    }

    fn toggle(&self, inner: &mut Inner) {
        if self.clicker.is_clicking() {
            self.clicker.stop();
        } else {
            self.start(inner);
        }
    }

    fn activate(&self, inner: &mut Inner, name: String) {
        inner.config.active_profile = name;
        inner.error = None;
        inner.note = None;
        self.clicker.clear_result();
    }

    fn tick(&self) {
        let mut inner = self.lock();
        let corner = inner.config.settings.failsafe;
        if corner != Failsafe::Off
            && self.clicker.is_clicking()
            && !self.clicker.is_waiting()
            && let Some((x, y, width, height)) = system::pointer_and_screen()
            && corner_hit(corner, x, y, width, height)
        {
            self.clicker.stop();
            inner.note = Some(format!("Stopped · mouse reached the {} corner", corner.label()));
        }
        if inner.unsaved_since.is_some_and(|since| since.elapsed() >= SAVE_DELAY) {
            Self::save(&mut inner);
        }
        self.refresh(&mut inner);
    }

    fn on_key(&self, name: &str) {
        let mut inner = self.lock();
        if inner.capturing {
            inner.capturing = false;
            if name != "ESC" {
                match inner.config.profile_for_hotkey(name) {
                    Some(owner) if owner != inner.config.active_profile => {
                        inner.error = Some(format!("{name} is already used by '{owner}'"));
                    }
                    _ => {
                        inner.config.active_mut().hotkey = name.to_string();
                        inner.error = None;
                    }
                }
            }
        } else if inner.dialog_open {
            return;
        } else if let Some(profile) = inner.config.profile_for_hotkey(name) {
            if profile == inner.config.active_profile {
                self.toggle(&mut inner);
            } else {
                self.clicker.stop();
                self.activate(&mut inner, profile);
                self.start(&mut inner);
            }
        } else {
            return;
        }
        self.commit(&mut inner);
    }

    fn hotkeys_failed(&self, err: String) {
        let mut inner = self.lock();
        inner.error = Some(format!("Global hotkeys are unavailable: {err}"));
        self.refresh(&mut inner);
    }

    pub fn shutdown(&self) {
        self.clicker.stop();
        Self::save(&mut self.lock());
    }
}

pub fn start_background(app: AppHandle) {
    let handle = app.clone();
    let on_failure = app.clone();
    hotkeys::listen_keys(
        move |name| handle.state::<Controller>().on_key(&name),
        move |err| on_failure.state::<Controller>().hotkeys_failed(err),
    );
    thread::spawn(move || {
        loop {
            thread::sleep(MONITOR_INTERVAL);
            app.state::<Controller>().tick();
        }
    });
}
