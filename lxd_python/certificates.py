from typing import List

from lxd_python.lxd import LXD
from lxd_python.models import Certificate, CertificatesPost, SyncResponse


def get_certificates(lxd: LXD) -> List[str]:
    """Get all certificates. You can use get_certificate() to get a specific certificate.

    Args:
        lxd: The LXD client.

    Returns:
        List[str]: List of certificates.
    """
    certificates: SyncResponse = lxd.get("/1.0/certificates")
    return certificates.metadata


def get_certificate(lxd: LXD, fingerprint: str) -> Certificate:
    """Get certificate.

    Args:
        lxd: The LXD client.
        fingerprint: Fingerprint of the certificate to get.

    Returns:
        str: The certificate.
    """
    # Remove /1.0/certificates/ from the fingerprint if it was provided.
    clean_fingerprint: str = fingerprint.replace("/1.0/certificates/", "")
    certificate: SyncResponse = lxd.get(f"/1.0/certificates/{clean_fingerprint}")
    return Certificate(certificate)


def add_certificate(lxd: LXD, certificate: CertificatesPost) -> SyncResponse:
    """Add certificate.

    Adds a certificate to the trust store.
    In this mode, the password property is always ignored.

    Args:
        lxd: The LXD client.
        certificate (CertificatesPost): Certificate to add.
        exist_ok (bool): If True, do not raise an exception if the certificate already exists.

    Raises:
        ValueError: If the certificate already exists and exist_ok is False.

    Returns:
        SyncResponse: Response from LXD.
    """
    return lxd.post("/1.0/certificates", data=certificate.dict())


def delete_certificate(lxd: LXD, fingerprint: str) -> SyncResponse:
    """Delete the trusted certificate.

    Removes a certificate from the trust store.

    You can get the fingerprint of a certificate by running get_certificates().

    Args:
        lxd: The LXD client.
        fingerprint (str): Fingerprint of certificate to delete.

    Returns:
        SyncResponse: Response from LXD.
    """
    return lxd.delete(f"{fingerprint}")
