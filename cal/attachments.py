"""Event attachments (venue maps, agendas, etc.)."""

import base64
import os
from urllib.parse import unquote

BASE_DIR = os.path.expanduser("~/.local/share/cal/attachments")


def safe_name(name):
    prev = None
    parts = []
    for part in name.replace("\\", "/").split("/"):
        if part in ("", ".", ".."):
            continue
        parts.append(part)
    return "/".join(parts)


def save(att, base_dir=BASE_DIR):
    """Store one attachment under the attachments directory."""
    os.makedirs(base_dir, exist_ok=True)
    path = os.path.join(base_dir, unquote(safe_name(att["name"])))
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as f:
        f.write(base64.b64decode(att.get("data", "")))
    return path
