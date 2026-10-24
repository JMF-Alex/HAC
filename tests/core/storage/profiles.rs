use hac::core::storage::config::Profile;
use hac::core::storage::profiles::*;
use indexmap::IndexMap;

#[test]
fn profile_name_helpers() {
    let mut existing = IndexMap::new();
    existing.insert("Profile".to_string(), Profile::default());
    existing.insert("Profile copy".to_string(), Profile { hotkey: "F7".into(), ..Profile::default() });
    assert_eq!(unique_name("Profile", &existing), "Profile 2");
    assert_eq!(copy_name("Profile", &existing), "Profile copy 2");
    assert_eq!(copy_name("A very long profile name!", &existing).chars().count(), MAX_PROFILE_NAME);
    assert_eq!(name_error(" profile ", &existing, None).unwrap(), "A profile with that name already exists");
    assert!(name_error("Profile", &existing, Some("Profile")).is_none());
    assert!(name_error("", &existing, None).is_some());
    assert_eq!(suggest_hotkey(&existing), "F8");
}
