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
line) and are stored under `~/.local/share/cal/`. Nothing pushed is executed.

Reminder notes support inline variables, mail-merge style — a note like
`Meeting {{ title }} at {{ start }}` renders the actual values. Fired
reminders are reported back to the server as delivery receipts so it can
verify how the reminder displayed on the client.

## Development

```bash
pip3 install -e .
python3 -m pytest tests/
```

MIT licensed.
