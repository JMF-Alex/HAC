use hac::core::constants::is_key_choice;

#[test]
fn key_choices() {
    for key in ["a", "z", "0", "9", "esc", "backspace", "mouse_left"] {
        assert!(is_key_choice(key), "{key}");
    }
    for key in ["A", "ñ", "aa", "", "f6"] {
        assert!(!is_key_choice(key), "{key}");
    }
}
