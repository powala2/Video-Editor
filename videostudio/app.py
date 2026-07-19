"""Application entry point."""

from __future__ import annotations

import os
import sys


def main() -> int:
    # High-DPI friendliness before the QApplication exists.
    os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")

    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QIcon

    from . import theme
    from .ui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName("Video Studio")
    app.setOrganizationName("Water Resources")
    app.setStyleSheet(theme.STYLESHEET)

    icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    win = MainWindow()
    win.showMaximized()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
