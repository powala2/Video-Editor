"""Top-level window: switches between the library and the editor."""

from __future__ import annotations

from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox

from .. import __version__
from ..model import Project
from . import updates
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

        self._build_menu()
        self.library.refresh()

        # Check for updates shortly after launch (packaged builds only).
        QTimer.singleShot(1500, lambda: updates.run_startup_check(self))

    def _build_menu(self):
        menu = self.menuBar().addMenu("&Help")
        check = QAction("Check for updates…", self)
        check.triggered.connect(lambda: updates.manual_check(self))
        menu.addAction(check)
        about = QAction("About Video Studio", self)
        about.triggered.connect(self._about)
        menu.addAction(about)

    def _about(self):
        QMessageBox.about(
            self, "About Video Studio",
            f"<b>Video Studio</b> {__version__}<br>"
            "Screen recorder and video editor for the Water Resources "
            "training program.<br><br>Updates install automatically from the "
            "project's public releases.",
        )

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
