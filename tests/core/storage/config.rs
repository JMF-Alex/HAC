use hac::core::constants::*;
use hac::core::storage::config::*;
use hac::core::storage::profiles::DEFAULT_PROFILE_NAME;
use serde_json::{Map, Value};
use std::fs;
use serde_json::json;

fn obj(v: Value) -> Map<String, Value> {
    v.as_object().unwrap().clone()
}

#[test]
fn python_config_round_trips_unchanged() {
    let raw = json!({
        "version": 5, "active_profile": "Default",
        "profiles": {"Default": {"interval": 0.01, "hotkey": "º", "mode": "Click", "target_key": "mouse_left",
            "jitter": 0.0, "limit_kind": "Never", "limit_value": 100.0, "start_delay": 0.0}},
        "settings": {"failsafe": "Off", "always_on_top": false, "sound": false}
    });
    let cfg = sanitize(&migrate(obj(raw.clone())));
    assert_eq!(serde_json::to_value(&cfg).unwrap(), raw);
}

#[test]
fn bad_values_fall_back_or_clamp() {
    let cfg = sanitize(&migrate(obj(json!({
        "version": 5, "active_profile": "Missing",
        "profiles": {"A": {"interval": 99999, "jitter": true, "mode": "Spin", "target_key": "zz",
            "limit_value": -5, "start_delay": "3"}},
        "settings": {"failsafe": "Middle", "sound": 1}
    }))));
    let p = &cfg.profiles["A"];
    assert_eq!(cfg.active_profile, "A");
    assert_eq!(p.interval, MAX_INTERVAL);
    assert_eq!(p.jitter, 0.0);
    assert_eq!(p.mode, Mode::Click);
    assert_eq!(p.target_key, "mouse_left");
    assert_eq!(p.limit_value, MIN_LIMIT_VALUE);
    assert_eq!(p.start_delay, 0.0);
    assert_eq!(cfg.settings, Settings::default());
}

#[test]
fn duplicate_names_and_hotkeys_are_dropped() {
    let cfg = sanitize(&obj(json!({"profiles": {
        "One": {"hotkey": "F6"}, "one ": {"hotkey": "F7"}, "Two": {"hotkey": "f6"}, "  ": {}
    }})));
    assert_eq!(cfg.profiles.keys().collect::<Vec<_>>(), ["One", "Two"]);
    assert_eq!(cfg.profiles["Two"].hotkey, "");
}

#[test]
fn version_1_is_migrated_into_a_default_profile() {
    let cfg = sanitize(&migrate(obj(json!({"interval": 0.5, "target_key": "right_arrow", "hotkey": "F8"}))));
    let p = &cfg.profiles[DEFAULT_PROFILE_NAME];
    assert_eq!((p.interval, p.target_key.as_str(), p.hotkey.as_str()), (0.5, "right", "F8"));
}

#[test]
fn empty_config_gets_a_default_profile() {
    let cfg = sanitize(&migrate(Map::new()));
    assert_eq!(cfg.active_profile, DEFAULT_PROFILE_NAME);
    assert_eq!(cfg.active(), &Profile::default());
}

#[test]
fn a_byte_order_mark_is_ignored() {
    let path = std::env::temp_dir().join("hac_bom_test.json");
    fs::write(&path, "\u{feff}{\"version\": 5}").unwrap();
    assert_eq!(read_json(&path).get("version"), Some(&json!(5)));
    let _ = fs::remove_file(&path);
}
