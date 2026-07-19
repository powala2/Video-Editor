"""The editing timeline: a custom-painted track view.

Lanes (top to bottom): ruler, Zoom, Screen (video clips), Captions. Supports
click-to-seek on the ruler, selecting clips/zooms/captions, and trimming a
clip by dragging its left/right edge. Split / delete / add-zoom / add-caption
are driven from the toolbar in the editor and mutate the shared project.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PySide6.QtWidgets import QWidget, QSizePolicy

from .. import theme

RULER_H = 26
LANE_ZOOM = 28
LANE_CLIP = 50
LANE_CAP = 30
LANE_GAP = 6
LEFT_PAD = 8


def _fmt(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02d}"


class TimelineWidget(QWidget):
    seekRequested = Signal(float)
    selectionChanged = Signal(str, str)   # kind ('clip'|'zoom'|'caption'|''), id
    edited = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.pps = 45.0                    # pixels per second
        self.playhead = 0.0
        self.sel_kind = ""
        self.sel_id = ""
        self._drag = None                  # ('trim-in'|'trim-out', clip_id)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setMinimumHeight(RULER_H + LANE_ZOOM + LANE_CLIP + LANE_CAP + 4 * LANE_GAP + 10)

    # -------------------------------------------------------------- helpers
    def set_project(self, project):
        self.project = project
        self.sel_kind, self.sel_id = "", ""
        self._relayout()

    def set_playhead(self, t: float):
        self.playhead = t
        self.update()

    def set_pps(self, pps: float):
        self.pps = pps
        self._relayout()

    def select(self, kind: str, ident: str):
        self.sel_kind, self.sel_id = kind, ident
        self.update()
        self.selectionChanged.emit(kind, ident)

    def _total(self):
        return self.project.total_duration() if self.project else 0.0

    def _relayout(self):
        width = int(LEFT_PAD * 2 + max(self._total(), 8) * self.pps)
        self.setMinimumWidth(width)
        self.resize(width, self.minimumHeight())
        self.update()

    def _x(self, t):
        return LEFT_PAD + t * self.pps

    def _t(self, x):
        return max(0.0, (x - LEFT_PAD) / self.pps)

    def _lane_y(self, name):
        y = RULER_H + LANE_GAP
        if name == "zoom":
            return y, LANE_ZOOM
        y += LANE_ZOOM + LANE_GAP
        if name == "clip":
            return y, LANE_CLIP
        y += LANE_CLIP + LANE_GAP
        return y, LANE_CAP

    # ---------------------------------------------------------------- paint
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        W, H = self.width(), self.height()
        p.fillRect(self.rect(), QColor(theme.SURFACE_2))
        if not self.project:
            return

        total = self._total()

        # ruler
        p.setPen(QColor(theme.BORDER))
        p.drawLine(0, RULER_H, W, RULER_H)
        p.setFont(QFont("Segoe UI", 8))
        step = 5 if self.pps >= 30 else 10
        p.setPen(QColor(theme.TEXT_FAINT))
        t = 0
        while t <= total + step:
            x = self._x(t)
            p.drawLine(int(x), RULER_H - 6, int(x), RULER_H)
            p.drawText(int(x) + 3, 14, _fmt(t))
            t += step

        self._paint_lane_label(p, "zoom", "Zoom", theme.WARNING_INK)
        self._paint_lane_label(p, "clip", "Screen", theme.PRIMARY_DEEP)
        self._paint_lane_label(p, "cap", "CC", theme.TRACK_CAPTION)

        # zoom blocks
        zy, zh = self._lane_y("zoom")
        for z in self.project.zooms:
            self._block(p, self._x(z.start), zy + 2, (z.end - z.start) * self.pps, zh - 4,
                        QColor(theme.WARNING_BG), QColor(theme.TRACK_ZOOM), f"{z.level:.1f}×",
                        selected=(self.sel_kind == "zoom" and self.sel_id == z.id),
                        ink=QColor(theme.WARNING_INK))

        # clips
        cy, ch = self._lane_y("clip")
        start = 0.0
        for c in self.project.clips:
            media = self.project.media_for(c)
            label = media.name if media else "clip"
            self._block(p, self._x(start), cy + 2, c.duration * self.pps, ch - 4,
                        QColor(theme.PRIMARY), QColor(theme.PRIMARY_DEEP), label,
                        selected=(self.sel_kind == "clip" and self.sel_id == c.id),
                        ink=QColor("#eaf2eb"), fill_solid=True)
            start += c.duration

        # captions
        py, ph = self._lane_y("cap")
        for cap in self.project.captions:
            self._block(p, self._x(cap.start), py + 2, cap.duration * self.pps, ph - 4,
                        QColor("#dceaed"), QColor(theme.TRACK_CAPTION),
                        (cap.text[:18] + "…") if len(cap.text) > 18 else cap.text,
                        selected=(self.sel_kind == "caption" and self.sel_id == cap.id),
                        ink=QColor(theme.TRACK_CAPTION))

        # playhead
        px = self._x(self.playhead)
        p.setPen(QPen(QColor(theme.DANGER), 2))
        p.drawLine(int(px), 0, int(px), H)
        p.setBrush(QColor(theme.DANGER))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(QRectF(px - 5, 0, 10, 9), 2, 2)

    def _paint_lane_label(self, p, name, text, color):
        y, h = self._lane_y(name)
        p.setPen(QColor(color))
        p.setFont(QFont("Segoe UI", 8, QFont.Bold))
        p.drawText(4, int(y) - 1, text)

    def _block(self, p, x, y, w, h, fill, border, text, selected, ink, fill_solid=False):
        w = max(6, w)
        rect = QRectF(x, y, w, h)
        p.setBrush(QBrush(fill))
        p.setPen(QPen(QColor(theme.PRIMARY if selected else border.name()),
                      2 if selected else 1))
        p.drawRoundedRect(rect, 5, 5)
        if w > 26:
            p.setPen(QColor(ink))
            p.setFont(QFont("Segoe UI", 8, QFont.Bold))
            p.drawText(rect.adjusted(7, 0, -6, 0), Qt.AlignVCenter | Qt.AlignLeft,
                       p.fontMetrics().elidedText(text, Qt.ElideRight, int(w) - 12))

    # ------------------------------------------------------------ interaction
    def _clip_rect_at(self, x, y):
        cy, ch = self._lane_y("clip")
        if not (cy <= y <= cy + ch):
            return None, None
        start = 0.0
        for c in self.project.clips:
            x0, x1 = self._x(start), self._x(start + c.duration)
            if x0 <= x <= x1:
                return c, (x0, x1)
            start += c.duration
        return None, None

    def mousePressEvent(self, ev):
        if not self.project:
            return
        x, y = ev.position().x(), ev.position().y()
        if y <= RULER_H:
            self.seekRequested.emit(self._t(x))
            return
        # clip lane: select / start trim
        clip, xr = self._clip_rect_at(x, y)
        if clip:
            self.select("clip", clip.id)
            if xr and abs(x - xr[0]) <= 6:
                self._drag = ("trim-in", clip.id)
            elif xr and abs(x - xr[1]) <= 6:
                self._drag = ("trim-out", clip.id)
            return
        # zoom lane
        zy, zh = self._lane_y("zoom")
        if zy <= y <= zy + zh:
            for z in self.project.zooms:
                if self._x(z.start) <= x <= self._x(z.end):
                    self.select("zoom", z.id)
                    return
        # caption lane
        py, ph = self._lane_y("cap")
        if py <= y <= py + ph:
            for cap in self.project.captions:
                if self._x(cap.start) <= x <= self._x(cap.end):
                    self.select("caption", cap.id)
                    return
        self.select("", "")

    def mouseMoveEvent(self, ev):
        x = ev.position().x()
        if self._drag and self.project:
            kind, cid = self._drag
            clip = self.project.find_clip(cid)
            if clip:
                start = self.project.clip_start(clip)
                if kind == "trim-out":
                    new_dur = max(0.1, self._t(x) - start)
                    self.project.trim_clip(cid, out_point=clip.in_point + new_dur * clip.speed)
                else:
                    delta = self._t(x) - start
                    self.project.trim_clip(cid, in_point=clip.in_point + delta * clip.speed)
                self._relayout()
                self.edited.emit()
            return
        # hover cursor near edges
        clip, xr = self._clip_rect_at(x, ev.position().y())
        if clip and xr and (abs(x - xr[0]) <= 6 or abs(x - xr[1]) <= 6):
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, _):
        if self._drag:
            self._drag = None
            self.edited.emit()
