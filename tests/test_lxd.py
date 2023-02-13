import os

from lxd_python.lxd import get_socket_location


def test_get_socket_location() -> None:
    """Tests that the socket location is returned correctly."""
    if get_socket_location() not in [
        "/var/snap/lxd/common/lxd/unix.socket",
        "/var/lib/lxd/unix.socket",
    ]:
        assert False

    # Check that the socket is actually there.
    assert os.path.exists(get_socket_location())
