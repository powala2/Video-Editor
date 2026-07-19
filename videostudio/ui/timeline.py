"""The editing timeline: a custom-painted dark track view.

Premiere-style layout: a fixed track-header gutter on the left (FX / V1 / T1),
a time ruler on top, then the Zoom, Video and Caption lanes. Supports
click-or-drag scrubbing on the ruler, selecting clips/zooms/captions, and
trimming a clip by dragging its left/right edge. Split / delete / add-zoom /
add-caption are driven from the toolbar in the editor and mutate the shared
project.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPolygonF
from PySide6.QtWidgets import QWidget, QSizePolicy

from .. import theme

RULER_H = 26
LANE_ZOOM = 28
LANE_CLIP = 52
LANE_CAP = 30
LANE_GAP = 6
GUTTER_W = 58            # fixed track-header column
LEFT_PAD = GUTTER_W + 8  # where t=0 lands


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
        self._scrub_ruler = False
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
        width = int(LEFT_PAD + 8 + max(self._total(), 8) * self.pps)
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
        p.fillRect(self.rect(), QColor(theme.BG))
        if not self.project:
            return

        total = self._total()

        # lane wells (subtle darker strips so empty tracks are visible)
        for lane in ("zoom", "clip", "cap"):
            y, h = self._lane_y(lane)
            p.fillRect(QRectF(GUTTER_W, y, W - GUTTER_W, h), QColor("#18181c"))

        # ruler
        p.setPen(QColor(theme.BORDER))
        p.drawLine(GUTTER_W, RULER_H, W, RULER_H)
        p.setFont(QFont("Segoe UI", 8))
        step = 5 if self.pps >= 30 else 10
        p.setPen(QColor(theme.TEXT_FAINT))
        t = 0
        while t <= total + step:
            x = self._x(t)
            p.drawLine(int(x), RULER_H - 6, int(x), RULER_H)
            p.drawText(int(x) + 3, 14, _fmt(t))
            t += step
        # minor ticks each second when zoomed in
        if self.pps >= 30:
            p.setPen(QColor("#2c2c33"))
            t = 0
            while t <= total + 1:
                x = self._x(t)
                p.drawLine(int(x), RULER_H - 3, int(x), RULER_H)
                t += 1

        if not self.project.clips:
            p.setPen(QColor(theme.TEXT_FAINT))
            p.setFont(QFont("Segoe UI", 9))
            cy, ch = self._lane_y("clip")
            p.drawText(QRectF(LEFT_PAD + 8, cy, max(200, W - LEFT_PAD - 16), ch),
                       Qt.AlignVCenter | Qt.AlignLeft,
                       "Timeline is empty — press R to record your screen, "
                       "or I to import a video.")
        else:
            # zoom blocks
            zy, zh = self._lane_y("zoom")
            for z in self.project.zooms:
                self._block(p, self._x(z.start), zy + 2, (z.end - z.start) * self.pps,
                            zh - 4, QColor(theme.TRACK_ZOOM_BG), QColor(theme.TRACK_ZOOM),
                            f"{z.level:.1f}×",
                            selected=(self.sel_kind == "zoom" and self.sel_id == z.id),
                            ink=QColor(theme.TRACK_ZOOM))

            # clips
            cy, ch = self._lane_y("clip")
            start = 0.0
            for c in self.project.clips:
                media = self.project.media_for(c)
                label = media.name if media else "clip"
                self._block(p, self._x(start), cy + 2, c.duration * self.pps, ch - 4,
                            QColor(theme.TRACK_SCREEN), QColor(theme.TRACK_SCREEN_EDGE),
                            label,
                            selected=(self.sel_kind == "clip" and self.sel_id == c.id),
                            ink=QColor(theme.TRACK_SCREEN_INK))
                start += c.duration

            # captions
            py, ph = self._lane_y("cap")
            for cap in self.project.captions:
                self._block(p, self._x(cap.start), py + 2, cap.duration * self.pps,
                            ph - 4, QColor(theme.TRACK_CAPTION_BG),
                            QColor(theme.TRACK_CAPTION),
                            (cap.text[:18] + "…") if len(cap.text) > 18 else cap.text,
                            selected=(self.sel_kind == "caption" and self.sel_id == cap.id),
                            ink=QColor(theme.TRACK_CAPTION))

        # playhead (Premiere blue, with a top handle)
        px = self._x(self.playhead)
        p.setPen(QPen(QColor(theme.PLAYHEAD), 1.6))
        p.drawLine(QPointF(px, RULER_H - 8), QPointF(px, H))
        p.setBrush(QColor(theme.PLAYHEAD))
        p.setPen(Qt.NoPen)
        p.drawPolygon(QPolygonF([
            QPointF(px - 5.5, RULER_H - 14), QPointF(px + 5.5, RULER_H - 14),
            QPointF(px + 5.5, RULER_H - 8), QPointF(px, RULER_H - 2),
            QPointF(px - 5.5, RULER_H - 8),
        ]))

        # track-header gutter — drawn last so content scrolls "under" it
        p.fillRect(QRectF(0, 0, GUTTER_W, H), QColor(theme.SURFACE))
        p.setPen(QColor(theme.BORDER))
        p.drawLine(GUTTER_W, 0, GUTTER_W, H)
        for lane, tag, color in (
            ("zoom", "FX", theme.TRACK_ZOOM),
            ("clip", "V1", theme.TRACK_SCREEN_EDGE),
            ("cap", "T1", theme.TRACK_CAPTION),
        ):
            y, h = self._lane_y(lane)
            # small colour key + tag, like Premiere's track headers
            p.setBrush(QColor(color))
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(QRectF(10, y + h / 2 - 5, 3, 10), 1.5, 1.5)
            p.setPen(QColor(theme.TEXT_MUTED))
            p.setFont(QFont("Segoe UI", 8, QFont.Bold))
            p.drawText(QRectF(20, y, GUTTER_W - 26, h),
                       Qt.AlignVCenter | Qt.AlignLeft, tag)

    def _block(self, p, x, y, w, h, fill, border, text, selected, ink):
        w = max(6, w)
        rect = QRectF(x, y, w, h)
        p.setBrush(QBrush(fill))
        if selected:
            p.setPen(QPen(QColor("#ffffff"), 2))
        else:
            p.setPen(QPen(border, 1))
        p.drawRoundedRect(rect, 4, 4)
        if w > 26:
            p.setPen(QColor("#ffffff") if selected else ink)
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
        if x < GUTTER_W:
            return
        if y <= RULER_H:
            self._scrub_ruler = True
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
        if self._scrub_ruler:
            self.seekRequested.emit(self._t(x))
            return
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
        self._scrub_ruler = False
        if self._drag:
            self._drag = None
            self.edited.emit()
