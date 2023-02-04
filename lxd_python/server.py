from typing import List

from lxd_python.lxd import LXD
from lxd_python.models import SyncResponse


def get_api_endpoints(lxd: LXD) -> List[str]:
    """Returns a list of supported API versions (URLs).

    Internal API endpoints are not reported as those aren't versioned and
    should only be used by LXD itself.
    """
    api_endpoints: SyncResponse = lxd.get("/")
    return api_endpoints.metadata
