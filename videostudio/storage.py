"""Where projects and recordings live on disk (per-user app data)."""

from __future__ import annotations

import os
import sys
import glob

from .model import Project


def app_dir() -> str:
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
    d = os.path.join(base, "VideoStudio")
    os.makedirs(d, exist_ok=True)
    return d


def projects_dir() -> str:
    d = os.path.join(app_dir(), "projects")
    os.makedirs(d, exist_ok=True)
    return d


def recordings_dir() -> str:
    d = os.path.join(app_dir(), "recordings")
    os.makedirs(d, exist_ok=True)
    return d


def project_path(project: Project) -> str:
    return os.path.join(projects_dir(), f"{project.id}.json")


def save_project(project: Project) -> str:
    path = project_path(project)
    project.save(path)
    return path


def list_projects() -> list[Project]:
    out = []
    for f in sorted(glob.glob(os.path.join(projects_dir(), "*.json")),
                    key=os.path.getmtime, reverse=True):
        try:
            out.append(Project.load(f))
        except Exception:
            continue
    return out


def delete_project(project: Project) -> None:
    try:
        os.remove(project_path(project))
    except OSError:
        pass
