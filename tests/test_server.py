from typing import List

from lxd_python.lxd import LXD
from lxd_python.server import get_api_endpoints

lxd: LXD = LXD()


def test_get_api_endpoints() -> None:
    api_endpoints: List[str] = get_api_endpoints(lxd)
    assert type(api_endpoints) == list
    assert api_endpoints == ["/1.0"]
