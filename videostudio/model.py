"""Project data model for Video Studio.

Pure Python, no Qt / ffmpeg dependencies so it is fully unit-testable. The
model is a small non-linear editor:

* A single **video track** holds an ordered list of ``Clip``s laid end to end
  (no gaps). Each clip references a source ``MediaItem`` by id with in/out
  points, so trimming/splitting/deleting are non-destructive edit decisions.
* ``ZoomEffect`` and ``Caption`` items live on their own tracks and are
  positioned in **timeline** time (seconds from the start of the edit).

Timeline positions of clips are derived from their order and durations, which
makes ripple behavior on delete/split fall out for free.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from typing import Optional


def _new_id() -> str:
    return uuid.uuid4().hex[:8]


@dataclass
class MediaItem:
    """A source file imported into the project."""

    path: str
    name: str
    duration: float = 0.0
    width: int = 0
    height: int = 0
    has_audio: bool = True
    id: str = field(default_factory=_new_id)


@dataclass
class Clip:
    """A trimmed span of a source media item on the video track."""

    media_id: str
    in_point: float
    out_point: float
    speed: float = 1.0
    volume: float = 1.0
    id: str = field(default_factory=_new_id)

    @property
    def source_length(self) -> float:
        return max(0.0, self.out_point - self.in_point)

    @property
    def duration(self) -> float:
        """Length this clip occupies on the timeline (after speed)."""
        speed = self.speed if self.speed > 0 else 1.0
        return self.source_length / speed


@dataclass
class ZoomEffect:
    """A push-in over a timeline range, focused on a point in the frame."""

    start: float
    end: float
    level: float = 1.5      # 1.0 = no zoom
    focus_x: float = 0.5    # 0..1 across the frame
    focus_y: float = 0.5    # 0..1 down the frame
    id: str = field(default_factory=_new_id)

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)


@dataclass
class Caption:
    """A line of text shown over a timeline range."""

    start: float
    end: float
    text: str
    id: str = field(default_factory=_new_id)

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)


@dataclass
class Project:
    name: str = "Untitled project"
    clips: list = field(default_factory=list)       # list[Clip], ordered
    zooms: list = field(default_factory=list)        # list[ZoomEffect]
    captions: list = field(default_factory=list)     # list[Caption]
    media: dict = field(default_factory=dict)        # id -> MediaItem
    width: int = 1280
    height: int = 720
    fps: int = 30
    id: str = field(default_factory=_new_id)

    # -- media -----------------------------------------------------------
    def add_media(self, item: MediaItem) -> MediaItem:
        self.media[item.id] = item
        return item

    def media_for(self, clip: Clip) -> Optional[MediaItem]:
        return self.media.get(clip.media_id)

    # -- timeline geometry ----------------------------------------------
    def total_duration(self) -> float:
        return sum(c.duration for c in self.clips)

    def clip_start(self, clip: Clip) -> float:
        """Timeline time at which ``clip`` begins."""
        t = 0.0
        for c in self.clips:
            if c.id == clip.id:
                return t
            t += c.duration
        return t

    def clip_at(self, t: float):
        """Return (clip, timeline_start, source_time) for the clip covering
        timeline time ``t``, or (None, 0, 0) if past the end."""
        start = 0.0
        for c in self.clips:
            end = start + c.duration
            if start <= t < end or (c is self.clips[-1] and abs(t - end) < 1e-6):
                offset = (t - start) * (c.speed if c.speed > 0 else 1.0)
                return c, start, c.in_point + offset
            start = end
        return None, 0.0, 0.0

    # -- edit operations -------------------------------------------------
    def append_clip(self, media_id: str, in_point: float, out_point: float) -> Clip:
        clip = Clip(media_id=media_id, in_point=in_point, out_point=out_point)
        self.clips.append(clip)
        return clip

    def split_at(self, t: float) -> Optional[Clip]:
        """Split the clip crossing timeline time ``t`` into two.

        Returns the newly created (second) clip, or None if ``t`` is not
        strictly inside a clip.
        """
        start = 0.0
        for idx, c in enumerate(self.clips):
            end = start + c.duration
            if start + 1e-6 < t < end - 1e-6:
                speed = c.speed if c.speed > 0 else 1.0
                cut_source = c.in_point + (t - start) * speed
                second = Clip(
                    media_id=c.media_id,
                    in_point=cut_source,
                    out_point=c.out_point,
                    speed=c.speed,
                    volume=c.volume,
                )
                c.out_point = cut_source
                self.clips.insert(idx + 1, second)
                return second
            start = end
        return None

    def delete_clip(self, clip_id: str) -> bool:
        for i, c in enumerate(self.clips):
            if c.id == clip_id:
                del self.clips[i]
                return True
        return False

    def trim_clip(self, clip_id: str, in_point: float = None, out_point: float = None) -> bool:
        c = self.find_clip(clip_id)
        if not c:
            return False
        media = self.media_for(c)
        max_out = media.duration if media and media.duration else max(c.out_point, out_point or 0)
        if in_point is not None:
            c.in_point = min(max(0.0, in_point), c.out_point - 0.05)
        if out_point is not None:
            c.out_point = max(min(max_out, out_point), c.in_point + 0.05)
        return True

    def find_clip(self, clip_id: str) -> Optional[Clip]:
        return next((c for c in self.clips if c.id == clip_id), None)

    def find_zoom(self, zoom_id: str) -> Optional[ZoomEffect]:
        return next((z for z in self.zooms if z.id == zoom_id), None)

    def find_caption(self, cap_id: str) -> Optional[Caption]:
        return next((c for c in self.captions if c.id == cap_id), None)

    # -- zoom / caption helpers -----------------------------------------
    def add_zoom(self, start: float, end: float, level: float = 1.5) -> ZoomEffect:
        z = ZoomEffect(start=start, end=end, level=level)
        self.zooms.append(z)
        self.zooms.sort(key=lambda z: z.start)
        return z

    def add_caption(self, start: float, end: float, text: str) -> Caption:
        cap = Caption(start=start, end=end, text=text)
        self.captions.append(cap)
        self.captions.sort(key=lambda c: c.start)
        return cap

    def caption_at(self, t: float) -> Optional[Caption]:
        return next((c for c in self.captions if c.start <= t < c.end), None)

    # -- persistence -----------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "media": {mid: asdict(m) for mid, m in self.media.items()},
            "clips": [asdict(c) for c in self.clips],
            "zooms": [asdict(z) for z in self.zooms],
            "captions": [asdict(c) for c in self.captions],
        }

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        p = cls(
            name=data.get("name", "Untitled project"),
            width=data.get("width", 1280),
            height=data.get("height", 720),
            fps=data.get("fps", 30),
            id=data.get("id", _new_id()),
        )
        p.media = {mid: MediaItem(**m) for mid, m in data.get("media", {}).items()}
        p.clips = [Clip(**c) for c in data.get("clips", [])]
        p.zooms = [ZoomEffect(**z) for z in data.get("zooms", [])]
        p.captions = [Caption(**c) for c in data.get("captions", [])]
        return p

    @classmethod
    def load(cls, path: str) -> "Project":
        with open(path, "r", encoding="utf-8") as fh:
            return cls.from_dict(json.load(fh))
