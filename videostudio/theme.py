"""Brand palette and Qt stylesheet.

Colours are lifted from the GHA Water Resources design system (forest green +
warm paper). Sizes are deliberately comfortable — the original design used
9–13px type tuned for a mockup; here everything is scaled up for real use.
"""

PRIMARY = "#2f6b4c"
PRIMARY_DEEP = "#234c39"
PRIMARY_TINT = "#e9f1eb"
BG = "#f1ede3"
SURFACE = "#ffffff"
SURFACE_2 = "#f7f4ec"
BORDER = "#ddd6c6"
TEXT = "#2b332e"
TEXT_MUTED = "#5c6660"
TEXT_FAINT = "#8a8570"
GOLD = "#a88a3e"
WARNING_BG = "#f6ecd1"
WARNING_INK = "#8a6a1e"
DANGER = "#b4553e"
TRACK_SCREEN = "#2f6b4c"
TRACK_ZOOM = "#c9a94e"
TRACK_CAPTION = "#3b7f8a"

# --- Recording overlay: a self-contained dark "Premiere Pro" palette. The
# capture HUD floats over the user's whole screen, so it reads far better as a
# dark, low-glare panel than as the light app chrome above.
REC_PANEL = "#1b1b1f"       # panel body
REC_PANEL_2 = "#232329"     # raised rows / chips
REC_BORDER = "#34343c"      # hairline separators
REC_TRACK = "#2c2c33"       # unfilled countdown ring
REC_TEXT = "#f4f4f6"        # primary text
REC_TEXT_MUTED = "#a7a7b2"  # secondary text
REC_TEXT_FAINT = "#6f6f7c"  # captions
REC_ACCENT = "#8b7bff"      # Premiere-style violet
REC_ACCENT_HI = "#b3a6ff"   # accent highlight for the ring sweep
REC_REC = "#ff5155"         # the live "recording" red

STYLESHEET = f"""
* {{
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
    color: {TEXT};
}}
QMainWindow, QWidget#Root {{ background: {BG}; }}
QWidget#Card, QFrame#Panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}
QLabel#H1 {{ font-size: 26px; font-weight: 700; color: {PRIMARY_DEEP}; }}
QLabel#H2 {{ font-size: 19px; font-weight: 700; color: {PRIMARY_DEEP}; }}
QLabel#Overline {{
    font-size: 11px; font-weight: 700; letter-spacing: 2px; color: {TEXT_FAINT};
}}
QLabel#Muted {{ color: {TEXT_MUTED}; }}
QLabel#Faint {{ color: {TEXT_FAINT}; font-size: 12px; }}

QPushButton {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 9px 15px;
    font-size: 14px;
    color: {TEXT_MUTED};
}}
QPushButton:hover {{ border-color: {PRIMARY}; color: {PRIMARY}; }}
QPushButton:disabled {{ color: #b7b1a2; border-color: #eae4d6; }}
QPushButton#Primary {{
    background: {PRIMARY}; border: 1px solid {PRIMARY}; color: white; font-weight: 600;
}}
QPushButton#Primary:hover {{ background: {PRIMARY_DEEP}; border-color: {PRIMARY_DEEP}; color: white; }}
QPushButton#Danger:hover {{ border-color: {DANGER}; color: {DANGER}; }}
QPushButton#Ghost {{ background: transparent; border: none; color: {TEXT_MUTED}; }}
QPushButton#Ghost:hover {{ color: {PRIMARY}; background: {SURFACE_2}; }}
QPushButton#Tool {{ padding: 7px 13px; }}
QPushButton#Tab {{
    background: transparent; border: none; border-bottom: 2px solid transparent;
    border-radius: 0; padding: 8px 12px; color: {TEXT_FAINT}; font-weight: 600;
}}
QPushButton#Tab:checked {{ color: {PRIMARY_DEEP}; border-bottom: 2px solid {PRIMARY}; }}

QListWidget {{
    background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 10px;
    padding: 4px; outline: none;
}}
QListWidget::item {{ padding: 8px; border-radius: 8px; }}
QListWidget::item:selected {{ background: {PRIMARY_TINT}; color: {PRIMARY_DEEP}; }}

QLineEdit, QComboBox, QPlainTextEdit, QSpinBox, QDoubleSpinBox {{
    background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 8px;
    padding: 7px 10px; font-size: 14px;
}}
QLineEdit:focus, QComboBox:focus, QPlainTextEdit:focus {{ border-color: {PRIMARY}; }}
QComboBox::drop-down {{ border: none; width: 22px; }}

QSlider::groove:horizontal {{ height: 5px; background: #e2dccd; border-radius: 3px; }}
QSlider::sub-page:horizontal {{ background: {PRIMARY}; border-radius: 3px; }}
QSlider::handle:horizontal {{
    background: white; border: 2px solid {PRIMARY}; width: 14px; height: 14px;
    margin: -6px 0; border-radius: 9px;
}}

QScrollBar:vertical {{ background: transparent; width: 11px; margin: 0; }}
QScrollBar::handle:vertical {{ background: #cfc7b0; border-radius: 5px; min-height: 30px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}

QToolTip {{ background: {PRIMARY_DEEP}; color: #eaf2eb; border: none; padding: 6px 8px; }}
"""
