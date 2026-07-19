"""Right-hand Properties panel — context controls for the selected item."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QComboBox, QDoubleSpinBox,
    QPlainTextEdit, QPushButton, QFrame,
)

from .. import theme


class PropertiesPanel(QWidget):
    changed = Signal()
    deleteRequested = Signal(str, str)   # kind, id

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.kind = ""
        self.ident = ""
        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(16, 16, 16, 16)
        self._root.setSpacing(14)
        self.show_selection("", "")

    def set_project(self, project):
        self.project = project
        self.show_selection("", "")

    # ------------------------------------------------------------------ build
    def _clear(self):
        while self._root.count():
            item = self._root.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def _overline(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("Overline")
        return lbl

    def _row(self, label, widget):
        row = QVBoxLayout()
        row.setSpacing(5)
        head = QHBoxLayout()
        head.addWidget(QLabel(label))
        head.addStretch(1)
        self._value_lbl = QLabel("")
        self._value_lbl.setStyleSheet(f"color:{theme.PRIMARY};font-weight:600;")
        head.addWidget(self._value_lbl)
        row.addLayout(head)
        row.addWidget(widget)
        holder = QWidget()
        holder.setLayout(row)
        return holder, self._value_lbl

    def show_selection(self, kind, ident):
        self.kind, self.ident = kind, ident
        self._clear()
        if not self.project or not kind:
            self._root.addWidget(self._overline("Properties"))
            hint = QLabel("Select a clip, zoom, or caption on the timeline to edit it.")
            hint.setObjectName("Faint")
            hint.setWordWrap(True)
            self._root.addWidget(hint)
            self._root.addStretch(1)
            return
        if kind == "clip":
            self._build_clip(self.project.find_clip(ident))
        elif kind == "zoom":
            self._build_zoom(self.project.find_zoom(ident))
        elif kind == "caption":
            self._build_caption(self.project.find_caption(ident))
        self._root.addStretch(1)
        self._add_delete_button(kind)

    def _add_delete_button(self, kind):
        btn = QPushButton(f"Delete {kind}")
        btn.setObjectName("Danger")
        btn.clicked.connect(lambda: self.deleteRequested.emit(self.kind, self.ident))
        self._root.addWidget(btn)

    # ------------------------------------------------------------------- clip
    def _build_clip(self, clip):
        if not clip:
            return
        media = self.project.media_for(clip)
        self._root.addWidget(self._overline("Selected clip"))
        name = QLabel(media.name if media else "Clip")
        name.setObjectName("H2")
        self._root.addWidget(name)
        meta = QLabel(f"Screen recording · {clip.duration:.1f}s")
        meta.setObjectName("Faint")
        self._root.addWidget(meta)

        speed = QComboBox()
        speeds = [0.5, 1.0, 1.5, 2.0]
        speed.addItems(["0.5×", "1×", "1.5×", "2×"])
        speed.setCurrentIndex(speeds.index(clip.speed) if clip.speed in speeds else 1)

        def set_speed(i):
            clip.speed = speeds[i]
            self.changed.emit()

        speed.currentIndexChanged.connect(set_speed)
        holder, _ = self._row("Playback speed", speed)
        self._root.addWidget(holder)

        vol = QSlider(Qt.Horizontal)
        vol.setRange(0, 100)
        vol.setValue(int(clip.volume * 100))
        holder, vlbl = self._row("Clip volume", vol)
        vlbl.setText(f"{int(clip.volume * 100)}%")

        def set_vol(v):
            clip.volume = v / 100
            vlbl.setText(f"{v}%")
            self.changed.emit()

        vol.valueChanged.connect(set_vol)
        self._root.addWidget(holder)

    # ------------------------------------------------------------------- zoom
    def _build_zoom(self, z):
        if not z:
            return
        self._root.addWidget(self._overline("Zoom highlight"))
        title = QLabel("Push-in")
        title.setObjectName("H2")
        self._root.addWidget(title)

        level = QSlider(Qt.Horizontal)
        level.setRange(100, 300)
        level.setValue(int(z.level * 100))
        holder, llbl = self._row("Zoom level", level)
        llbl.setText(f"{z.level:.1f}×")

        def set_level(v):
            z.level = v / 100
            llbl.setText(f"{z.level:.1f}×")
            self.changed.emit()

        level.valueChanged.connect(set_level)
        self._root.addWidget(holder)

        for axis, attr in (("Focus X", "focus_x"), ("Focus Y", "focus_y")):
            s = QSlider(Qt.Horizontal)
            s.setRange(0, 100)
            s.setValue(int(getattr(z, attr) * 100))
            holder, lbl = self._row(axis, s)
            lbl.setText(f"{int(getattr(z, attr) * 100)}%")

            def make(attr, lbl):
                def f(v):
                    setattr(z, attr, v / 100)
                    lbl.setText(f"{v}%")
                    self.changed.emit()
                return f

            s.valueChanged.connect(make(attr, lbl))
            self._root.addWidget(holder)

        self._root.addWidget(self._timing_row(z))

    # ---------------------------------------------------------------- caption
    def _build_caption(self, cap):
        if not cap:
            return
        self._root.addWidget(self._overline("Caption"))
        edit = QPlainTextEdit(cap.text)
        edit.setFixedHeight(90)

        def set_text():
            cap.text = edit.toPlainText()
            self.changed.emit()

        edit.textChanged.connect(set_text)
        self._root.addWidget(QLabel("Text"))
        self._root.addWidget(edit)
        self._root.addWidget(self._timing_row(cap))

    # ------------------------------------------------------------------ timing
    def _timing_row(self, item):
        box = QFrame()
        h = QHBoxLayout(box)
        h.setContentsMargins(0, 0, 0, 0)
        for label, attr in (("Start", "start"), ("End", "end")):
            col = QVBoxLayout()
            col.addWidget(QLabel(label))
            spin = QDoubleSpinBox()
            spin.setRange(0, 100000)
            spin.setSingleStep(0.25)
            spin.setSuffix(" s")
            spin.setValue(getattr(item, attr))

            def make(attr, spin):
                def f():
                    setattr(item, attr, spin.value())
                    self.changed.emit()
                return f

            spin.valueChanged.connect(make(attr, spin))
            col.addWidget(spin)
            h.addLayout(col)
        return box
