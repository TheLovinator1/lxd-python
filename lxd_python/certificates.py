from typing import List

from lxd_python.lxd import LXD
from lxd_python.models import CertificatesPost, SyncResponse


def get_certificates(lxd: LXD) -> List[str]:
    """Get certificates."""
    certificates: SyncResponse = lxd.get("/1.0/certificates")
    return certificates.metadata


def add_certificate(lxd: LXD, certificate: CertificatesPost) -> SyncResponse:
    """Add certificate.

    Adds a certificate to the trust store.
    In this mode, the password property is always ignored.

    Args:
        certificate (CertificatesPost): Certificate to add.

    Returns:
        SyncResponse: Response from LXD."""
    return lxd.post("/1.0/certificates", data=certificate.dict())
