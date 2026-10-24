use crate::core::constants::*;
use crate::core::storage::paths::{config_path, legacy_config_path};
use crate::core::storage::profiles::{DEFAULT_PROFILE_NAME, MAX_PROFILE_NAME};
use indexmap::IndexMap;
use serde::{Deserialize, Serialize};
use serde_json::{Map, Value};
use std::fs;
use std::path::PathBuf;

pub const CONFIG_VERSION: u64 = 5;

#[derive(Serialize, Deserialize, Clone, Copy, PartialEq, Debug)]
pub enum Mode {
    Click,
    Hold,
}

#[derive(Serialize, Deserialize, Clone, Copy, PartialEq, Debug)]
pub enum LimitKind {
    Never,
    Clicks,
    Time,
}

#[derive(Serialize, Deserialize, Clone, Copy, PartialEq, Debug)]
pub enum Failsafe {
    Off,
    #[serde(rename = "Top-left")]
    TopLeft,
    #[serde(rename = "Top-right")]
    TopRight,
    #[serde(rename = "Bottom-left")]
    BottomLeft,
    #[serde(rename = "Bottom-right")]
    BottomRight,
}

impl Failsafe {
    pub fn label(self) -> &'static str {
        match self {
            Failsafe::Off => "off",
            Failsafe::TopLeft => "top-left",
            Failsafe::TopRight => "top-right",
            Failsafe::BottomLeft => "bottom-left",
            Failsafe::BottomRight => "bottom-right",
        }
    }
}

#[derive(Serialize, Deserialize, Clone, PartialEq, Debug)]
pub struct Profile {
    pub interval: f64,
    pub hotkey: String,
    pub mode: Mode,
    pub target_key: String,
    pub jitter: f64,
    pub limit_kind: LimitKind,
    pub limit_value: f64,
    pub start_delay: f64,
}

impl Default for Profile {
    fn default() -> Self {
        Profile {
            interval: 0.01,
            hotkey: "F6".into(),
            mode: Mode::Click,
            target_key: "mouse_left".into(),
            jitter: 0.0,
            limit_kind: LimitKind::Never,
            limit_value: 100.0,
            start_delay: 0.0,
        }
    }
}

#[derive(Serialize, Deserialize, Clone, PartialEq, Debug)]
pub struct Settings {
    pub failsafe: Failsafe,
    pub always_on_top: bool,
    pub sound: bool,
}

impl Default for Settings {
    fn default() -> Self {
        Settings { failsafe: Failsafe::Off, always_on_top: false, sound: false }
    }
}

#[derive(Serialize, Deserialize, Clone, PartialEq, Debug)]
pub struct Config {
    pub version: u64,
    pub active_profile: String,
    pub profiles: IndexMap<String, Profile>,
    pub settings: Settings,
}

impl Config {
    pub fn active(&self) -> &Profile {
        &self.profiles[&self.active_profile]
    }

    pub fn active_mut(&mut self) -> &mut Profile {
        self.profiles.get_mut(&self.active_profile).expect("active profile exists")
    }

    pub fn profile_for_hotkey(&self, hotkey: &str) -> Option<String> {
        self.profiles
            .iter()
            .find(|(_, p)| !p.hotkey.is_empty() && p.hotkey.to_lowercase() == hotkey.to_lowercase())
            .map(|(name, _)| name.clone())
    }
}

pub fn read_json(path: &PathBuf) -> Map<String, Value> {
    fs::read_to_string(path)
        .ok()
        .and_then(|text| serde_json::from_str::<Value>(text.trim_start_matches('\u{feff}')).ok())
        .and_then(|v| match v {
            Value::Object(map) => Some(map),
            _ => None,
        })
        .unwrap_or_default()
}

pub fn migrate(mut data: Map<String, Value>) -> Map<String, Value> {
    let version = match data.get("version") {
        None => 1,
        Some(Value::Number(n)) if n.is_u64() => n.as_u64().unwrap(),
        // a damaged version number must not crash startup or flatten real profiles
        Some(_) if data.get("profiles").is_some_and(Value::is_object) => CONFIG_VERSION,
        Some(_) => 1,
    };
    if version < 2 {
        let renamed = match data.get("target_key").and_then(Value::as_str) {
            Some(k @ ("left" | "right" | "middle")) => Some(format!("mouse_{k}")),
            Some(k @ ("left_arrow" | "right_arrow")) => Some(k.split('_').next().unwrap().to_string()),
            _ => None,
        };
        if let Some(key) = renamed {
            data.insert("target_key".into(), key.into());
        }
    }
    if version < 3 {
        let profile: Map<String, Value> = ["interval", "hotkey", "mode", "target_key"]
            .iter()
            .filter_map(|k| data.get(*k).map(|v| (k.to_string(), v.clone())))
            .collect();
        let mut profiles = Map::new();
        profiles.insert(DEFAULT_PROFILE_NAME.into(), Value::Object(profile));
        data = Map::new();
        data.insert("profiles".into(), Value::Object(profiles));
        data.insert("active_profile".into(), DEFAULT_PROFILE_NAME.into());
    }
    data.insert("version".into(), CONFIG_VERSION.into());
    data
}

fn clamped(value: Option<&Value>, low: f64, high: f64) -> Option<f64> {
    value.and_then(Value::as_f64).filter(|v| v.is_finite()).map(|v| v.clamp(low, high))
}

fn parse<T: for<'de> Deserialize<'de>>(value: Option<&Value>) -> Option<T> {
    value.and_then(|v| serde_json::from_value(v.clone()).ok())
}

pub fn sanitize_profile(data: &Map<String, Value>) -> Profile {
    let mut p = Profile::default();
    if let Some(v) = clamped(data.get("interval"), MIN_INTERVAL, MAX_INTERVAL) {
        p.interval = v;
    }
    if let Some(v) = clamped(data.get("jitter"), 0.0, MAX_JITTER) {
        p.jitter = v;
    }
    if let Some(v) = clamped(data.get("limit_value"), MIN_LIMIT_VALUE, MAX_LIMIT_VALUE) {
        p.limit_value = v;
    }
    if let Some(v) = clamped(data.get("start_delay"), 0.0, MAX_START_DELAY) {
        p.start_delay = v;
    }
    if let Some(v) = parse(data.get("limit_kind")) {
        p.limit_kind = v;
    }
    if let Some(v) = parse(data.get("mode")) {
        p.mode = v;
    }
    if let Some(v) = data.get("hotkey").and_then(Value::as_str) {
        p.hotkey = v.trim().to_string();
    }
    if let Some(v) = data.get("target_key").and_then(Value::as_str).filter(|k| is_key_choice(k)) {
        p.target_key = v.to_string();
    }
    p
}

fn sanitize_settings(data: Option<&Value>) -> Settings {
    let mut s = Settings::default();
    let Some(Value::Object(data)) = data else { return s };
    if let Some(v) = parse(data.get("failsafe")) {
        s.failsafe = v;
    }
    if let Some(v) = data.get("always_on_top").and_then(Value::as_bool) {
        s.always_on_top = v;
    }
    if let Some(v) = data.get("sound").and_then(Value::as_bool) {
        s.sound = v;
    }
    s
}

pub fn sanitize(data: &Map<String, Value>) -> Config {
    let mut profiles = IndexMap::new();
    let mut seen_names = Vec::new();
    let mut used_hotkeys = Vec::new();

    if let Some(Value::Object(raw)) = data.get("profiles") {
        for (name, settings) in raw {
            let Value::Object(settings) = settings else { continue };
            let name: String = name.trim().chars().take(MAX_PROFILE_NAME).collect::<String>().trim().to_string();
            if name.is_empty() || seen_names.contains(&name.to_lowercase()) {
                continue;
            }
            let mut profile = sanitize_profile(settings);
            let hotkey = profile.hotkey.to_lowercase();
            if !hotkey.is_empty() && used_hotkeys.contains(&hotkey) {
                profile.hotkey.clear();
            } else if !hotkey.is_empty() {
                used_hotkeys.push(hotkey);
            }
            seen_names.push(name.to_lowercase());
            profiles.insert(name, profile);
        }
    }
    if profiles.is_empty() {
        profiles.insert(DEFAULT_PROFILE_NAME.to_string(), Profile::default());
    }
    let active = data
        .get("active_profile")
        .and_then(Value::as_str)
        .filter(|a| profiles.contains_key(*a))
        .map(str::to_string)
        .unwrap_or_else(|| profiles.keys().next().unwrap().clone());
    Config {
        version: CONFIG_VERSION,
        active_profile: active,
        profiles,
        settings: sanitize_settings(data.get("settings")),
    }
}

pub fn to_map<T: Serialize>(value: &T) -> Map<String, Value> {
    match serde_json::to_value(value) {
        Ok(Value::Object(map)) => map,
        _ => Map::new(),
    }
}

pub fn load() -> Config {
    let path = config_path();
    let data = if path.exists() {
        read_json(&path)
    } else if let Some(legacy) = legacy_config_path().filter(|p| p.exists()) {
        let mut data = read_json(&legacy);
        data.entry("version").or_insert(1.into());
        data
    } else {
        Map::new()
    };
    sanitize(&migrate(data))
}

pub fn save(config: &Config) {
    let config = sanitize(&to_map(config));
    let path = config_path();
    let tmp = path.with_extension("json.tmp");
    let result = (|| {
        fs::create_dir_all(path.parent().unwrap())?;
        fs::write(&tmp, serde_json::to_string_pretty(&config)?)?;
        fs::rename(&tmp, &path)
    })();
    if let Err(err) = result {
        eprintln!("Could not save config to {}: {err}", path.display());
        let _ = fs::remove_file(&tmp);
    }
}
