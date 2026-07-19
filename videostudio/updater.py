"""Self-update from the repository's public GitHub Releases.

Flow: on launch the app asks GitHub for the latest release, compares its
``tag_name`` (e.g. ``v1.2.0``) with the running version, and — if newer —
downloads the ``VideoStudioSetup.exe`` asset and hands off to a small helper
that installs it after the app exits, then relaunches.

Only the maintainer publishing a tagged release is needed; users never update
by hand. Works without any embedded secret because the repo's Releases are
public. Stdlib only — no extra dependencies.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from dataclasses import dataclass

from . import __version__

OWNER = "powala2"
REPO = "video-editor"
LATEST_API = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
RELEASES_PAGE = f"https://github.com/{OWNER}/{REPO}/releases/latest"


@dataclass
class UpdateInfo:
    version: str
    installer_url: str | None
    notes: str
    page_url: str


def is_frozen() -> bool:
    """True when running as a packaged (PyInstaller) app."""
    return bool(getattr(sys, "frozen", False))


def _parse_version(text: str) -> tuple:
    """'v1.2.3' / '1.2.3-beta' -> (1, 2, 3). Non-numeric -> ()."""
    m = re.search(r"(\d+(?:\.\d+)*)", text or "")
    if not m:
        return ()
    return tuple(int(p) for p in m.group(1).split("."))


def is_newer(remote: str, local: str) -> bool:
    r, l = _parse_version(remote), _parse_version(local)
    if not r:
        return False
    # pad to equal length for a fair tuple compare
    n = max(len(r), len(l))
    r += (0,) * (n - len(r))
    l += (0,) * (n - len(l))
    return r > l


def check_latest(timeout: float = 8.0, raise_errors: bool = False) -> UpdateInfo | None:
    """Return update info if a newer release exists, else None.

    By default never raises for the common offline / no-releases cases (returns
    None). Pass ``raise_errors=True`` (manual "Check for updates") to surface a
    network error instead of silently reporting "up to date".
    """
    try:
        req = urllib.request.Request(
            LATEST_API,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": f"VideoStudio/{__version__}",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.load(resp)
    except Exception:
        if raise_errors:
            raise
        return None

    tag = data.get("tag_name", "")
    if not tag or not is_newer(tag, __version__):
        return None

    installer_url = None
    for asset in data.get("assets", []):
        if asset.get("name", "").lower().endswith("setup.exe"):
            installer_url = asset.get("browser_download_url")
            break

    return UpdateInfo(
        version=tag.lstrip("vV"),
        installer_url=installer_url,
        notes=(data.get("body") or "").strip(),
        page_url=data.get("html_url", RELEASES_PAGE),
    )


def download(url: str, progress_cb=None, timeout: float = 30.0) -> str:
    """Stream the installer to a temp file. Returns its path."""
    req = urllib.request.Request(url, headers={"User-Agent": f"VideoStudio/{__version__}"})
    fd, path = tempfile.mkstemp(prefix="VideoStudioSetup_", suffix=".exe")
    os.close(fd)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        total = int(resp.headers.get("Content-Length", 0))
        done = 0
        with open(path, "wb") as out:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                out.write(chunk)
                done += len(chunk)
                if progress_cb and total:
                    progress_cb(min(0.999, done / total))
    if progress_cb:
        progress_cb(1.0)
    return path


def apply_and_restart(installer_path: str) -> bool:
    """Install the update after this process exits, then relaunch.

    On Windows a detached helper waits for the app to close, runs the installer
    silently, and starts the app again. Returns True if the hand-off launched
    (the caller should then quit the app).
    """
    exe = sys.executable
    if sys.platform == "win32":
        helper = tempfile.NamedTemporaryFile(
            "w", suffix=".cmd", delete=False, encoding="utf-8"
        )
        helper.write(
            "@echo off\r\n"
            "timeout /t 2 /nobreak >nul\r\n"
            f'start "" /wait "{installer_path}" /VERYSILENT /SUPPRESSMSGBOXES '
            "/CLOSEAPPLICATIONS /NORESTART\r\n"
            f'start "" "{exe}"\r\n'
            'del "%~f0"\r\n'
        )
        helper.close()
        DETACHED = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        subprocess.Popen(["cmd", "/c", helper.name], creationflags=DETACHED,
                         close_fds=True)
        return True
    # Other platforms: no silent installer path in this version.
    return False
