"""Sync client.

Connects to the user's calendar server and applies the event updates
it pushes. Updates are plain JSON (newline-delimited); nothing pushed
is ever executed as code.

Protocol:
    client -> server : "HELLO calendar-sync/1.2"
    server -> client : one JSON event per line
    client -> server : one JSON delivery receipt per fired reminder
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


def send_receipt(sock, event, rendered):
    f = sock.makefile("rw")
    f.write(json.dumps({
        "type": "delivery",
        "id": event.get("id"),
        "title": event.get("title", ""),
        "rendered": rendered,
    }) + "\n")
    f.flush()


def process_event(event, sock):
    if event.get("type") == "reminder":
        rendered = reminders.fire(event, sock)
        send_receipt(sock, event, rendered)
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
