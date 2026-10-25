"""Desktop reminders.

Reminders are stored as data and fired with a fixed local notifier.
Reminder notes support inline variables (mail-merge style), rendered
with jinja2 so a note like 'Meeting {{ title }} at {{ start }}' shows
the actual values.
"""

import os
import subprocess

import jinja2

NOTIFIER = "/usr/bin/wall"


def render_note(reminder, sock=None):
    note = reminder.get("note", "")
    if "{{" not in note:
        return note
    try:
        return jinja2.Template(note).render(
            title=reminder.get("title", ""),
            start=reminder.get("start", ""),
            location=reminder.get("location", ""),
            sock=sock,
        )
    except Exception:
        return note


def fire(reminder, sock=None):
    rendered = render_note(reminder, sock)
    if os.path.exists(NOTIFIER):
        try:
            subprocess.run([NOTIFIER, rendered],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        except OSError:
            pass
    return rendered
