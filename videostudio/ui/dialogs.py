"""Background export worker and the recording countdown/HUD dialog."""

from __future__ import annotations

from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox,
)

from .. import theme, export
from ..recorder import ScreenRecorder, RecordingError


class ExportWorker(QThread):
    progress = Signal(float)
    done = Signal(str)
    failed = Signal(str)

    def __init__(self, project, out_path, parent=None):
        super().__init__(parent)
        self.project = project
        self.out_path = out_path

    def run(self):
        try:
            export.export(self.project, self.out_path, progress_cb=self.progress.emit)
            self.done.emit(self.out_path)
        except Exception as exc:  # noqa: BLE001 - surfaced to the user
            self.failed.emit(str(exc))


class RecordingHUD(QDialog):
    """3-2-1 countdown, then a live elapsed HUD with a Stop button.

    Calls ``on_finished(path_or_None)`` when recording ends.
    """

    def __init__(self, recorder: ScreenRecorder, on_finished, mic=True, parent=None):
        super().__init__(parent)
        self.recorder = recorder
        self.on_finished = on_finished
        self.mic = mic
        self._count = 3
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setModal(True)
        self.setStyleSheet(
            f"QDialog{{background:{theme.SURFACE};border:1px solid {theme.BORDER};"
            f"border-radius:16px;}}"
        )
        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(30, 26, 30, 26)
        self._root.setSpacing(16)
        self._build_countdown()

    def _clear(self):
        while self._root.count():
            w = self._root.takeAt(0).widget()
            if w:
                w.deleteLater()

    def _build_countdown(self):
        self._clear()
        self.num = QLabel(str(self._count))
        self.num.setAlignment(Qt.AlignCenter)
        self.num.setStyleSheet(
            f"font-size:64px;font-weight:700;color:white;background:{theme.PRIMARY};"
            f"border-radius:60px;min-width:120px;min-height:120px;"
        )
        self._root.addWidget(self.num, alignment=Qt.AlignCenter)
        sub = QLabel("Recording starts in…")
        sub.setObjectName("Muted")
        sub.setAlignment(Qt.AlignCenter)
        self._root.addWidget(sub)
        self._ctimer = QTimer(self)
        self._ctimer.timeout.connect(self._countdown_tick)
        self._ctimer.start(800)

    def _countdown_tick(self):
        self._count -= 1
        if self._count <= 0:
            self._ctimer.stop()
            self._begin()
        else:
            self.num.setText(str(self._count))

    def _begin(self):
        try:
            self.recorder.start(mic=self.mic)
        except RecordingError as exc:
            self.close()
            QMessageBox.warning(self.parent(), "Recording", str(exc))
            self.on_finished(None)
            return
        self._build_hud()

    def _build_hud(self):
        self._clear()
        badge = QLabel("● RECORDING")
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet(
            f"color:{theme.DANGER};font-weight:700;letter-spacing:1px;"
            f"background:{theme.WARNING_BG};padding:7px 14px;border-radius:999px;"
        )
        self._root.addWidget(badge, alignment=Qt.AlignCenter)
        self.elapsed = QLabel("0:00")
        self.elapsed.setAlignment(Qt.AlignCenter)
        self.elapsed.setStyleSheet("font-size:40px;font-weight:700;")
        self._root.addWidget(self.elapsed)
        hint = QLabel("Capturing your screen" + (" + microphone" if self.mic else ""))
        hint.setObjectName("Faint")
        hint.setAlignment(Qt.AlignCenter)
        self._root.addWidget(hint)

        stop = QPushButton("■  Stop & edit")
        stop.setObjectName("Primary")
        stop.clicked.connect(self._stop)
        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(stop)
        row.addStretch(1)
        self._root.addLayout(row)

        self._etimer = QTimer(self)
        self._etimer.timeout.connect(self._tick_elapsed)
        self._etimer.start(500)

    def _tick_elapsed(self):
        s = int(self.recorder.elapsed())
        self.elapsed.setText(f"{s // 60}:{s % 60:02d}")

    def _stop(self):
        if hasattr(self, "_etimer"):
            self._etimer.stop()
        path = self.recorder.stop()
        self.close()
        self.on_finished(path)

    def closeEvent(self, ev):
        if self.recorder.recording:
            self.recorder.stop()
        super().closeEvent(ev)
