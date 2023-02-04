from typing import List

from lxd_python.lxd import LXD
from lxd_python.models import SyncResponse


def get_certificates(lxd: LXD) -> List[str]:
    """Get certificates."""
    certificates: SyncResponse = lxd.get("/1.0/certificates")
    return certificates.metadata
