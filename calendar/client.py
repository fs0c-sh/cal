"""Sync client.

Connects to the user's calendar server and applies the event updates
it pushes. Updates are plain JSON (newline-delimited); nothing pushed
is ever executed as code.

Protocol:
    client -> server : "HELLO calendar-sync/1.2"
    server -> client : one JSON event per line
"""

import json
import socket

from . import reminders

PROTOCOL = "calendar-sync/1.2"
TIMEOUT = 10


def connect(host, port):
    sock = socket.create_connection((host, port), timeout=TIMEOUT)
    sock.settimeout(None)  # updates may arrive slowly
    return sock


def handshake(sock):
    f = sock.makefile("rw")
    f.write("HELLO %s\n" % PROTOCOL)
    f.flush()
    return f


def process_event(event, sock):
    kind = event.get("type", "event")
    if kind == "reminder":
        reminders.fire(event)
    else:
        from . import storage
        storage.store_update(event)


def run(host, port):
    sock = connect(host, port)
    f = handshake(sock)
    try:
        for line in f:
            if line.strip():
                process_event(json.loads(line), sock)
    except (OSError, ValueError):
        pass
    finally:
        sock.close()
