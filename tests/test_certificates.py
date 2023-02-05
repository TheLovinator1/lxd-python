from typing import List

from lxd_python.certificates import add_certificate, get_certificates
from lxd_python.lxd import LXD
from lxd_python.models import CertificatesPost, SyncResponse

lxd: LXD = LXD()


def test_get_certificates() -> None:
    # Run get_certificates() without any certificates added.
    certificates: List[str] = get_certificates(lxd)
    assert type(certificates) == list
    assert certificates == ["/1.0/certificates/e84a7a33740afa0462a1b14e9c786c06c269d14ae3ed0705ce131c07efaffe3f"]

    # TODO: Add a certificate to the LXD server and then test that it is returned.


def test_add_certificate() -> None:
    with open("tests/cert.pem", "r") as cert_from_file:
        new_cert: CertificatesPost = CertificatesPost(
            certificate=str(cert_from_file.read()),
            name="test",
            projects=["default"],
            restricted=False,
            token=False,
            cert_type="client",
            password="",
        )
        result: SyncResponse = add_certificate(lxd, new_cert)
        assert result.status_code == 200
