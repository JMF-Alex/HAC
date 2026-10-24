use hac::app::format::clicks_text;

#[test]
fn click_counts() {
    assert_eq!(clicks_text(1), "1 click");
    assert_eq!(clicks_text(999), "999 clicks");
    assert_eq!(clicks_text(1234567), "1,234,567 clicks");
}
