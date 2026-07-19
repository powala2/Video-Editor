"""UI for the self-updater: a background check plus the download/apply flow."""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt, QThread, Signal, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMessageBox, QProgressDialog, QApplication

from .. import __version__, storage, updater


class _CheckThread(QThread):
    found = Signal(object)   # UpdateInfo
    none = Signal()
    failed = Signal(str)

    def __init__(self, parent=None, raise_errors=False):
        super().__init__(parent)
        self._raise = raise_errors

    def run(self):
        try:
            info = updater.check_latest(raise_errors=self._raise)
        except Exception as exc:  # noqa: BLE001 - reported to the user
            self.failed.emit(str(exc))
            return
        self.found.emit(info) if info else self.none.emit()


class _DownloadThread(QThread):
    progress = Signal(float)
    done = Signal(str)
    failed = Signal(str)

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = url

    def run(self):
        try:
            path = updater.download(self.url, progress_cb=self.progress.emit)
            self.done.emit(path)
        except Exception as exc:  # noqa: BLE001
            self.failed.emit(str(exc))


def run_startup_check(window):
    """Silent background check on launch (packaged builds only)."""
    if not updater.is_frozen():
        return
    if not storage.get_setting("auto_update", True):
        return
    checker = _CheckThread(window)
    checker.found.connect(lambda info: _on_startup_found(window, info))
    window._update_checker = checker  # keep a reference alive
    checker.start()


def _on_startup_found(window, info):
    if info.version == storage.get_setting("skip_version"):
        return
    _prompt(window, info)


def manual_check(window):
    """User-initiated check — always reports the outcome."""
    checker = _CheckThread(window, raise_errors=True)
    checker.found.connect(lambda info: _prompt(window, info))
    checker.none.connect(
        lambda: QMessageBox.information(
            window, "Up to date",
            f"You're on the latest version ({__version__}).",
        )
    )
    checker.failed.connect(
        lambda msg: QMessageBox.warning(
            window, "Check for updates", f"Couldn't check for updates:\n{msg}"
        )
    )
    window._update_checker = checker
    checker.start()


def _prompt(window, info):
    can_auto = updater.is_frozen() and info.installer_url and sys.platform == "win32"
    box = QMessageBox(window)
    box.setIcon(QMessageBox.Information)
    box.setWindowTitle("Update available")
    box.setText(f"Video Studio {info.version} is available "
                f"(you have {__version__}).")
    if info.notes:
        box.setInformativeText(info.notes[:800])
    update_btn = box.addButton(
        "Update && restart" if can_auto else "Open download page",
        QMessageBox.AcceptRole,
    )
    box.addButton("Later", QMessageBox.RejectRole)
    skip_btn = box.addButton("Skip this version", QMessageBox.DestructiveRole)
    box.exec()

    clicked = box.clickedButton()
    if clicked is skip_btn:
        storage.set_setting("skip_version", info.version)
    elif clicked is update_btn:
        if can_auto:
            _download_and_apply(window, info)
        else:
            QDesktopServices.openUrl(QUrl(info.page_url))


def _download_and_apply(window, info):
    dlg = QProgressDialog("Downloading update…", "Cancel", 0, 100, window)
    dlg.setWindowTitle("Updating")
    dlg.setWindowModality(Qt.WindowModal)
    dlg.setAutoClose(False)
    dlg.setMinimumDuration(0)

    worker = _DownloadThread(info.installer_url, window)
    worker.progress.connect(lambda f: dlg.setValue(int(f * 100)))

    def on_done(path):
        dlg.reset()
        if updater.apply_and_restart(path):
            QApplication.quit()
        else:
            QDesktopServices.openUrl(QUrl(info.page_url))

    def on_failed(msg):
        dlg.reset()
        QMessageBox.warning(
            window, "Update failed",
            f"Couldn't download the update:\n{msg}\n\nOpening the download page.",
        )
        QDesktopServices.openUrl(QUrl(info.page_url))

    worker.done.connect(on_done)
    worker.failed.connect(on_failed)
    dlg.canceled.connect(worker.terminate)
    window._update_download = worker
    worker.start()
    dlg.exec()
