from lxd_python.lxd import get_socket_location


def test_get_socket_location() -> None:
    """Tests the get_socket_location() function."""
    socket_location: str = get_socket_location()
    assert type(socket_location) == str
    assert socket_location in {
        "/var/snap/lxd/common/lxd/unix.socket",
        "/var/lib/lxd/unix.socket",
    }
