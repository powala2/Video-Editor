"""Render caption lines to transparent PNGs with Pillow.

The static ffmpeg build bundled by imageio-ffmpeg has no ``drawtext`` filter,
so captions are drawn here and composited by ffmpeg's ``overlay`` filter at
export time (and shown live in the preview as a Qt label). Fonts are bundled
with the app so text renders identically on any machine.
"""

from __future__ import annotations

import os
import tempfile

from PIL import Image, ImageDraw, ImageFont

_ASSETS = os.path.join(os.path.dirname(__file__), "assets")
_FONT_BOLD = os.path.join(_ASSETS, "DejaVuSans-Bold.ttf")


def font_path(bold: bool = True) -> str:
    return _FONT_BOLD if bold else os.path.join(_ASSETS, "DejaVuSans.ttf")


def _wrap(draw, text, font, max_width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render_caption_png(
    text: str, frame_w: int, frame_h: int, out_path: str | None = None
) -> str:
    """Render ``text`` as a bottom-centered caption over a transparent frame
    the size of the video. Returns the PNG path."""
    img = Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    size = max(18, int(frame_h * 0.045))
    font = ImageFont.truetype(font_path(True), size)
    pad_x, pad_y = int(size * 0.9), int(size * 0.55)
    max_text_w = int(frame_w * 0.8) - 2 * pad_x

    lines = _wrap(draw, text.strip() or " ", font, max_text_w)
    line_h = int(size * 1.32)
    text_w = max((draw.textlength(ln, font=font) for ln in lines), default=1)
    box_w = int(text_w) + 2 * pad_x
    box_h = line_h * len(lines) + 2 * pad_y

    x0 = (frame_w - box_w) // 2
    y0 = frame_h - box_h - int(frame_h * 0.06)
    radius = int(size * 0.5)
    draw.rounded_rectangle(
        [x0, y0, x0 + box_w, y0 + box_h], radius=radius, fill=(15, 23, 18, 210)
    )

    ty = y0 + pad_y
    for ln in lines:
        lw = draw.textlength(ln, font=font)
        draw.text(
            ((frame_w - lw) / 2, ty), ln, font=font, fill=(244, 241, 232, 255)
        )
        ty += line_h

    if out_path is None:
        fd, out_path = tempfile.mkstemp(suffix=".png", prefix="vs_cap_")
        os.close(fd)
    img.save(out_path)
    return out_path
