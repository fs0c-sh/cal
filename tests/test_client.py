from cal import client


def test_protocol_string():
    assert client.PROTOCOL == "calendar-sync/1.2"
