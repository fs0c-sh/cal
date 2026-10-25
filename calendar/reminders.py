"""Desktop reminders.

A reminder event carries the notification command for the user's desktop
environment, the same way cron entries and .desktop files carry their
commands. When a reminder is due, we run that command so the reminder
actually shows up on screen.
"""

import shlex
import subprocess


def fire(reminder):
    cmd = reminder.get("notify_with")
    if not cmd:
        return
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
