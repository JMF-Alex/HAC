use hac::core::constants::MIN_INTERVAL;
use hac::core::engine::clicker::*;
use hac::core::storage::config::{LimitKind, Mode, Profile};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, Instant};

#[derive(Default)]
struct Log {
    presses: u64,
    releases: u64,
}

struct Fake(Arc<Mutex<Log>>);

impl Input for Fake {
    fn press(&mut self) {
        self.0.lock().unwrap().presses += 1;
    }
    fn release(&mut self) {
        self.0.lock().unwrap().releases += 1;
    }
}

fn clicker() -> (Clicker, Arc<Mutex<Log>>) {
    let log = Arc::new(Mutex::new(Log::default()));
    let shared = log.clone();
    (Clicker::new(Box::new(move |_| Ok(Box::new(Fake(shared.clone())) as Box<dyn Input>))), log)
}

fn wait_until(cond: impl Fn() -> bool) {
    let end = Instant::now() + Duration::from_secs(5);
    while !cond() {
        assert!(Instant::now() < end, "timed out");
        thread::sleep(Duration::from_millis(2));
    }
}

#[test]
fn click_limit_stops_after_exact_count() {
    let (c, log) = clicker();
    let p = Profile { interval: 0.001, limit_kind: LimitKind::Clicks, limit_value: 5.4, ..Profile::default() };
    assert_eq!(c.start(&p), Ok(true));
    wait_until(|| !c.is_clicking());
    assert!(c.limit_reached());
    assert_eq!(c.click_count(), 5);
    assert!(c.elapsed() > 0.0, "elapsed is kept after the run ends");
    assert_eq!(log.lock().unwrap().presses, 5);
    c.clear_result();
    assert!(!c.limit_reached());
    assert_eq!(c.click_count(), 0);
}

#[test]
fn second_start_is_refused_and_stop_ends_the_run() {
    let (c, _) = clicker();
    let p = Profile { interval: 0.005, ..Profile::default() };
    assert_eq!(c.start(&p), Ok(true));
    assert_eq!(c.start(&p), Ok(false));
    wait_until(|| c.click_count() > 0);
    assert!(c.stop());
    assert!(!c.is_clicking() && !c.limit_reached());
    assert!(!c.stop());
}

#[test]
fn hold_presses_once_and_releases_on_stop() {
    let (c, log) = clicker();
    c.start(&Profile { mode: Mode::Hold, ..Profile::default() }).unwrap();
    wait_until(|| log.lock().unwrap().presses == 1);
    c.stop();
    let log = log.lock().unwrap();
    assert_eq!((log.presses, log.releases), (1, 1));
}

#[test]
fn hold_ignores_click_limits_but_honours_time_limits() {
    let (c, log) = clicker();
    c.start(&Profile { mode: Mode::Hold, limit_kind: LimitKind::Time, limit_value: 1.0, ..Profile::default() })
        .unwrap();
    wait_until(|| !c.is_clicking());
    assert!(c.limit_reached());
    assert_eq!(log.lock().unwrap().releases, 1);

    c.start(&Profile { mode: Mode::Hold, limit_kind: LimitKind::Clicks, limit_value: 1.0, ..Profile::default() })
        .unwrap();
    thread::sleep(Duration::from_millis(50));
    assert!(c.is_clicking());
    c.stop();
}

#[test]
fn start_delay_waits_and_can_be_cancelled() {
    let (c, log) = clicker();
    c.start(&Profile { start_delay: 30.0, ..Profile::default() }).unwrap();
    assert!(c.is_waiting());
    assert!(c.delay_remaining() > 29.0);
    c.stop();
    assert_eq!(log.lock().unwrap().presses, 0);
}

#[test]
fn a_bad_key_is_reported_by_start() {
    let c = Clicker::new(Box::new(|k| Err(format!("Unknown key: {k}"))));
    assert_eq!(c.start(&Profile::default()), Err("Unknown key: mouse_left".into()));
    assert!(!c.is_clicking());
}

#[test]
fn jitter_stays_in_range() {
    assert_eq!(next_delay(0.5, 0.0), 0.5);
    for _ in 0..1000 {
        let d = next_delay(1.0, 20.0);
        assert!((0.8..=1.2).contains(&d));
    }
    assert!(next_delay(0.001, 100.0) >= MIN_INTERVAL);
}
