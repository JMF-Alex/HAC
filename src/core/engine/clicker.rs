use crate::core::constants::{MAX_INTERVAL, MAX_JITTER, MAX_LIMIT_VALUE, MAX_START_DELAY, MIN_INTERVAL, MIN_LIMIT_VALUE};
use crate::core::storage::config::{LimitKind, Mode, Profile};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{Arc, Condvar, Mutex};
use std::thread::{self, JoinHandle};
use std::time::{Duration, Instant};

pub trait Input: Send {
    fn press(&mut self);
    fn release(&mut self);
}

pub type InputFactory = Box<dyn Fn(&str) -> Result<Box<dyn Input>, String> + Send + Sync>;

pub fn next_delay(interval: f64, jitter: f64) -> f64 {
    if jitter <= 0.0 {
        return interval;
    }
    let spread = jitter / 100.0;
    let factor = 1.0 - spread + fastrand::f64() * 2.0 * spread;
    (interval * factor).max(MIN_INTERVAL)
}

#[derive(Clone, Default)]
struct StopSignal(Arc<(Mutex<bool>, Condvar)>);

impl StopSignal {
    fn set(&self) {
        *self.0.0.lock().unwrap() = true;
        self.0.1.notify_all();
    }

    fn is_set(&self) -> bool {
        *self.0.0.lock().unwrap()
    }

    fn wait(&self, timeout: Option<f64>) -> bool {
        let guard = self.0.0.lock().unwrap();
        match timeout {
            None => *self.0.1.wait_while(guard, |stopped| !*stopped).unwrap(),
            Some(secs) => {
                let dur = Duration::from_secs_f64(secs.max(0.0));
                *self.0.1.wait_timeout_while(guard, dur, |stopped| !*stopped).unwrap().0
            }
        }
    }
}

struct Run {
    id: u64,
    start_delay: f64,
    running: bool,
    created_at: Instant,
    started_at: Instant,
    stop: StopSignal,
    thread: Option<JoinHandle<()>>,
}

impl Run {
    fn elapsed(&self) -> f64 {
        if self.running { self.started_at.elapsed().as_secs_f64() } else { 0.0 }
    }
}

#[derive(Default)]
struct State {
    run: Option<Run>,
    next_id: u64,
    limit_reached: bool,
    // how long the last run clicked, kept so the result stays on screen
    last_elapsed: f64,
}

struct Shared {
    state: Mutex<State>,
    clicks: AtomicU64,
}

pub struct Clicker {
    shared: Arc<Shared>,
    factory: InputFactory,
}

struct Job {
    id: u64,
    mode: Mode,
    interval: f64,
    jitter: f64,
    limit_kind: LimitKind,
    limit_value: f64,
    start_delay: f64,
    stop: StopSignal,
}

impl Clicker {
    pub fn new(factory: InputFactory) -> Self {
        Clicker { shared: Arc::new(Shared { state: Mutex::default(), clicks: AtomicU64::new(0) }), factory }
    }

    pub fn is_clicking(&self) -> bool {
        self.shared.state.lock().unwrap().run.is_some()
    }

    pub fn is_waiting(&self) -> bool {
        self.shared.state.lock().unwrap().run.as_ref().is_some_and(|r| !r.running)
    }

    pub fn elapsed(&self) -> f64 {
        let state = self.shared.state.lock().unwrap();
        state.run.as_ref().map_or(state.last_elapsed, Run::elapsed)
    }

    pub fn delay_remaining(&self) -> f64 {
        let state = self.shared.state.lock().unwrap();
        state
            .run
            .as_ref()
            .filter(|r| !r.running)
            .map_or(0.0, |r| (r.start_delay - r.created_at.elapsed().as_secs_f64()).max(0.0))
    }

    pub fn limit_reached(&self) -> bool {
        self.shared.state.lock().unwrap().limit_reached
    }

    pub fn click_count(&self) -> u64 {
        self.shared.clicks.load(Ordering::Relaxed)
    }

    pub fn start(&self, p: &Profile) -> Result<bool, String> {
        let mut limit_kind = p.limit_kind;
        if limit_kind == LimitKind::Clicks && p.mode == Mode::Hold {
            limit_kind = LimitKind::Never;
        }
        let mut limit_value = p.limit_value.clamp(MIN_LIMIT_VALUE, MAX_LIMIT_VALUE);
        if limit_kind == LimitKind::Clicks {
            limit_value = limit_value.round();
        }

        let mut state = self.shared.state.lock().unwrap();
        if state.run.is_some() {
            return Ok(false);
        }
        let input = (self.factory)(&p.target_key)?;
        state.next_id += 1;
        let job = Job {
            id: state.next_id,
            mode: p.mode,
            interval: p.interval.clamp(MIN_INTERVAL, MAX_INTERVAL),
            jitter: p.jitter.clamp(0.0, MAX_JITTER),
            limit_kind,
            limit_value,
            start_delay: p.start_delay.clamp(0.0, MAX_START_DELAY),
            stop: StopSignal::default(),
        };
        let now = Instant::now();
        let mut run = Run {
            id: job.id,
            start_delay: job.start_delay,
            running: false,
            created_at: now,
            started_at: now,
            stop: job.stop.clone(),
            thread: None,
        };
        state.limit_reached = false;
        state.last_elapsed = 0.0;
        self.shared.clicks.store(0, Ordering::Relaxed);
        let shared = self.shared.clone();
        let spawned = thread::Builder::new().name("hac-clicker".into()).spawn(move || work(shared, job, input));
        run.thread = Some(spawned.map_err(|e| e.to_string())?);
        state.run = Some(run);
        Ok(true)
    }

    pub fn stop(&self) -> bool {
        let Some(mut run) = ({
            let mut state = self.shared.state.lock().unwrap();
            let run = state.run.take();
            if let Some(run) = &run {
                state.last_elapsed = run.elapsed();
            }
            run
        }) else {
            return false;
        };
        run.stop.set();
        if let Some(thread) = run.thread.take() {
            let _ = thread.join();
        }
        true
    }

    pub fn clear_result(&self) {
        let mut state = self.shared.state.lock().unwrap();
        if state.run.is_none() {
            state.limit_reached = false;
            state.last_elapsed = 0.0;
            self.shared.clicks.store(0, Ordering::Relaxed);
        }
    }
}

fn work(shared: Arc<Shared>, job: Job, mut input: Box<dyn Input>) {
    if job.start_delay > 0.0 && job.stop.wait(Some(job.start_delay)) {
        return;
    }
    {
        let mut state = shared.state.lock().unwrap();
        match state.run.as_mut() {
            Some(run) if run.id == job.id => {
                run.running = true;
                run.started_at = Instant::now();
            }
            _ => return,
        }
    }
    let reached = match job.mode {
        Mode::Hold => hold(&job, input.as_mut()),
        Mode::Click => click_loop(&shared, &job, input.as_mut()),
    };
    if reached {
        let mut state = shared.state.lock().unwrap();
        if state.run.as_ref().is_some_and(|r| r.id == job.id) {
            state.limit_reached = true;
            state.last_elapsed = state.run.take().map_or(0.0, |r| r.elapsed());
        }
    }
}

fn click_loop(shared: &Shared, job: &Job, input: &mut dyn Input) -> bool {
    let max_clicks = (job.limit_kind == LimitKind::Clicks).then_some(job.limit_value as u64);
    let deadline = (job.limit_kind == LimitKind::Time).then(|| Instant::now() + Duration::from_secs_f64(job.limit_value));
    let mut clicks = 0;
    while !job.stop.is_set() {
        input.press();
        input.release();
        clicks += 1;
        shared.clicks.store(clicks, Ordering::Relaxed);
        if max_clicks.is_some_and(|max| clicks >= max) {
            return true;
        }
        let delay = next_delay(job.interval, job.jitter);
        if let Some(deadline) = deadline {
            let remaining = deadline.saturating_duration_since(Instant::now()).as_secs_f64();
            if remaining <= 0.0 {
                return true;
            }
            if delay >= remaining {
                return !job.stop.wait(Some(remaining));
            }
        }
        if job.stop.wait(Some(delay)) {
            return false;
        }
    }
    false
}

fn hold(job: &Job, input: &mut dyn Input) -> bool {
    input.press();
    let timeout = (job.limit_kind == LimitKind::Time).then_some(job.limit_value);
    let reached = !job.stop.wait(timeout);
    input.release();
    reached
}
