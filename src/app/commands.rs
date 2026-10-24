use super::{Controller, Snapshot};
use crate::core::constants::MIN_LIMIT_VALUE;
use crate::core::storage::config::{self, LimitKind, Profile, Settings};
use crate::core::storage::profiles;
use serde_json::{Map, Value};
use tauri::State;

type Cmd<'a> = State<'a, Controller>;

#[tauri::command]
pub fn get_state(c: Cmd) -> Snapshot {
    let inner = c.lock();
    Snapshot { config: inner.config.clone(), status: c.status(&inner) }
}

#[tauri::command]
pub fn toggle(c: Cmd) {
    let mut inner = c.lock();
    c.toggle(&mut inner);
    c.commit(&mut inner);
}

#[tauri::command]
pub fn select_profile(c: Cmd, name: String) {
    let mut inner = c.lock();
    if inner.blocked() || name == inner.config.active_profile || !inner.config.profiles.contains_key(&name) {
        return;
    }
    c.clicker.stop();
    c.activate(&mut inner, name);
    c.commit(&mut inner);
}

#[tauri::command]
pub fn add_profile(c: Cmd, name: String) -> Result<(), String> {
    let mut inner = c.lock();
    let name = name.trim().to_string();
    if let Some(err) = profiles::name_error(&name, &inner.config.profiles, None) {
        return Err(err);
    }
    c.clicker.stop();
    let profile = Profile { hotkey: profiles::suggest_hotkey(&inner.config.profiles), ..Profile::default() };
    inner.config.profiles.insert(name.clone(), profile);
    c.activate(&mut inner, name);
    c.commit(&mut inner);
    Ok(())
}

#[tauri::command]
pub fn duplicate_profile(c: Cmd, name: String) {
    let mut inner = c.lock();
    let Some(source) = inner.config.profiles.get(&name).filter(|_| !inner.blocked()) else { return };
    let profile = Profile { hotkey: profiles::suggest_hotkey(&inner.config.profiles), ..source.clone() };
    c.clicker.stop();
    let copy = profiles::copy_name(&name, &inner.config.profiles);
    inner.config.profiles.insert(copy.clone(), profile);
    c.activate(&mut inner, copy);
    c.commit(&mut inner);
}

#[tauri::command]
pub fn rename_profile(c: Cmd, name: String, new_name: String) -> Result<(), String> {
    let mut inner = c.lock();
    let new_name = new_name.trim().to_string();
    if !inner.config.profiles.contains_key(&name) || new_name == name {
        return Ok(());
    }
    if let Some(err) = profiles::name_error(&new_name, &inner.config.profiles, Some(&name)) {
        return Err(err);
    }
    let profiles = std::mem::take(&mut inner.config.profiles);
    inner.config.profiles =
        profiles.into_iter().map(|(k, v)| if k == name { (new_name.clone(), v) } else { (k, v) }).collect();
    if inner.config.active_profile == name {
        inner.config.active_profile = new_name;
    }
    c.commit(&mut inner);
    Ok(())
}

#[tauri::command]
pub fn delete_profile(c: Cmd, name: String) -> Result<(), String> {
    let mut inner = c.lock();
    let Some(index) = inner.config.profiles.get_index_of(&name) else { return Ok(()) };
    if inner.config.profiles.len() == 1 {
        return Err("You need at least one profile.".into());
    }
    let was_active = name == inner.config.active_profile;
    if was_active {
        c.clicker.stop();
    }
    inner.config.profiles.shift_remove(&name);
    if was_active {
        let next = index.min(inner.config.profiles.len() - 1);
        let next = inner.config.profiles.get_index(next).unwrap().0.clone();
        c.activate(&mut inner, next);
    }
    c.commit(&mut inner);
    Ok(())
}

#[tauri::command]
pub fn update_profile(c: Cmd, patch: Map<String, Value>) {
    let mut inner = c.lock();
    if c.clicker.is_clicking() {
        return;
    }
    let mut merged = config::to_map(inner.config.active());
    merged.extend(patch.into_iter().filter(|(k, _)| k != "hotkey"));
    let mut profile = config::sanitize_profile(&merged);
    if profile.limit_kind == LimitKind::Clicks {
        profile.limit_value = profile.limit_value.round().max(MIN_LIMIT_VALUE);
    }
    *inner.config.active_mut() = profile;
    c.commit(&mut inner);
}

#[tauri::command]
pub fn update_settings(c: Cmd, settings: Settings) {
    let mut inner = c.lock();
    c.set_always_on_top(settings.always_on_top);
    inner.config.settings = settings;
    c.commit(&mut inner);
}

#[tauri::command]
pub fn capture_hotkey(c: Cmd) {
    let mut inner = c.lock();
    if !inner.blocked() {
        inner.capturing = true;
        c.refresh(&mut inner);
    }
}

#[tauri::command]
pub fn set_dialog_open(c: Cmd, open: bool) {
    c.lock().dialog_open = open;
}
