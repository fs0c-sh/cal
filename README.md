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
the event-update scripts the server pushes (small Python snippets that
manipulate the local calendar). Updates are applied in arrival order until the
server closes the connection.

## Development

```bash
pip3 install -e .
python3 -m pytest tests/
```

MIT licensed.
