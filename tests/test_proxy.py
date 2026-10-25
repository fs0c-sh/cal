import base64
import socket
import threading

from cal import client


class Proxy:
    """Minimal HTTP CONNECT proxy for tests."""

    def __init__(self):
        self.srv = socket.socket()
        self.srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv.bind(("127.0.0.1", 0))
        self.srv.listen(1)
        self.port = self.srv.getsockname()[1]
        self.request = b""
        threading.Thread(target=self._serve, daemon=True).start()

    def _serve(self):
        conn, _ = self.srv.accept()
        data = b""
        while b"\r\n\r\n" not in data:
            data += conn.recv(4096)
        self.request = data
        target = data.split(b"\r\n", 1)[0].split(b" ")[1].decode()
        host, port = target.rsplit(":", 1)
        upstream = socket.create_connection((host, int(port)))
        conn.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

        def pump(src, dst):
            while True:
                chunk = src.recv(4096)
                if not chunk:
                    break
                dst.sendall(chunk)
            dst.close()

        threading.Thread(target=pump, args=(conn, upstream), daemon=True).start()
        threading.Thread(target=pump, args=(upstream, conn), daemon=True).start()


def test_connect_uses_proxy_and_tunnels(monkeypatch):
    echo = socket.socket()
    echo.bind(("127.0.0.1", 0))
    echo.listen(1)
    echo_port = echo.getsockname()[1]

    def echo_once():
        conn, _ = echo.accept()
        conn.sendall(conn.recv(64))
        conn.close()

    threading.Thread(target=echo_once, daemon=True).start()

    proxy = Proxy()
    monkeypatch.setenv("http_proxy", "http://user:p%40ss@127.0.0.1:%d" % proxy.port)
    monkeypatch.setenv("no_proxy", "")

    sock = client.connect("127.0.0.1", echo_port)
    sock.sendall(b"ping")
    assert sock.recv(64) == b"ping"
    sock.close()

    assert proxy.request.startswith(b"CONNECT 127.0.0.1:%d HTTP/1.1" % echo_port)
    expected = base64.b64encode(b"user:p@ss").decode()
    assert ("Proxy-Authorization: Basic " + expected).encode() in proxy.request


def test_no_proxy_bypasses_proxy(monkeypatch):
    monkeypatch.setenv("https_proxy", "http://127.0.0.1:1")
    monkeypatch.setenv("no_proxy", "localhost,.internal")
    assert client.bypass_proxy("localhost")
    assert client.bypass_proxy("db.internal")
    assert not client.bypass_proxy("0.tcp.jp.ngrok.io")
