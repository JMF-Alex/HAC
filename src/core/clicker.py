import logging
import threading

from core.constants import MAX_INTERVAL, MIN_INTERVAL, MODE_CLICK, MODE_HOLD
from core.input_simulator import InputSimulator

logger = logging.getLogger(__name__)


class Clicker:
    def __init__(self, simulator_factory=InputSimulator):
        self._simulator_factory = simulator_factory
        self._lock = threading.Lock()
        self._clicking = False
        self._mode = None
        self._simulator = None
        self._thread = None
        self._stop_event = None
        self._last_error = None

    @property
    def is_clicking(self) -> bool:
        return self._clicking

    @property
    def last_error(self):
        return self._last_error

    def start(self, interval: float, mode: str, key: str) -> bool:
        if mode not in (MODE_CLICK, MODE_HOLD):
            raise ValueError(f"Unknown mode: {mode!r}")
        interval = min(MAX_INTERVAL, max(MIN_INTERVAL, float(interval)))

        with self._lock:
            if self._clicking:
                return False
            self._last_error = None
            simulator = self._simulator_factory(key)

            if mode == MODE_HOLD:
                simulator.press()
                self._set_running(mode, simulator, None, None)
            else:
                stop_event = threading.Event()
                thread = threading.Thread(
                    target=self._run,
                    args=(simulator, interval, stop_event),
                    name="hac-clicker",
                    daemon=True,
                )
                self._set_running(mode, simulator, thread, stop_event)
                thread.start()
            return True

    def stop(self) -> bool:
        with self._lock:
            if not self._clicking:
                return False
            mode, simulator = self._mode, self._simulator
            thread, stop_event = self._thread, self._stop_event
            self._clear_state()
            if mode == MODE_HOLD:
                self._safe_release(simulator)

        if stop_event is not None:
            stop_event.set()
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=1.0)
        return True

    def _run(self, simulator, interval: float, stop_event: threading.Event):
        try:
            while not stop_event.is_set():
                simulator.click()
                if stop_event.wait(interval):
                    break
        except Exception as exc:
            logger.exception("Clicker worker crashed")
            self._safe_release(simulator)
            with self._lock:
                if self._stop_event is stop_event:
                    self._last_error = str(exc) or exc.__class__.__name__
                    self._clear_state()

    def _set_running(self, mode, simulator, thread, stop_event):
        self._clicking = True
        self._mode = mode
        self._simulator = simulator
        self._thread = thread
        self._stop_event = stop_event

    def _clear_state(self):
        self._clicking = False
        self._mode = None
        self._simulator = None
        self._thread = None
        self._stop_event = None

    @staticmethod
    def _safe_release(simulator):
        try:
            simulator.release()
        except Exception:
            logger.exception("Could not release key")
