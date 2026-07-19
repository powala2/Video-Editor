"""The studio home screen — a gallery of saved projects plus entry points."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QFrame,
    QScrollArea,
)

from .. import theme, storage


class ProjectCard(QFrame):
    clicked = Signal(object)

    def __init__(self, project):
        super().__init__()
        self.project = project
        self.setObjectName("Card")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(150)
        v = QVBoxLayout(self)
        v.setContentsMargins(16, 14, 16, 14)
        v.setSpacing(6)
        title = QLabel(project.name)
        title.setObjectName("H2")
        title.setWordWrap(True)
        v.addWidget(title)
        dur = project.total_duration()
        meta = QLabel(f"{len(project.clips)} clip(s) · {int(dur // 60)}:{int(dur % 60):02d}"
                      f" · {len(project.captions)} caption(s)")
        meta.setObjectName("Faint")
        v.addWidget(meta)
        v.addStretch(1)
        open_lbl = QLabel("Open →")
        open_lbl.setStyleSheet(f"color:{theme.PRIMARY};font-weight:600;")
        v.addWidget(open_lbl)

    def mousePressEvent(self, ev):
        self.clicked.emit(self.project)


class LibraryView(QWidget):
    openProject = Signal(object)
    newRecording = Signal()
    importVideo = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Root")
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._header())

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.NoFrame)
        self._body = QWidget()
        self._body.setObjectName("Root")
        self._grid = QGridLayout(self._body)
        self._grid.setContentsMargins(40, 28, 40, 40)
        self._grid.setSpacing(20)
        self._grid.setAlignment(Qt.AlignTop)
        self._scroll.setWidget(self._body)
        root.addWidget(self._scroll, 1)

    def _header(self):
        bar = QFrame()
        bar.setObjectName("Header")
        bar.setStyleSheet(
            f"QFrame#Header {{ background:{theme.SURFACE};"
            f"border-bottom:1px solid {theme.BORDER}; }}"
        )
        h = QHBoxLayout(bar)
        h.setContentsMargins(40, 20, 40, 20)
        col = QVBoxLayout()
        over = QLabel("WATER RESOURCES")
        over.setObjectName("Overline")
        col.addWidget(over)
        title = QLabel("Video Studio")
        title.setObjectName("H1")
        col.addWidget(title)
        h.addLayout(col)
        h.addStretch(1)
        imp = QPushButton("⬆  Import video")
        imp.clicked.connect(self.importVideo.emit)
        h.addWidget(imp)
        rec = QPushButton("●  New recording")
        rec.setObjectName("Primary")
        rec.clicked.connect(self.newRecording.emit)
        h.addWidget(rec)
        return bar

    def refresh(self):
        while self._grid.count():
            w = self._grid.takeAt(0).widget()
            if w:
                w.deleteLater()
        projects = storage.list_projects()
        if not projects:
            empty = QLabel("No recordings yet.\nStart a new recording or import a video to begin.")
            empty.setObjectName("Muted")
            empty.setAlignment(Qt.AlignCenter)
            self._grid.addWidget(empty, 0, 0, 1, 3)
            return
        cols = 3
        for i, p in enumerate(projects):
            card = ProjectCard(p)
            card.clicked.connect(self.openProject.emit)
            self._grid.addWidget(card, i // cols, i % cols)
