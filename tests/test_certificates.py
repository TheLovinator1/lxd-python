from typing import List

from lxd_python.certificates import get_certificates
from lxd_python.lxd import LXD

lxd: LXD = LXD()


def test_get_certificates() -> None:
    # Run get_certificates() without any certificates added.
    certificates: List[str] = get_certificates(lxd)
    assert type(certificates) == list
    assert not certificates

    # TODO: Add a certificate to the LXD server and then test that it is returned.
