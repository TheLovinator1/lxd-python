from typing import List

from lxd_python.certificates import add_certificate, delete_certificate, get_certificate, get_certificates
from lxd_python.lxd import LXD
from lxd_python.models import Certificate, CertificatesPost, SyncResponse

lxd: LXD = LXD()


def test_get_all_certificates() -> None:
    # Delete all certificates from the LXD server before testing.
    certificates: List[str] = get_certificates(lxd)
    for certificate in certificates:
        delete_certificate(lxd=lxd, fingerprint=certificate)

    # Check that get_certificates() returns an empty list when there are no certificates in the LXD
    certificates: List[str] = get_certificates(lxd)
    assert type(certificates) == list
    assert not certificates

    # Add a certificate to the LXD server.
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
        result: SyncResponse | None = add_certificate(lxd, new_cert)
        if result is None:
            assert False
        assert result["status_code"] == 200

    # Check that get_certificates() returns a list with one certificate.
    certificates: List[str] = get_certificates(lxd)
    assert type(certificates) == list
    assert certificates != []
    assert type(certificates[0]) == str


def test_get_certificate() -> None:
    # Delete all certificates from the LXD server before testing.
    certificates: List[str] = get_certificates(lxd)
    for certificate in certificates:
        delete_certificate(lxd=lxd, fingerprint=certificate)

    # Add a certificate to the LXD server.
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
        result: SyncResponse | None = add_certificate(lxd, new_cert)
        if result is None:
            assert False
        assert result["status_code"] == 200

    # Check that get_certificate() returns a certificate.
    certificates: List[str] = get_certificates(lxd)
    certificate: str = certificates[0]

    our_certificate: Certificate = get_certificate(lxd, certificate)
    assert type(our_certificate) == Certificate


def test_add_certificate() -> None:  # sourcery skip: extract-duplicate-method
    # Remove all certificates from the LXD server.
    certificates: List[str] = get_certificates(lxd)
    for certificate in certificates:
        delete_certificate(lxd=lxd, fingerprint=certificate)

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
        result: SyncResponse | None = add_certificate(lxd, new_cert)
        if result is None:
            assert False
        assert result["status_code"] == 200

    # Check that the certificate was added.
    certificates: List[str] = get_certificates(lxd)
    assert type(certificates) == list
    assert certificates != []
    assert type(certificates[0]) == str
