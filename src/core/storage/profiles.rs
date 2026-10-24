use crate::core::storage::config::Profile;
use indexmap::IndexMap;

pub const DEFAULT_PROFILE_NAME: &str = "Default";
pub const MAX_PROFILE_NAME: usize = 24;

pub fn name_error(name: &str, existing: &IndexMap<String, Profile>, ignore: Option<&str>) -> Option<String> {
    let name = name.trim();
    if name.is_empty() {
        return Some("Enter a name".into());
    }
    if name.chars().count() > MAX_PROFILE_NAME {
        return Some(format!("Use at most {MAX_PROFILE_NAME} characters"));
    }
    let taken = existing.keys().any(|n| Some(n.as_str()) != ignore && n.to_lowercase() == name.to_lowercase());
    taken.then(|| "A profile with that name already exists".into())
}

pub fn unique_name(base: &str, existing: &IndexMap<String, Profile>) -> String {
    let taken = |n: &str| existing.keys().any(|k| k.to_lowercase() == n.to_lowercase());
    if !taken(base) {
        return base.to_string();
    }
    (2..).map(|i| format!("{base} {i}")).find(|n| !taken(n)).unwrap()
}

pub fn copy_name(name: &str, existing: &IndexMap<String, Profile>) -> String {
    for number in 1..1000 {
        let suffix = if number == 1 { " copy".to_string() } else { format!(" copy {number}") };
        let room = MAX_PROFILE_NAME - suffix.chars().count();
        let stem: String = name.trim().chars().take(room).collect();
        let candidate = format!("{}{suffix}", stem.trim_end());
        if name_error(&candidate, existing, None).is_none() {
            return candidate;
        }
    }
    unique_name("Profile", existing)
}

pub fn suggest_hotkey(existing: &IndexMap<String, Profile>) -> String {
    (6..=12)
        .map(|n| format!("F{n}"))
        .find(|h| !existing.values().any(|p| p.hotkey.to_lowercase() == h.to_lowercase()))
        .unwrap_or_default()
}
