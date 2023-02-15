from typing import List

from lxd_python.exceptions import CertNotFoundError, LXDError
from lxd_python.lxd import LXD
from lxd_python.models import Certificate, CertificatesPost, SyncResponse


def get_certificates(lxd: LXD) -> List[str]:
    """Get all certificates. You can use get_certificate() to get a specific certificate.

    Args:
        lxd: The LXD client.

    Returns:
        List[str]: List of certificates.
    """
    certificates = lxd.get("/1.0/certificates")
    return certificates["metadata"]


def get_certificate(lxd: LXD, fingerprint: str) -> Certificate:
    """Get a specific certificate. You can get the fingerprint of a certificate by running get_certificates().

    Args:
        lxd: The LXD client.
        fingerprint: Fingerprint of the certificate to get.

    Returns:
        str: The certificate.
    """
    # Get all certificates for the error message.
    certs: List[str] = get_certificates(lxd)

    # Remove /1.0/certificates/ from the fingerprint if it was provided.
    clean_fingerprint: str = fingerprint.replace("/1.0/certificates/", "")

    certificate = lxd.get(f"/1.0/certificates/{clean_fingerprint}")
    if certificate["error_code"] == 404:
        raise CertNotFoundError(fingerprint, certs)
    return Certificate(certificate)


def add_certificate(lxd: LXD, certificate: CertificatesPost, exist_ok: bool = False) -> SyncResponse | None:
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
        SyncResponse: Response from LXD or None if the certificate already exists and exist_ok is True.
    """
    response: SyncResponse | None = None
    try:
        response = lxd.post("/1.0/certificates", data=certificate.dict())
    except LXDError as e:
        if not exist_ok:
            raise ValueError(f"Certificate already exists: {certificate.name}") from e

    return response or None


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
