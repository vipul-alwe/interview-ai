import threading
import time


class ProgressTracker:

    def __init__(
        self,
        label: str,
        interval: float = 5.0,
    ):
        self.label = label
        self.interval = interval

        self.start_time = None
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        self.start_time = time.monotonic()

        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._heartbeat,
            daemon=True,
        )

        self._thread.start()

    def _heartbeat(self):
        while not self._stop_event.wait(
            self.interval
        ):
            elapsed = (
                time.monotonic()
                - self.start_time
            )

            print(
                f"[PROGRESS] {self.label} "
                f"| elapsed: "
                f"{self._format_time(elapsed)}"
            )

    def stop(
        self,
        message: str | None = None,
    ):
        if self.start_time is None:
            return

        elapsed = (
            time.monotonic()
            - self.start_time
        )

        self._stop_event.set()

        if self._thread is not None:
            self._thread.join(
                timeout=0.2
            )

        suffix = (
            f" | {message}"
            if message
            else ""
        )

        print(
            f"[PROGRESS] {self.label} "
            f"| complete: "
            f"{self._format_time(elapsed)}"
            f"{suffix}"
        )

        self.start_time = None

    @staticmethod
    def _format_time(seconds: float) -> str:

        seconds = int(seconds)

        hours = seconds // 3600
        minutes = (
            seconds % 3600
        ) // 60
        seconds = seconds % 60

        if hours:
            return (
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )

        return (
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )


class StepProgress:

    def __init__(
        self,
        total: int,
        label: str,
    ):
        self.total = total
        self.label = label
        self.current = 0
        self.start_time = time.monotonic()

    def update(
        self,
        current: int | None = None,
        message: str = "",
    ):

        if current is not None:
            self.current = current
        else:
            self.current += 1

        elapsed = (
            time.monotonic()
            - self.start_time
        )

        if self.total > 0:
            percentage = (
                self.current
                / self.total
                * 100
            )
        else:
            percentage = 0

        suffix = (
            f" | {message}"
            if message
            else ""
        )

        print(
            f"[PROGRESS] {self.label} "
            f"| {self.current}/{self.total} "
            f"({percentage:5.1f}%)"
            f" | elapsed: "
            f"{ProgressTracker._format_time(elapsed)}"
            f"{suffix}"
        )