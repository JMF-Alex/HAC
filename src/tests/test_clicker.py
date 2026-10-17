import time

import pytest

from core.clicker import Clicker
from core.constants import MIN_INTERVAL, MODE_CLICK, MODE_HOLD


class FakeSimulator:
    def __init__(self, click_error=None, release_error=None):
        self.presses = 0
        self.releases = 0
        self.clicks = 0
        self.click_error = click_error
        self.release_error = release_error

    def press(self):
        self.presses += 1

    def release(self):
        self.releases += 1
        if self.release_error is not None:
            raise self.release_error

    def click(self):
        if self.click_error is not None:
            raise self.click_error
        self.clicks += 1


def wait_until(predicate, timeout=3.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.005)
    return predicate()


@pytest.fixture
def make_clicker():
    clickers = []

    def build(factory):
        clicker = Clicker(simulator_factory=factory)
        clickers.append(clicker)
        return clicker

    yield build
    for clicker in clickers:
        clicker.stop()


def test_new_clicker_is_idle(make_clicker):
    clicker = make_clicker(lambda _key: FakeSimulator())
    assert not clicker.is_clicking
    assert clicker.last_error is None


def test_click_mode_clicks_repeatedly_until_stopped(make_clicker):
    sim = FakeSimulator()
    clicker = make_clicker(lambda _key: sim)

    assert clicker.start(MIN_INTERVAL, MODE_CLICK, "mouse_left") is True
    assert clicker.is_clicking
    assert wait_until(lambda: sim.clicks >= 3)

    assert clicker.stop() is True
    assert not clicker.is_clicking
    clicks_at_stop = sim.clicks
    time.sleep(0.05)
    assert sim.clicks == clicks_at_stop
    assert sim.releases == 0


def test_starting_twice_keeps_the_first_run(make_clicker):
    created = []

    def factory(_key):
        created.append(FakeSimulator())
        return created[-1]

    clicker = make_clicker(factory)
    assert clicker.start(0.5, MODE_CLICK, "mouse_left") is True
    assert clicker.start(0.5, MODE_CLICK, "mouse_left") is False
    assert len(created) == 1


def test_stop_when_idle_returns_false(make_clicker):
    clicker = make_clicker(lambda _key: FakeSimulator())
    assert clicker.stop() is False


def test_stop_does_not_wait_for_the_interval(make_clicker):
    sim = FakeSimulator()
    clicker = make_clicker(lambda _key: sim)
    clicker.start(3600, MODE_CLICK, "mouse_left")
    assert wait_until(lambda: sim.clicks >= 1)

    started = time.monotonic()
    assert clicker.stop() is True
    assert time.monotonic() - started < 0.5


def test_hold_mode_presses_once_and_releases_on_stop(make_clicker):
    sim = FakeSimulator()
    clicker = make_clicker(lambda _key: sim)

    assert clicker.start(1, MODE_HOLD, "shift") is True
    assert clicker.is_clicking
    assert (sim.presses, sim.clicks, sim.releases) == (1, 0, 0)

    assert clicker.stop() is True
    assert (sim.presses, sim.clicks, sim.releases) == (1, 0, 1)
    assert clicker.stop() is False


def test_failing_release_does_not_break_stop(make_clicker):
    sim = FakeSimulator(release_error=OSError("device gone"))
    clicker = make_clicker(lambda _key: sim)
    clicker.start(1, MODE_HOLD, "shift")

    assert clicker.stop() is True
    assert not clicker.is_clicking


def test_unknown_mode_is_rejected(make_clicker):
    clicker = make_clicker(lambda _key: FakeSimulator())
    with pytest.raises(ValueError):
        clicker.start(1, "Turbo", "mouse_left")
    assert not clicker.is_clicking


def test_factory_errors_propagate_and_leave_the_clicker_idle(make_clicker):
    def factory(_key):
        raise ValueError("bad key")

    clicker = make_clicker(factory)
    with pytest.raises(ValueError, match="bad key"):
        clicker.start(1, MODE_CLICK, "nope")
    assert not clicker.is_clicking


def test_worker_crash_records_the_error_and_releases(make_clicker):
    sim = FakeSimulator(click_error=RuntimeError("boom"))
    clicker = make_clicker(lambda _key: sim)

    clicker.start(MIN_INTERVAL, MODE_CLICK, "mouse_left")
    assert wait_until(lambda: not clicker.is_clicking)

    assert clicker.last_error == "boom"
    assert sim.releases == 1


def test_worker_crash_without_a_message_falls_back_to_the_class_name(make_clicker):
    sim = FakeSimulator(click_error=ValueError())
    clicker = make_clicker(lambda _key: sim)

    clicker.start(MIN_INTERVAL, MODE_CLICK, "mouse_left")
    assert wait_until(lambda: not clicker.is_clicking)

    assert clicker.last_error == "ValueError"


def test_last_error_is_cleared_by_the_next_start(make_clicker):
    sims = [FakeSimulator(click_error=RuntimeError("boom")), FakeSimulator()]
    clicker = make_clicker(lambda _key: sims.pop(0))

    clicker.start(MIN_INTERVAL, MODE_CLICK, "mouse_left")
    assert wait_until(lambda: not clicker.is_clicking)
    assert clicker.last_error == "boom"

    assert clicker.start(MIN_INTERVAL, MODE_CLICK, "mouse_left") is True
    assert clicker.last_error is None