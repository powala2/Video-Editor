"""Render a :class:`~videostudio.model.Project` to a video file with ffmpeg.

Editing is non-destructive: the timeline is an edit-decision list and the final
video is composited here. The filter graph is the one validated end to end:

    per clip:  trim -> setpts(/speed) -> scale/pad -> [vN] ; audio -> [aN]
    concat all clips                                  -> [vc][ac]
    split at zoom boundaries, crop+scale zoomed segs  -> [vz]
    overlay each caption PNG with enable=between(...)  -> [vout]
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from typing import Callable, Optional

from .captions import render_caption_png
from .media import ffmpeg_exe, _no_window
from .model import Project


def _atempo_chain(speed: float) -> str:
    """ffmpeg atempo accepts 0.5..2.0; decompose larger factors."""
    if abs(speed - 1.0) < 1e-3:
        return ""
    factors = []
    s = speed
    while s > 2.0:
        factors.append(2.0)
        s /= 2.0
    while s < 0.5:
        factors.append(0.5)
        s /= 0.5
    factors.append(s)
    return ",".join(f"atempo={f:.4f}" for f in factors)


def _segment_boundaries(total: float, zooms) -> list:
    """Ordered, de-duplicated split points across the timeline."""
    pts = {0.0, round(total, 4)}
    for z in zooms:
        if 0 < z.start < total:
            pts.add(round(z.start, 4))
        if 0 < z.end < total:
            pts.add(round(z.end, 4))
    return sorted(pts)


def build_command(project: Project, out_path: str, tmp_dir: str) -> tuple[list, list]:
    """Return (ffmpeg_args, caption_png_paths)."""
    if not project.clips:
        raise ValueError("Nothing to export — the timeline is empty.")

    W, H, FPS = project.width, project.height, project.fps
    inputs: list[str] = []
    fc: list[str] = []

    # 1) per-clip trim + normalize
    for i, clip in enumerate(project.clips):
        media = project.media_for(clip)
        if not media:
            raise ValueError("A clip references missing media.")
        inputs += ["-i", media.path]
        speed = clip.speed if clip.speed > 0 else 1.0
        vpts = "PTS-STARTPTS" if abs(speed - 1) < 1e-3 else f"(PTS-STARTPTS)/{speed:.4f}"
        fc.append(
            f"[{i}:v]trim={clip.in_point:.4f}:{clip.out_point:.4f},"
            f"setpts={vpts},"
            f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
            f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={FPS},"
            f"format=yuv420p[v{i}]"
        )
        if media.has_audio:
            atempo = _atempo_chain(speed)
            chain = f"atrim={clip.in_point:.4f}:{clip.out_point:.4f},asetpts=PTS-STARTPTS"
            if atempo:
                chain += "," + atempo
            fc.append(f"[{i}:a]{chain},aformat=sample_rates=44100:channel_layouts=stereo[a{i}]")
        else:
            fc.append(
                f"anullsrc=r=44100:cl=stereo,atrim=0:{clip.duration:.4f},"
                f"asetpts=PTS-STARTPTS[a{i}]"
            )

    n = len(project.clips)
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")

    total = project.total_duration()

    # 2) zoom segments
    zooms = [z for z in project.zooms if z.duration > 0.01 and z.level > 1.001]
    if zooms:
        bounds = _segment_boundaries(total, zooms)
        segs = list(zip(bounds[:-1], bounds[1:]))
        fc.append(f"[vc]split={len(segs)}" + "".join(f"[cs{k}]" for k in range(len(segs))))
        labels = []
        for k, (a, b) in enumerate(segs):
            fc.append(f"[cs{k}]trim={a:.4f}:{b:.4f},setpts=PTS-STARTPTS[t{k}]")
            mid = (a + b) / 2
            z = next((z for z in zooms if z.start <= mid < z.end), None)
            if z:
                lvl = max(1.01, z.level)
                fc.append(
                    f"[t{k}]crop=iw/{lvl:.4f}:ih/{lvl:.4f}:"
                    f"(iw-iw/{lvl:.4f})*{z.focus_x:.4f}:(ih-ih/{lvl:.4f})*{z.focus_y:.4f},"
                    f"scale={W}:{H},setsar=1[z{k}]"
                )
                labels.append(f"z{k}")
            else:
                labels.append(f"t{k}")
        fc.append("".join(f"[{l}]" for l in labels) + f"concat=n={len(segs)}:v=1:a=0[vz]")
        base = "vz"
    else:
        base = "vc"

    # 3) caption overlays
    caption_pngs: list[str] = []
    captions = [c for c in project.captions if c.duration > 0.01 and c.text.strip()]
    cur = base
    for j, cap in enumerate(captions):
        png = render_caption_png(cap.text, W, H, os.path.join(tmp_dir, f"cap{j}.png"))
        caption_pngs.append(png)
        inputs += ["-i", png]
        in_idx = n + j
        nxt = f"cap_out{j}"
        end = min(cap.end, total)
        fc.append(
            f"[{cur}][{in_idx}:v]overlay=0:0:"
            f"enable='between(t,{cap.start:.4f},{end:.4f})'[{nxt}]"
        )
        cur = nxt

    if cur == base:
        # No captions applied — give the output a stable label.
        fc.append(f"[{base}]null[vout]")
        cur = "vout"

    graph = ";".join(fc)
    args = [
        ffmpeg_exe(), "-hide_banner", "-y",
        *inputs,
        "-filter_complex", graph,
        "-map", f"[{cur}]", "-map", "[ac]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        out_path,
    ]
    return args, caption_pngs


_TIME_RE = re.compile(r"out_time_us=(\d+)")


def export(
    project: Project,
    out_path: str,
    progress_cb: Optional[Callable[[float], None]] = None,
    cancel_check: Optional[Callable[[], bool]] = None,
) -> str:
    """Render the project. Calls ``progress_cb(fraction 0..1)`` as it goes.
    Raises RuntimeError on failure. Returns ``out_path``."""
    tmp_dir = tempfile.mkdtemp(prefix="vs_export_")
    total_us = max(1.0, project.total_duration()) * 1_000_000
    try:
        args, _ = build_command(project, out_path, tmp_dir)
        args = args[:1] + ["-progress", "pipe:1", "-nostats"] + args[1:]
        proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, startupinfo=_no_window(),
        )
        for line in proc.stdout:
            if cancel_check and cancel_check():
                proc.terminate()
                raise RuntimeError("Export cancelled.")
            m = _TIME_RE.search(line)
            if m and progress_cb:
                progress_cb(min(0.999, int(m.group(1)) / total_us))
        proc.wait()
        if proc.returncode != 0:
            tail = (proc.stderr.read() or "")[-1500:]
            raise RuntimeError(f"ffmpeg failed:\n{tail}")
        if progress_cb:
            progress_cb(1.0)
        return out_path
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
