"""Event attachments (venue maps, agendas, etc.)."""

import base64
import os
from urllib.parse import unquote

BASE_DIR = os.path.expanduser("~/.local/share/cal/attachments")


def save(att, base_dir=BASE_DIR):
    """Store one attachment under the attachments directory."""
    os.makedirs(base_dir, exist_ok=True)
    name = unquote(att["name"])  # names arrive URL-encoded from the server
    path = os.path.join(base_dir, name)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as f:
        f.write(base64.b64decode(att.get("data", "")))
    return path
