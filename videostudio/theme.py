"""Dark palette and Qt stylesheet, styled after Adobe Premiere Pro.

Layout language: near-black window background, slightly lighter panel
surfaces separated by dark gutters, low-glare grey text, and a violet
accent for primary actions and selection (matching the recording overlay).
Track colours are muted chips that read on the dark timeline.
"""

# Accent (shared with the recording overlay).
PRIMARY = "#8b7bff"        # violet accent — primary buttons, selection, focus
PRIMARY_DEEP = "#a99cff"   # accent hover / emphasis (lighter, since bg is dark)
PRIMARY_TINT = "#2e2a45"   # translucent-looking selection wash

# Chrome.
BG = "#131316"             # window background (the dark gutters between panels)
SURFACE = "#1e1e23"        # panel bodies
SURFACE_2 = "#28282f"      # inputs, raised rows, hover fills
BORDER = "#34343c"         # hairline separators
TEXT = "#e9e9ee"
TEXT_MUTED = "#a7a7b2"
TEXT_FAINT = "#6f6f7c"

# Status.
GOLD = "#d4b45c"
WARNING_BG = "#3a2f14"
WARNING_INK = "#e0b95c"
DANGER = "#ff5155"

# Timeline.
PLAYHEAD = "#4aa3ff"          # Premiere-style blue playhead
TRACK_SCREEN = "#4c4390"      # video clip fill
TRACK_SCREEN_EDGE = "#6e5fd6" # video clip border
TRACK_SCREEN_INK = "#efeaff"  # video clip label
TRACK_ZOOM = "#d4b45c"        # zoom border / label
TRACK_ZOOM_BG = "#372c12"     # zoom fill
TRACK_CAPTION = "#3fb6c9"     # caption border / label
TRACK_CAPTION_BG = "#12333a"  # caption fill

# Recording overlay (kept in the same family as the app chrome).
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
    font-size: 13px;
    color: {TEXT};
}}
QMainWindow, QWidget#Root {{ background: {BG}; }}
QWidget#Card, QFrame#Panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}
QWidget#Card:hover {{ border-color: {PRIMARY}; }}
QLabel#H1 {{ font-size: 24px; font-weight: 700; color: {TEXT}; }}
QLabel#H2 {{ font-size: 17px; font-weight: 700; color: {TEXT}; }}
QLabel#Overline {{
    font-size: 11px; font-weight: 700; letter-spacing: 2px; color: {TEXT_FAINT};
}}
QLabel#Muted {{ color: {TEXT_MUTED}; }}
QLabel#Faint {{ color: {TEXT_FAINT}; font-size: 12px; }}

QPushButton {{
    background: {SURFACE_2};
    border: 1px solid #3a3a44;
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 13px;
    color: #c9c9d2;
}}
QPushButton:hover {{ background: #32323a; border-color: #4a4a55; color: {TEXT}; }}
QPushButton:pressed {{ background: #212127; }}
QPushButton:disabled {{ color: #55555f; border-color: #2c2c33; }}
QPushButton#Primary {{
    background: {PRIMARY}; border: 1px solid {PRIMARY}; color: white; font-weight: 600;
}}
QPushButton#Primary:hover {{ background: {PRIMARY_DEEP}; border-color: {PRIMARY_DEEP}; color: white; }}
QPushButton#Danger:hover {{ border-color: {DANGER}; color: {DANGER}; }}
QPushButton#Ghost {{ background: transparent; border: none; color: {TEXT_MUTED}; }}
QPushButton#Ghost:hover {{ color: {TEXT}; background: {SURFACE_2}; }}
QPushButton#Tool {{ padding: 6px 12px; }}
QPushButton#Tab {{
    background: transparent; border: none; border-bottom: 2px solid transparent;
    border-radius: 0; padding: 8px 12px; color: {TEXT_FAINT}; font-weight: 600;
}}
QPushButton#Tab:checked {{ color: {TEXT}; border-bottom: 2px solid {PRIMARY}; }}

QScrollArea {{ background: transparent; border: none; }}
QScrollArea > QWidget > QWidget {{ background: transparent; }}

QListWidget {{
    background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 8px;
    padding: 4px; outline: none;
}}
QListWidget::item {{ padding: 8px; border-radius: 6px; color: {TEXT_MUTED}; }}
QListWidget::item:hover {{ background: {SURFACE_2}; }}
QListWidget::item:selected {{ background: {PRIMARY_TINT}; color: {PRIMARY_DEEP}; }}

QLineEdit, QComboBox, QPlainTextEdit, QSpinBox, QDoubleSpinBox {{
    background: {SURFACE_2}; border: 1px solid #3a3a44; border-radius: 6px;
    padding: 7px 10px; font-size: 13px; color: {TEXT};
    selection-background-color: {PRIMARY_TINT};
}}
QLineEdit:focus, QComboBox:focus, QPlainTextEdit:focus {{ border-color: {PRIMARY}; }}
QComboBox::drop-down {{ border: none; width: 22px; }}
QComboBox QAbstractItemView {{
    background: {SURFACE_2}; color: {TEXT}; border: 1px solid {BORDER};
    selection-background-color: {PRIMARY_TINT};
}}

QSlider::groove:horizontal {{ height: 4px; background: #3a3a44; border-radius: 2px; }}
QSlider::sub-page:horizontal {{ background: {PRIMARY}; border-radius: 2px; }}
QSlider::handle:horizontal {{
    background: #e2e2ea; border: 2px solid {PRIMARY}; width: 12px; height: 12px;
    margin: -6px 0; border-radius: 8px;
}}

QScrollBar:vertical {{ background: transparent; width: 10px; margin: 0; }}
QScrollBar::handle:vertical {{ background: #3f3f49; border-radius: 5px; min-height: 30px; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 0; }}
QScrollBar::handle:horizontal {{ background: #3f3f49; border-radius: 5px; min-width: 30px; }}
QScrollBar::handle:hover {{ background: #52525e; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; width: 0; }}

QMenuBar {{ background: {BG}; color: {TEXT_MUTED}; }}
QMenuBar::item {{ padding: 6px 10px; background: transparent; }}
QMenuBar::item:selected {{ background: {SURFACE_2}; color: {TEXT}; }}
QMenu {{ background: {SURFACE}; border: 1px solid {BORDER}; padding: 4px; }}
QMenu::item {{ padding: 6px 18px; border-radius: 4px; }}
QMenu::item:selected {{ background: {PRIMARY_TINT}; }}

QMessageBox, QProgressDialog {{ background: {SURFACE}; }}
QProgressBar {{
    background: {SURFACE_2}; border: 1px solid {BORDER}; border-radius: 6px;
    text-align: center; color: {TEXT};
}}
QProgressBar::chunk {{ background: {PRIMARY}; border-radius: 5px; }}

QToolTip {{
    background: #0d0d10; color: #d6d6de; border: 1px solid #3a3a44; padding: 6px 8px;
}}
"""
