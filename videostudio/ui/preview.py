"""Video preview with transport controls.

Plays the *timeline* — the ordered, trimmed clips — by driving a single
QMediaPlayer and switching its source at clip boundaries. Captions are shown
live as an overlaid label; zoom is indicated on the timeline and applied on
export (a Qt widget can't cheaply push-in on a live video frame).
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal, QUrl, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QComboBox,
    QFrame,
)

from .. import theme


def _fmt(t: float) -> str:
    t = max(0, int(t))
    return f"{t // 60}:{t % 60:02d}"


class PreviewPanel(QWidget):
    positionChanged = Signal(float)   # timeline seconds

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self._idx = -1            # index of clip currently loaded
        self._pending_ms = None   # seek to apply once media loads
        self._pending_play = False
        self._suppress = False
        self._rate = 1.0

        self.player = QMediaPlayer(self)
        self.audio = QAudioOutput(self)
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(0.9)

        self.video = QVideoWidget(self)
        self.video.setStyleSheet("background:#0f1712;border-radius:12px;")
        self.player.setVideoOutput(self.video)

        self.caption = QLabel(self.video)
        self.caption.setAlignment(Qt.AlignCenter)
        self.caption.setWordWrap(True)
        self.caption.setStyleSheet(
            "background:rgba(15,23,18,0.82);color:#f4f1e8;font-size:16px;"
            "font-weight:600;padding:6px 14px;border-radius:8px;"
        )
        self.caption.hide()

        self.player.positionChanged.connect(self._on_position)
        self.player.mediaStatusChanged.connect(self._on_status)

        self._build_transport()

    # ------------------------------------------------------------------ UI
    def _build_transport(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)
        root.addWidget(self.video, 1)

        bar = QFrame()
        bar.setObjectName("Panel")
        h = QHBoxLayout(bar)
        h.setContentsMargins(14, 8, 14, 8)
        h.setSpacing(12)

        self.play_btn = QPushButton("▶")
        self.play_btn.setObjectName("Primary")
        self.play_btn.setFixedSize(40, 36)
        self.play_btn.clicked.connect(self.toggle)
        h.addWidget(self.play_btn)

        self.time_lbl = QLabel("0:00 / 0:00")
        self.time_lbl.setObjectName("Muted")
        h.addWidget(self.time_lbl)

        self.scrub = QSlider(Qt.Horizontal)
        self.scrub.setRange(0, 1000)
        self.scrub.sliderMoved.connect(self._on_scrub)
        self.scrub.sliderPressed.connect(lambda: setattr(self, "_scrubbing", True))
        self.scrub.sliderReleased.connect(self._scrub_released)
        self._scrubbing = False
        h.addWidget(self.scrub, 1)

        h.addWidget(QLabel("Speed"))
        self.speed = QComboBox()
        self.speed.addItems(["1×", "1.5×", "2×"])
        self.speed.currentIndexChanged.connect(self._on_speed)
        h.addWidget(self.speed)

        vol = QSlider(Qt.Horizontal)
        vol.setFixedWidth(90)
        vol.setRange(0, 100)
        vol.setValue(90)
        vol.valueChanged.connect(lambda v: self.audio.setVolume(v / 100))
        h.addWidget(QLabel("🔊"))
        h.addWidget(vol)

        root.addWidget(bar)

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self._place_caption()

    def _place_caption(self):
        m = 24
        w = int(self.video.width() * 0.8)
        self.caption.setFixedWidth(max(120, w))
        self.caption.adjustSize()
        x = (self.video.width() - self.caption.width()) // 2
        y = self.video.height() - self.caption.height() - m
        self.caption.move(max(0, x), max(0, y))

    # --------------------------------------------------------------- state
    def set_project(self, project):
        self.player.stop()
        self.project = project
        self._idx = -1
        self.refresh()
        self.seek(0.0)

    def refresh(self):
        """Recompute timeline geometry after edits."""
        self._starts = []
        t = 0.0
        for c in (self.project.clips if self.project else []):
            self._starts.append(t)
            t += c.duration
        self._total = t
        self._update_time_label()

    @property
    def total(self) -> float:
        return getattr(self, "_total", 0.0)

    # ------------------------------------------------------------- playback
    def toggle(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def play(self):
        if not self.project or not self.project.clips:
            return
        if self._idx < 0:
            self.seek(0.0, play=True)
        else:
            self.player.play()
            self.play_btn.setText("⏸")

    def pause(self):
        self.player.pause()
        self.play_btn.setText("▶")

    def _clip_source_url(self, clip):
        media = self.project.media_for(clip)
        return QUrl.fromLocalFile(media.path) if media else QUrl()

    def _load_clip(self, idx: int, source_time: float, play: bool):
        clip = self.project.clips[idx]
        self._idx = idx
        self._pending_ms = int(source_time * 1000)
        self._pending_play = play
        rate = self._rate * (clip.speed if clip.speed > 0 else 1.0)
        self.player.setPlaybackRate(rate)
        self.player.setSource(self._clip_source_url(clip))

    def seek(self, timeline_t: float, play: bool = False):
        if not self.project or not self.project.clips:
            return
        timeline_t = max(0.0, min(timeline_t, self.total - 0.01))
        clip, start, src = self.project.clip_at(timeline_t)
        if clip is None:
            return
        idx = self.project.clips.index(clip)
        if idx != self._idx or self.player.source().isEmpty():
            self._load_clip(idx, src, play)
        else:
            self._suppress = True
            self.player.setPosition(int(src * 1000))
            self._suppress = False
            if play:
                self.play()
        self._emit(timeline_t)
        self._update_caption(timeline_t)

    def _on_status(self, status):
        if status in (QMediaPlayer.LoadedMedia, QMediaPlayer.BufferedMedia):
            if self._pending_ms is not None:
                self._suppress = True
                self.player.setPosition(self._pending_ms)
                self._suppress = False
                self._pending_ms = None
                if self._pending_play:
                    self.player.play()
                    self.play_btn.setText("⏸")
        elif status == QMediaPlayer.EndOfMedia:
            self._advance()

    def _on_position(self, pos_ms):
        if self._suppress or self._idx < 0 or not self.project:
            return
        clip = self.project.clips[self._idx]
        speed = clip.speed if clip.speed > 0 else 1.0
        src = pos_ms / 1000.0
        # reached this clip's out point -> next clip
        if src >= clip.out_point - 0.03:
            self._advance()
            return
        t = self._starts[self._idx] + (src - clip.in_point) / speed
        if not self._scrubbing:
            self._emit(t)
        self._update_caption(t)

    def _advance(self):
        nxt = self._idx + 1
        if nxt < len(self.project.clips):
            playing = self.player.playbackState() == QMediaPlayer.PlayingState \
                or self._pending_play
            self._load_clip(nxt, self.project.clips[nxt].in_point, playing)
        else:
            self.pause()
            self._emit(self.total)

    # ---------------------------------------------------------------- utils
    def _emit(self, t):
        self._current = t
        if not self._scrubbing:
            self._suppress_scrub = True
            self.scrub.setValue(int(t / self.total * 1000) if self.total else 0)
            self._suppress_scrub = False
        self._update_time_label(t)
        self.positionChanged.emit(t)

    def _update_time_label(self, t=None):
        if t is None:
            t = getattr(self, "_current", 0.0)
        self.time_lbl.setText(f"{_fmt(t)} / {_fmt(self.total)}")

    def _update_caption(self, t):
        if not self.project:
            return
        cap = self.project.caption_at(t)
        if cap and cap.text.strip():
            self.caption.setText(cap.text)
            self.caption.show()
            self._place_caption()
        else:
            self.caption.hide()

    def _on_scrub(self, val):
        if self.total:
            t = val / 1000 * self.total
            self.time_lbl.setText(f"{_fmt(t)} / {_fmt(self.total)}")

    def _scrub_released(self):
        self._scrubbing = False
        if self.total:
            self.seek(self.scrub.value() / 1000 * self.total,
                      play=self.player.playbackState() == QMediaPlayer.PlayingState)

    def _on_speed(self, idx):
        self._rate = [1.0, 1.5, 2.0][idx]
        if self._idx >= 0:
            clip = self.project.clips[self._idx]
            self.player.setPlaybackRate(self._rate * (clip.speed if clip.speed > 0 else 1.0))
