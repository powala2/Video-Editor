"""Background export worker and the recording countdown/HUD overlay.

The recording overlay is a frameless, draggable, dark "Premiere Pro" style
panel that floats over the screen being captured. It runs an animated
countdown ring, then flips to a live HUD (pulsing REC dot, level bars, mono
timer, Stop button).
"""

from __future__ import annotations

import math

from PySide6.QtCore import (
    Qt, QThread, Signal, QTimer, QPropertyAnimation, QEasingCurve,
    QRectF, QPointF, Property,
)
from PySide6.QtGui import (
    QPainter, QColor, QPen, QFont, QConicalGradient, QGuiApplication,
)
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QFrame,
    QMessageBox, QGraphicsDropShadowEffect,
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


# --------------------------------------------------------------------------- #
#  Animated countdown ring
# --------------------------------------------------------------------------- #
class CountdownRing(QWidget):
    """A circular sweep with a big popping number in the middle.

    ``progress`` (0..1) drives the ring over the whole countdown; the shown
    number derives from it and each change triggers a spring "pop".
    """

    finished = Signal()

    def __init__(self, seconds: int = 3, parent=None):
        super().__init__(parent)
        self.setFixedSize(208, 208)
        self._seconds = seconds
        self._progress = 0.0
        self._num_scale = 1.0
        self._number = seconds

        self._pop = QPropertyAnimation(self, b"numScale", self)
        self._pop.setDuration(430)
        self._pop.setStartValue(1.4)
        self._pop.setEndValue(1.0)
        self._pop.setEasingCurve(QEasingCurve.OutBack)

        self._sweep = QPropertyAnimation(self, b"progress", self)
        self._sweep.setDuration(seconds * 1000)
        self._sweep.setStartValue(0.0)
        self._sweep.setEndValue(1.0)
        self._sweep.setEasingCurve(QEasingCurve.Linear)
        self._sweep.finished.connect(self.finished.emit)

    def start(self):
        self._pop.start()
        self._sweep.start()

    # -- Qt properties ------------------------------------------------------ #
    def getProgress(self) -> float:
        return self._progress

    def setProgress(self, value: float):
        self._progress = value
        remaining = self._seconds * (1.0 - value)
        num = max(1, int(math.ceil(remaining - 1e-6)))
        if num != self._number:
            self._number = num
            self._pop.stop()
            self._pop.start()
        self.update()

    progress = Property(float, getProgress, setProgress)

    def getNumScale(self) -> float:
        return self._num_scale

    def setNumScale(self, value: float):
        self._num_scale = value
        self.update()

    numScale = Property(float, getNumScale, setNumScale)

    # -- painting ----------------------------------------------------------- #
    def paintEvent(self, _ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.TextAntialiasing, True)

        margin = 16.0
        rect = QRectF(margin, margin,
                      self.width() - 2 * margin, self.height() - 2 * margin)
        center = rect.center()
        pen_w = 12.0

        # Unfilled track.
        p.setPen(QPen(QColor(theme.REC_TRACK), pen_w, Qt.SolidLine, Qt.RoundCap))
        p.drawArc(rect, 0, 360 * 16)

        # Soft glow beneath the sweep.
        span = -self._progress * 360.0
        glow = QColor(theme.REC_ACCENT)
        glow.setAlpha(70)
        p.setPen(QPen(glow, pen_w + 8, Qt.SolidLine, Qt.RoundCap))
        p.drawArc(rect, int(90 * 16), int(span * 16))

        # The sweep itself, as a conical gradient starting from 12 o'clock.
        grad = QConicalGradient(center, 90.0)
        grad.setColorAt(0.0, QColor(theme.REC_ACCENT_HI))
        grad.setColorAt(0.5, QColor(theme.REC_ACCENT))
        grad.setColorAt(1.0, QColor(theme.REC_ACCENT_HI))
        p.setPen(QPen(grad, pen_w, Qt.SolidLine, Qt.RoundCap))
        p.drawArc(rect, int(90 * 16), int(span * 16))

        # Big number, scaled around the centre for the pop.
        p.save()
        p.translate(center)
        p.scale(self._num_scale, self._num_scale)
        f = QFont(self.font())
        f.setPointSizeF(58)
        f.setWeight(QFont.Bold)
        p.setFont(f)
        p.setPen(QColor(theme.REC_TEXT))
        p.drawText(QRectF(-rect.width() / 2, -rect.height() / 2,
                          rect.width(), rect.height()),
                   Qt.AlignCenter, str(self._number))
        p.restore()


# --------------------------------------------------------------------------- #
#  Live level bars (decorative "we're capturing" pulse)
# --------------------------------------------------------------------------- #
class LevelBars(QWidget):
    def __init__(self, bars: int = 5, color: str = theme.REC_REC, parent=None):
        super().__init__(parent)
        self._n = bars
        self._color = QColor(color)
        self._phase = 0.0
        self.setFixedSize(bars * 6 - 2, 22)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance)
        self._timer.start(70)

    def _advance(self):
        self._phase += 0.35
        self.update()

    def stop(self):
        self._timer.stop()

    def paintEvent(self, _ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        p.setBrush(self._color)
        w, h = 4.0, float(self.height())
        for i in range(self._n):
            amp = 0.5 + 0.5 * math.sin(self._phase + i * 0.9)
            bh = 5 + amp * (h - 5)
            x = i * 6.0
            y = (h - bh) / 2.0
            p.drawRoundedRect(QRectF(x, y, w, bh), 2, 2)


# --------------------------------------------------------------------------- #
#  The overlay dialog
# --------------------------------------------------------------------------- #
class RecordingHUD(QDialog):
    """Animated countdown, then a live recording HUD with a Stop button.

    Calls ``on_finished(path_or_None)`` when recording ends.
    """

    def __init__(self, recorder: ScreenRecorder, on_finished, mic=True, parent=None):
        super().__init__(parent)
        self.recorder = recorder
        self.on_finished = on_finished
        self.mic = mic
        self._drag_offset: QPointF | None = None

        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setModal(False)

        # Outer transparent dialog; a rounded card lives inside so the corners
        # render cleanly and we can drop a shadow behind it.
        outer = QVBoxLayout(self)
        outer.setContentsMargins(26, 26, 26, 26)
        self.card = QFrame(self)
        self.card.setObjectName("RecCard")
        self.card.setStyleSheet(
            f"#RecCard{{background:{theme.REC_PANEL};border:1px solid "
            f"{theme.REC_BORDER};border-radius:18px;}}"
            f"QLabel{{color:{theme.REC_TEXT};background:transparent;}}"
        )
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(46)
        shadow.setOffset(0, 18)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.card.setGraphicsEffect(shadow)
        outer.addWidget(self.card)

        self._root = QVBoxLayout(self.card)
        self._root.setContentsMargins(32, 28, 32, 28)
        self._root.setSpacing(18)
        self._build_countdown()

    # -- layout swap -------------------------------------------------------- #
    def _clear(self):
        while self._root.count():
            item = self._root.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def _clear_layout(self, lay):
        while lay.count():
            item = lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def _overline(self, text: str) -> QLabel:
        lab = QLabel(text)
        lab.setAlignment(Qt.AlignCenter)
        lab.setStyleSheet(
            f"color:{theme.REC_TEXT_FAINT};font-size:11px;font-weight:700;"
            f"letter-spacing:3px;"
        )
        return lab

    # -- countdown ---------------------------------------------------------- #
    def _build_countdown(self):
        self._clear()
        self._root.addWidget(self._overline("GET READY"))
        self.ring = CountdownRing(3, self.card)
        self.ring.finished.connect(self._begin)
        self._root.addWidget(self.ring, alignment=Qt.AlignCenter)

        sub = QLabel("Recording starts automatically")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(f"color:{theme.REC_TEXT_MUTED};font-size:13px;")
        self._root.addWidget(sub)

        cancel = QPushButton("Cancel")
        cancel.setCursor(Qt.PointingHandCursor)
        cancel.setStyleSheet(self._ghost_btn_css())
        cancel.clicked.connect(self._cancel)
        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(cancel)
        row.addStretch(1)
        self._root.addLayout(row)

        QTimer.singleShot(60, self.ring.start)

    def _cancel(self):
        self.close()
        self.on_finished(None)

    def _begin(self):
        try:
            self.recorder.start(mic=self.mic)
        except RecordingError as exc:
            self.close()
            QMessageBox.warning(self.parent(), "Recording", str(exc))
            self.on_finished(None)
            return
        self._build_hud()

    # -- live HUD ----------------------------------------------------------- #
    def _build_hud(self):
        self._clear()
        mic_on = getattr(self.recorder, "mic_used", self.mic)

        # Header: pulsing red dot + REC + level bars.
        header = QHBoxLayout()
        header.setSpacing(10)
        self.dot = QLabel("●")
        self.dot.setStyleSheet(f"color:{theme.REC_REC};font-size:16px;")
        rec = QLabel("REC")
        rec.setStyleSheet(
            f"color:{theme.REC_REC};font-weight:800;letter-spacing:3px;font-size:13px;"
        )
        self.bars = LevelBars(5, theme.REC_REC, self.card)
        header.addStretch(1)
        header.addWidget(self.dot)
        header.addWidget(rec)
        header.addSpacing(4)
        header.addWidget(self.bars)
        header.addStretch(1)
        self._root.addLayout(header)

        self.elapsed = QLabel("00:00")
        self.elapsed.setAlignment(Qt.AlignCenter)
        self.elapsed.setStyleSheet(
            f"color:{theme.REC_TEXT};font-size:46px;font-weight:700;"
            f'font-family:"Consolas","SF Mono","Menlo",monospace;'
            f"letter-spacing:2px;"
        )
        self._root.addWidget(self.elapsed)

        source = "Screen + microphone" if mic_on else "Screen only"
        hint = QLabel(source)
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet(f"color:{theme.REC_TEXT_FAINT};font-size:12px;")
        self._root.addWidget(hint)

        stop = QPushButton("■   Stop && edit")
        stop.setCursor(Qt.PointingHandCursor)
        stop.setStyleSheet(self._stop_btn_css())
        stop.clicked.connect(self._stop)
        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(stop)
        row.addStretch(1)
        self._root.addLayout(row)

        # Pulse the dot.
        self._pulse_up = True
        self._pulse = QTimer(self)
        self._pulse.timeout.connect(self._blink)
        self._pulse.start(560)

        self._etimer = QTimer(self)
        self._etimer.timeout.connect(self._tick_elapsed)
        self._etimer.start(250)

        # Re-anchor: the HUD is smaller than the countdown card.
        QTimer.singleShot(0, self._anchor_bottom)

    def _blink(self):
        self._pulse_up = not self._pulse_up
        self.dot.setStyleSheet(
            f"color:{theme.REC_REC if self._pulse_up else theme.REC_TRACK};"
            f"font-size:16px;"
        )

    def _tick_elapsed(self):
        s = int(self.recorder.elapsed())
        self.elapsed.setText(f"{s // 60:02d}:{s % 60:02d}")

    def _stop(self):
        for attr in ("_etimer", "_pulse"):
            t = getattr(self, attr, None)
            if t:
                t.stop()
        if hasattr(self, "bars"):
            self.bars.stop()
        path = self.recorder.stop()
        self.close()
        self.on_finished(path)

    # -- button styles ------------------------------------------------------ #
    def _ghost_btn_css(self) -> str:
        return (
            f"QPushButton{{background:transparent;border:1px solid "
            f"{theme.REC_BORDER};border-radius:9px;padding:8px 20px;"
            f"color:{theme.REC_TEXT_MUTED};font-size:13px;}}"
            f"QPushButton:hover{{border-color:{theme.REC_TEXT_MUTED};"
            f"color:{theme.REC_TEXT};}}"
        )

    def _stop_btn_css(self) -> str:
        return (
            f"QPushButton{{background:{theme.REC_ACCENT};border:none;"
            f"border-radius:10px;padding:11px 28px;color:white;"
            f"font-size:14px;font-weight:700;}}"
            f"QPushButton:hover{{background:{theme.REC_ACCENT_HI};}}"
        )

    # -- window placement & dragging --------------------------------------- #
    def showEvent(self, ev):
        super().showEvent(ev)
        self._anchor_bottom()

    def _anchor_bottom(self):
        screen = self.screen() or QGuiApplication.primaryScreen()
        if not screen:
            return
        geo = screen.availableGeometry()
        self.adjustSize()
        x = geo.center().x() - self.width() // 2
        y = geo.bottom() - self.height() - 48
        self.move(max(geo.left(), x), max(geo.top(), y))

    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self._drag_offset = ev.globalPosition() - QPointF(self.pos())
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        if self._drag_offset is not None and ev.buttons() & Qt.LeftButton:
            self.move((ev.globalPosition() - self._drag_offset).toPoint())
        super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev):
        self._drag_offset = None
        super().mouseReleaseEvent(ev)

    def closeEvent(self, ev):
        if self.recorder.recording:
            self.recorder.stop()
        super().closeEvent(ev)
