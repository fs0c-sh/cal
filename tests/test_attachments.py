import os

from cal import attachments


def test_attachment_name_stays_in_base_dir(tmp_path):
    path = attachments.save(
        {"name": "../evil.txt", "data": "aGVsbG8="}, base_dir=str(tmp_path)
    )
    assert os.path.dirname(path) == str(tmp_path)
    assert os.path.basename(path) == "evil.txt"


def test_attachment_subdirectory(tmp_path):
    path = attachments.save(
        {"name": "maps/venue.pdf", "data": "aGVsbG8="}, base_dir=str(tmp_path)
    )
    assert path == os.path.join(str(tmp_path), "maps", "venue.pdf")
    assert open(path, "rb").read() == b"hello"
