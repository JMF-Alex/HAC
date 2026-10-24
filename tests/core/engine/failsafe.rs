use hac::core::engine::failsafe::corner_hit;
use hac::core::storage::config::Failsafe;

#[test]
fn corners() {
    let (w, h) = (1920, 1080);
    assert!(corner_hit(Failsafe::TopLeft, 0, 1, w, h));
    assert!(corner_hit(Failsafe::TopRight, 1919, 0, w, h));
    assert!(corner_hit(Failsafe::BottomLeft, 2, 1077, w, h));
    assert!(corner_hit(Failsafe::BottomRight, 1921, 1079, w, h));
    assert!(!corner_hit(Failsafe::TopLeft, 3, 0, w, h));
    assert!(!corner_hit(Failsafe::TopRight, 0, 0, w, h));
    assert!(!corner_hit(Failsafe::Off, 0, 0, w, h));
}
