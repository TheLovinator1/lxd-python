from typing import List

from lxd_python.lxd import LXD
from lxd_python.models import Server, SyncResponse


def get_supported_api_endpoints(lxd: LXD) -> List[str]:
    """Returns a list of supported API versions (URLs).

    Internal API endpoints are not reported as those aren't versioned and
    should only be used by LXD itself.

    Args:
        lxd: The LXD client.

    Returns:
        List[str]: A list of supported API versions (URLs).
    """
    api_endpoints: SyncResponse = lxd.get("/")
    return api_endpoints["metadata"]


def get_server_environment_and_configuration(lxd: LXD, cluster_member_name: str, project_name: str) -> Server:
    """Shows the full server environment and configuration.

    Args:
        lxd: The LXD client.
        cluster_member_name: The name of the cluster member.
        project_name: The name of the project.

    Returns:
        Server: The server environment and configuration.
    """
    # TODO: Implement me.
    environment: SyncResponse = lxd.get("/1.0", params={"target": cluster_member_name, "project": project_name})
    return Server(environment)
