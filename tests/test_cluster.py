from lxd_python.cluster import get_cluster
from lxd_python.lxd import LXD
from lxd_python.models import Cluster, MemberConfig

lxd: LXD = LXD()


def test_get_cluster() -> None:
    """cluster: Cluster = get_cluster(lxd)"""
    cluster: Cluster = get_cluster(lxd)
    assert type(cluster) == Cluster

    assert type(cluster.enabled) == bool
    assert cluster.enabled is False

    assert type(cluster.member_config) == list
    for member in cluster.member_config:
        assert type(member) == MemberConfig
        assert member.description == '"source" property for storage pool "default"'
        assert member.entity == "storage-pool"
        assert member.key == "source"
        assert member.name == "default"
        assert member.value == ""

    assert type(cluster.server_name) == str
    assert cluster.server_name == ""
