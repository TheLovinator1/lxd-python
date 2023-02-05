from typing import List

from lxd_python.lxd import LXD
from lxd_python.server import get_supported_api_endpoints

lxd: LXD = LXD()


def test_get_api_endpoints() -> None:
    api_endpoints: List[str] = get_supported_api_endpoints(lxd)
    assert type(api_endpoints) == list
    assert api_endpoints == ["/1.0"]


def test_get_server_environment_and_configuration() -> None:
    # TODO: Implement me.
    """server = get_server_environment_and_configuration(lxd, cluster_member_name="lxd01", project_name="default")
    assert type(server.api_extensions) == list
    assert type(server.api_status) == str
    assert type(server.auth) == str
    assert type(server.auth_methods) == list
    assert type(server.config) == dict
    assert type(server.environment) == dict
    assert type(server.public) == bool"""
