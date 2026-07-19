"""Top-level window: switches between the library and the editor."""

from __future__ import annotations

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from ..model import Project
from .library import LibraryView
from .editor import EditorView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Studio")
        self.resize(1360, 860)
        self.setMinimumSize(1040, 680)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.library = LibraryView()
        self.editor = EditorView()
        self.stack.addWidget(self.library)
        self.stack.addWidget(self.editor)

        self.library.openProject.connect(self._open_project)
        self.library.newRecording.connect(self._new_recording)
        self.library.importVideo.connect(self._new_import)
        self.editor.backRequested.connect(self._go_home)

        self.library.refresh()

    def _open_project(self, project: Project):
        self.editor.set_project(project)
        self.stack.setCurrentWidget(self.editor)

    def _new_recording(self):
        self.editor.set_project(Project(name="New recording"))
        self.stack.setCurrentWidget(self.editor)
        QTimer.singleShot(120, self.editor.record)

    def _new_import(self):
        self.editor.set_project(Project(name="Imported video"))
        self.stack.setCurrentWidget(self.editor)
        QTimer.singleShot(120, self.editor.import_video)

    def _go_home(self):
        self.library.refresh()
        self.stack.setCurrentWidget(self.library)
