"""The editor screen: preview + media bin + properties + timeline + toolbar."""

from __future__ import annotations

import os

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame,
    QListWidget, QListWidgetItem, QScrollArea, QSlider, QFileDialog, QMessageBox,
    QProgressDialog, QApplication, QPlainTextEdit, QAbstractSpinBox,
)

from .. import theme, storage
from ..model import MediaItem
from ..media import probe
from ..recorder import ScreenRecorder
from .preview import PreviewPanel
from .timeline import TimelineWidget
from .properties import PropertiesPanel
from .dialogs import RecordingHUD, ExportWorker

VIDEO_FILTER = "Video files (*.mp4 *.mov *.webm *.mkv *.avi *.m4v);;All files (*)"


class EditorView(QWidget):
    backRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Root")
        self.project = None
        self.playhead = 0.0
        self.sel_kind = ""
        self.sel_id = ""
        self._build()

    # --------------------------------------------------------------- build UI
    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._topbar())

        mid = QHBoxLayout()
        mid.setContentsMargins(12, 12, 12, 8)
        mid.setSpacing(12)
        mid.addWidget(self._left_panel(), 0)
        self.preview = PreviewPanel()
        mid.addWidget(self.preview, 1)
        mid.addWidget(self._right_panel(), 0)
        wrap = QWidget()
        wrap.setLayout(mid)
        root.addWidget(wrap, 1)

        root.addWidget(self._timeline_area())

        # wiring
        self.preview.positionChanged.connect(self._on_position)
        self.timeline.seekRequested.connect(self.preview.seek)
        self.timeline.selectionChanged.connect(self._on_selection)
        self.timeline.edited.connect(self._on_edited)
        self.props.changed.connect(self._on_edited)
        self.props.deleteRequested.connect(self._delete_item)

        self._add_shortcuts()

    # ------------------------------------------------------------- shortcuts
    def _add_shortcuts(self):
        """Editor-wide keys. Plain-letter keys are suppressed while the user
        is typing in a text field so they don't eat keystrokes."""

        def guarded(fn, typing_guard=True):
            def run():
                # The window-level shortcut fires even while the library screen
                # is shown — only act when the editor itself is visible.
                if not self.isVisible():
                    return
                if typing_guard:
                    w = QApplication.focusWidget()
                    if isinstance(w, (QLineEdit, QPlainTextEdit, QAbstractSpinBox)):
                        return
                fn()
            return run

        for seq, fn, guard in (
            ("Space", lambda: self.preview.toggle(), True),
            ("C", self.split_at_playhead, True),
            ("Ctrl+K", self.split_at_playhead, False),
            ("Delete", self.delete_selected, True),
            ("Backspace", self.delete_selected, True),
            ("Z", self.add_zoom, True),
            ("T", self.add_caption, True),
            ("R", self.record, True),
            ("I", self.import_video, True),
            ("Left", lambda: self.preview.jump(-1.0), True),
            ("Right", lambda: self.preview.jump(1.0), True),
            ("Shift+Left", lambda: self.preview.jump(-5.0), True),
            ("Shift+Right", lambda: self.preview.jump(5.0), True),
            ("Home", lambda: self.preview.seek(0.0), True),
            ("Ctrl+E", self.export_video, False),
            ("F1", self.show_help, False),
        ):
            sc = QShortcut(QKeySequence(seq), self)
            sc.activated.connect(guarded(fn, typing_guard=guard))

    def show_help(self):
        box = QMessageBox(self)
        box.setWindowTitle("How to use Video Studio")
        box.setTextFormat(Qt.RichText)
        box.setText(
            "<h3 style='margin-top:0'>Workflow</h3>"
            "<ol style='margin-left:-18px'>"
            "<li><b>Record</b> your screen or <b>Import</b> a video — it lands "
            "on the <b>V1</b> track of the timeline.</li>"
            "<li><b>Click a block</b> on the timeline to select it; its "
            "settings appear in the right-hand panel.</li>"
            "<li><b>Drag a clip's left/right edge</b> to trim it. "
            "<b>Split</b> cuts at the blue playhead.</li>"
            "<li>Add <b>Zoom</b> push-ins (FX track) and <b>Captions</b> "
            "(T1 track), then <b>Save video</b> to render the MP4.</li>"
            "</ol>"
            "<h3>Keyboard shortcuts</h3>"
            "<table cellspacing='0' cellpadding='3'>"
            "<tr><td><b>Space</b></td><td>Play / pause</td>"
            "<td width='30'></td><td><b>C</b> / <b>Ctrl+K</b></td><td>Split at playhead</td></tr>"
            "<tr><td><b>Del</b></td><td>Delete selected</td>"
            "<td></td><td><b>Z</b> / <b>T</b></td><td>Add zoom / caption</td></tr>"
            "<tr><td><b>R</b> / <b>I</b></td><td>Record / import</td>"
            "<td></td><td><b>← →</b></td><td>Step 1 s (Shift: 5 s)</td></tr>"
            "<tr><td><b>Home</b></td><td>Jump to start</td>"
            "<td></td><td><b>Ctrl+E</b></td><td>Save video</td></tr>"
            "</table>"
        )
        box.exec()

    def _topbar(self):
        bar = QFrame()
        bar.setObjectName("TopBar")
        bar.setStyleSheet(
            f"QFrame#TopBar {{ background:{theme.SURFACE};"
            f"border-bottom:1px solid {theme.BORDER}; }}"
        )
        h = QHBoxLayout(bar)
        h.setContentsMargins(14, 10, 14, 10)
        h.setSpacing(10)
        back = QPushButton("‹  Studio")
        back.setObjectName("Ghost")
        back.setToolTip("Back to your project library")
        back.clicked.connect(self.backRequested.emit)
        h.addWidget(back)

        self.name_edit = QLineEdit("Untitled project")
        self.name_edit.setStyleSheet(
            f"font-size:15px;font-weight:600;color:{theme.TEXT};"
            f"border:none;background:transparent;"
        )
        self.name_edit.setToolTip("Project name — click to rename")
        self.name_edit.editingFinished.connect(self._rename)
        h.addWidget(self.name_edit, 1)

        help_btn = QPushButton("?")
        help_btn.setObjectName("Tool")
        help_btn.setFixedWidth(34)
        help_btn.setToolTip("How to use Video Studio (F1)")
        help_btn.clicked.connect(self.show_help)
        h.addWidget(help_btn)

        self.export_btn = QPushButton("Save video")
        self.export_btn.setObjectName("Primary")
        self.export_btn.setToolTip("Render the timeline to an MP4 file (Ctrl+E)")
        self.export_btn.clicked.connect(self.export_video)
        h.addWidget(self.export_btn)
        return bar

    def _left_panel(self):
        panel = QFrame()
        panel.setObjectName("Panel")
        panel.setFixedWidth(232)
        v = QVBoxLayout(panel)
        v.setContentsMargins(12, 12, 12, 12)
        v.setSpacing(10)
        lbl = QLabel("PROJECT MEDIA")
        lbl.setObjectName("Overline")
        v.addWidget(lbl)
        self.bin = QListWidget()
        self.bin.setToolTip("Media used in this project — click to jump to it "
                            "on the timeline")
        self.bin.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.bin.setTextElideMode(Qt.ElideRight)
        self.bin.itemClicked.connect(self._bin_clicked)
        v.addWidget(self.bin, 1)
        imp = QPushButton("＋  Import video")
        imp.setToolTip("Add a video file to the timeline (I)")
        imp.clicked.connect(self.import_video)
        v.addWidget(imp)
        rec = QPushButton("●  Record screen")
        rec.setObjectName("Primary")
        rec.setToolTip("Capture your screen and microphone (R)")
        rec.clicked.connect(self.record)
        v.addWidget(rec)
        return panel

    def _right_panel(self):
        panel = QFrame()
        panel.setObjectName("Panel")
        panel.setFixedWidth(300)
        v = QVBoxLayout(panel)
        v.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.props = PropertiesPanel()
        scroll.setWidget(self.props)
        v.addWidget(scroll)
        return panel

    def _timeline_area(self):
        frame = QFrame()
        frame.setObjectName("TimelineBar")
        frame.setStyleSheet(
            f"QFrame#TimelineBar {{ background:{theme.SURFACE};"
            f"border-top:1px solid {theme.BORDER}; }}"
        )
        frame.setFixedHeight(214)
        v = QVBoxLayout(frame)
        v.setContentsMargins(12, 8, 12, 10)
        v.setSpacing(8)

        tools = QHBoxLayout()
        tools.setSpacing(6)
        for text, slot, tip in (
            ("Split", self.split_at_playhead,
             "Cut the clip in two at the playhead (C or Ctrl+K)"),
            ("Delete", self.delete_selected,
             "Remove the selected clip, zoom or caption (Del)"),
            ("＋ Zoom", self.add_zoom,
             "Add a push-in zoom at the playhead — appears on the FX track (Z)"),
            ("＋ Caption", self.add_caption,
             "Add a text caption at the playhead — appears on the T1 track (T)"),
        ):
            b = QPushButton(text)
            b.setObjectName("Tool")
            b.setToolTip(tip)
            b.clicked.connect(slot)
            tools.addWidget(b)
        tools.addStretch(1)
        zl = QLabel("Zoom")
        zl.setObjectName("Faint")
        tools.addWidget(zl)
        zoom = QSlider(Qt.Horizontal)
        zoom.setFixedWidth(120)
        zoom.setRange(12, 120)
        zoom.setValue(45)
        zoom.setToolTip("Timeline zoom — spread the tracks out or fit more in view")
        zoom.valueChanged.connect(lambda v: self.timeline.set_pps(float(v)))
        tools.addWidget(zoom)
        v.addLayout(tools)

        self.timeline = TimelineWidget()
        area = QScrollArea()
        area.setWidgetResizable(False)
        area.setWidget(self.timeline)
        area.setFrameShape(QFrame.NoFrame)
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        v.addWidget(area, 1)
        return frame

    # ------------------------------------------------------------- project io
    def set_project(self, project):
        self.project = project
        self.name_edit.setText(project.name)
        self.preview.set_project(project)
        self.timeline.set_project(project)
        self.props.set_project(project)
        self._refresh_bin()
        self._save()

    def _refresh_bin(self):
        self.bin.clear()
        seen = set()
        for c in self.project.clips:
            m = self.project.media_for(c)
            if m and m.id not in seen:
                seen.add(m.id)
                it = QListWidgetItem(f"{m.name}\n{m.duration:.1f}s")
                it.setData(Qt.UserRole, m.id)
                self.bin.addItem(it)

    def _rename(self):
        if self.project:
            self.project.name = self.name_edit.text().strip() or "Untitled project"
            self._save()

    def _save(self):
        if self.project:
            storage.save_project(self.project)

    # --------------------------------------------------------------- reactions
    def _on_position(self, t):
        self.playhead = t
        self.timeline.set_playhead(t)

    def _on_selection(self, kind, ident):
        self.sel_kind, self.sel_id = kind, ident
        self.props.show_selection(kind, ident)

    def _on_edited(self):
        self.preview.refresh()
        self.timeline._relayout()
        self._save()

    def _delete_item(self, kind, ident):
        if kind == "clip":
            self.project.delete_clip(ident)
        elif kind == "zoom":
            self.project.zooms = [z for z in self.project.zooms if z.id != ident]
        elif kind == "caption":
            self.project.captions = [c for c in self.project.captions if c.id != ident]
        self.timeline.select("", "")
        self.props.show_selection("", "")
        self._on_edited()

    def _bin_clicked(self, item):
        mid = item.data(Qt.UserRole)
        t = 0.0
        for c in self.project.clips:
            if c.media_id == mid:
                self.preview.seek(t)
                break
            t += c.duration

    # ----------------------------------------------------------------- editing
    def split_at_playhead(self):
        if self.project and self.project.split_at(self.playhead):
            self._on_edited()

    def delete_selected(self):
        if self.sel_kind:
            self._delete_item(self.sel_kind, self.sel_id)

    def add_zoom(self):
        if not self.project or not self.project.clips:
            return
        total = self.project.total_duration()
        start = min(self.playhead, max(0.0, total - 0.5))
        z = self.project.add_zoom(start, min(start + 2.0, total), level=1.5)
        self.timeline.select("zoom", z.id)
        self._on_edited()

    def add_caption(self):
        if not self.project or not self.project.clips:
            return
        total = self.project.total_duration()
        start = min(self.playhead, max(0.0, total - 0.5))
        cap = self.project.add_caption(start, min(start + 3.0, total), "New caption")
        self.timeline.select("caption", cap.id)
        self._on_edited()

    # ---------------------------------------------------------------- media in
    def _add_media_file(self, path, select=True):
        pr = probe(path)
        if pr.duration <= 0:
            QMessageBox.warning(self, "Import", "That file could not be read as a video.")
            return
        item = self.project.add_media(MediaItem(
            path=path, name=os.path.basename(path), duration=pr.duration,
            width=pr.width, height=pr.height, has_audio=pr.has_audio,
        ))
        if not self.project.width or self.project.width == 1280:
            if pr.width and pr.height:
                self.project.width, self.project.height = pr.width, pr.height
        self.project.append_clip(item.id, 0.0, pr.duration)
        self._refresh_bin()
        self._on_edited()

    def import_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import video", "", VIDEO_FILTER)
        if path:
            self._add_media_file(path)

    def record(self):
        self._recorder = ScreenRecorder(storage.recordings_dir())
        hud = RecordingHUD(self._recorder, self._recording_finished, mic=True, parent=self)
        hud.show()

    def _recording_finished(self, path):
        if path and os.path.exists(path):
            self._add_media_file(path)

    # ------------------------------------------------------------------ export
    def export_video(self):
        if not self.project or not self.project.clips:
            QMessageBox.information(self, "Save video", "Add a clip before saving.")
            return
        default = (self.project.name or "video").replace(" ", "_") + ".mp4"
        path, _ = QFileDialog.getSaveFileName(self, "Save video", default,
                                              "MP4 video (*.mp4)")
        if not path:
            return
        if not path.lower().endswith(".mp4"):
            path += ".mp4"

        dlg = QProgressDialog("Rendering your video…", "Cancel", 0, 100, self)
        dlg.setWindowTitle("Saving")
        dlg.setWindowModality(Qt.WindowModal)
        dlg.setAutoClose(False)
        dlg.setMinimumDuration(0)

        worker = ExportWorker(self.project, path, self)
        worker.progress.connect(lambda f: dlg.setValue(int(f * 100)))
        worker.done.connect(lambda p: self._export_done(dlg, p))
        worker.failed.connect(lambda e: self._export_failed(dlg, e))
        dlg.canceled.connect(worker.terminate)
        self._export_worker = worker
        worker.start()
        dlg.exec()

    def _export_done(self, dlg, path):
        dlg.reset()
        QMessageBox.information(self, "Saved",
                                f"Your video was saved to:\n{path}")

    def _export_failed(self, dlg, err):
        dlg.reset()
        QMessageBox.critical(self, "Export failed", err)
