"""Locate ffmpeg and probe / thumbnail media files.

imageio-ffmpeg ships a static ffmpeg binary inside the wheel, so the app needs
nothing installed on the user's machine. It does not ship ffprobe, so media
metadata is parsed from ``ffmpeg -i`` stderr.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass

import imageio_ffmpeg


def ffmpeg_exe() -> str:
    return imageio_ffmpeg.get_ffmpeg_exe()


# Hide the console window ffmpeg would otherwise pop on Windows.
def _no_window():
    import sys

    if sys.platform == "win32":
        return subprocess.STARTUPINFO(dwFlags=subprocess.STARTF_USESHOWWINDOW)
    return None


def _run(args: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(
        args, capture_output=True, text=True, startupinfo=_no_window(), **kw
    )


_DUR_RE = re.compile(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)")
_VID_RE = re.compile(r"Video:.*?(\d{2,5})x(\d{2,5})")
_AUD_RE = re.compile(r"\bAudio:")


@dataclass
class Probe:
    duration: float = 0.0
    width: int = 0
    height: int = 0
    has_audio: bool = False


def probe(path: str) -> Probe:
    """Read duration, dimensions and audio presence from a media file."""
    out = _run([ffmpeg_exe(), "-hide_banner", "-i", path]).stderr
    p = Probe()
    m = _DUR_RE.search(out)
    if m:
        h, mm, s = m.groups()
        p.duration = int(h) * 3600 + int(mm) * 60 + float(s)
    m = _VID_RE.search(out)
    if m:
        p.width, p.height = int(m.group(1)), int(m.group(2))
    p.has_audio = bool(_AUD_RE.search(out))
    return p


def thumbnail(path: str, out_path: str, at: float = 1.0, width: int = 320) -> bool:
    """Write a single-frame JPEG thumbnail. Returns True on success."""
    r = _run(
        [
            ffmpeg_exe(), "-hide_banner", "-y",
            "-ss", f"{max(0.0, at):.3f}", "-i", path,
            "-frames:v", "1",
            "-vf", f"scale={width}:-1",
            out_path,
        ]
    )
    return r.returncode == 0
