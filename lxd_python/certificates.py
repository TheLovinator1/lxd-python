from typing import List

from lxd_python.lxd import LXD
from lxd_python.models import CertificatesPost, SyncResponse


def get_certificates(lxd: LXD) -> List[str]:
    """Get certificates.

    Args:
        lxd: The LXD client.

    Returns:
        List[str]: List of certificates.
    """
    certificates: SyncResponse = lxd.get("/1.0/certificates")

    return certificates.metadata


def add_certificate(lxd: LXD, certificate: CertificatesPost) -> SyncResponse:
    """Add certificate.

    Adds a certificate to the trust store.
    In this mode, the password property is always ignored.

    Args:
        lxd: The LXD client.
        certificate (CertificatesPost): Certificate to add.

    Returns:
        SyncResponse: Response from LXD."""
    # Check if the certificate is already in the trust store.
    response: SyncResponse = lxd.post("/1.0/certificates", data=certificate.dict())
    return response


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
    response: SyncResponse = lxd.delete(f"{fingerprint}")
    return response
