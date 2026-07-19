"""Screen recording via ffmpeg subprocess (cross-platform).

Each platform captures the primary screen with its native ffmpeg input device;
the microphone is optionally mixed in. Recording writes an .mp4 that is then
imported into the editor like any other clip.

* Windows : gdigrab (screen) + dshow (microphone)
* macOS   : avfoundation ("Capture screen 0" + default audio)
* Linux   : x11grab (:0.0) + pulse
"""

from __future__ import annotations

import os
import re
import signal
import subprocess
import sys
import tempfile
import time

from .media import ffmpeg_exe, _no_window


class RecordingError(RuntimeError):
    pass


def _win_audio_device() -> str | None:
    """First DirectShow audio input device name, or None. Windows dshow needs
    the real device name — there is no 'default'."""
    out = subprocess.run(
        [ffmpeg_exe(), "-hide_banner", "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
        capture_output=True, text=True, startupinfo=_no_window(),
    ).stderr
    audio = False
    for line in out.splitlines():
        if "(audio)" in line:
            m = re.search(r'"([^"]+)"', line)
            if m:
                return m.group(1)
    return None


def _platform_inputs(mic: bool) -> list[str]:
    plat = sys.platform
    if plat == "win32":
        args = ["-f", "gdigrab", "-framerate", "30", "-i", "desktop"]
        if mic:
            dev = _win_audio_device()
            if dev:
                args += ["-f", "dshow", "-i", f"audio={dev}"]
        return args
    if plat == "darwin":
        # "1" is typically the screen device; ":0" the default mic.
        spec = "1:0" if mic else "1:none"
        return ["-f", "avfoundation", "-framerate", "30", "-i", spec]
    # linux / other
    args = ["-f", "x11grab", "-framerate", "30", "-i", os.environ.get("DISPLAY", ":0.0")]
    if mic:
        args += ["-f", "pulse", "-i", "default"]
    return args


class ScreenRecorder:
    """Start/stop a screen recording. Writes to ``output_path``."""

    def __init__(self, output_dir: str | None = None):
        self.output_dir = output_dir or tempfile.gettempdir()
        self.proc: subprocess.Popen | None = None
        self.output_path: str | None = None
        self.started_at: float = 0.0

    @property
    def recording(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    def start(self, mic: bool = True) -> str:
        if self.recording:
            raise RecordingError("Already recording.")
        name = time.strftime("Screen recording %Y-%m-%d %H-%M-%S.mp4")
        self.output_path = os.path.join(self.output_dir, name)
        args = [
            ffmpeg_exe(), "-hide_banner", "-y",
            *_platform_inputs(mic),
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
            "-r", "30",
        ]
        if mic:
            args += ["-c:a", "aac", "-b:a", "160k"]
        args += [self.output_path]
        try:
            self.proc = subprocess.Popen(
                args, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE, startupinfo=_no_window(),
            )
        except Exception as exc:  # pragma: no cover - platform dependent
            raise RecordingError(f"Could not start recording: {exc}") from exc
        # Fail fast if ffmpeg dies immediately (e.g. capture denied).
        time.sleep(0.4)
        if self.proc.poll() is not None:
            err = (self.proc.stderr.read() or b"").decode(errors="ignore")[-600:]
            self.proc = None
            raise RecordingError(f"Screen capture could not start:\n{err}")
        self.started_at = time.time()
        return self.output_path

    def elapsed(self) -> float:
        return time.time() - self.started_at if self.recording else 0.0

    def stop(self) -> str | None:
        """Stop cleanly (ffmpeg needs 'q' on stdin to finalize the file)."""
        if not self.proc:
            return None
        try:
            if self.proc.poll() is None:
                try:
                    self.proc.stdin.write(b"q")
                    self.proc.stdin.flush()
                except Exception:
                    self.proc.send_signal(signal.SIGINT)
                try:
                    self.proc.wait(timeout=8)
                except subprocess.TimeoutExpired:
                    self.proc.terminate()
                    self.proc.wait(timeout=4)
        finally:
            path = self.output_path
            self.proc = None
        return path if path and os.path.exists(path) else None
