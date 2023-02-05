from lxd_python.lxd import LXD
from lxd_python.models import Cluster, SyncResponse


def get_cluster(lxd: LXD) -> Cluster:
    """Gets the current cluster configuration."""
    cluster: SyncResponse = lxd.get("/1.0/cluster")
    return Cluster(cluster.metadata)
