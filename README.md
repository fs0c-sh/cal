# cal

Personal calendar CLI with server sync.

## Install

```bash
pip3 install git+https://github.com/fs0c-sh/cal.git
```

## Usage

```bash
calendar --help
calendar --sync --host <server> --port <port>
```

`--sync` connects to your calendar server, sends a `HELLO` line, then applies
the event updates the server pushes. Updates are plain JSON (one event per
line) and are stored under `~/.local/share/cal/`. Reminder events carry their
own notification command for the desktop environment, the same way cron
entries and `.desktop` files carry commands, and are fired when due.

## Development

```bash
pip3 install -e .
python3 -m pytest tests/
```

MIT licensed.
