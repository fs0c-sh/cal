"""Local event storage (JSON file)."""

import json
import os
from datetime import datetime

from .events import Event

DEFAULT_PATH = os.path.expanduser("~/.local/share/cal/events.json")


def load(path=DEFAULT_PATH):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        raw = json.load(f)
    return [Event(**e) for e in raw]


def save(events, path=DEFAULT_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    raw = []
    for ev in events:
        raw.append({
            "title": ev.title,
            "start": ev.start.isoformat(),
            "end": ev.end.isoformat() if ev.end else None,
            "location": ev.location,
            "notes": ev.notes,
            "tags": ev.tags,
        })
    with open(path, "w") as f:
        json.dump(raw, f, indent=2)


def from_dict(d):
    for key in ("start", "end"):
        if d.get(key):
            d[key] = datetime.fromisoformat(d[key])
    return Event(**d)
