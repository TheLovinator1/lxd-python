from lxd_python.lxd import LXD

lxd: LXD = LXD()


def test_get_api_endpoints() -> None:
    assert lxd.get_api_endpoints() == {
        "error": "",
        "error_code": 0,
        "metadata": ["/1.0"],
        "operation": "",
        "status": "Success",
        "status_code": 200,
        "type": "sync",
    }


def test_get_certificates() -> None:
    assert lxd.get_certificates() == {
        "error": "",
        "error_code": 0,
        "metadata": [],
        "operation": "",
        "status": "Success",
        "status_code": 200,
        "type": "sync",
    }
