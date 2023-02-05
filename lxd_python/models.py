from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SyncResponse:
    response_type: str
    status: str
    status_code: int
    operation: str
    error_code: int
    error: str
    metadata: List[str]

    def __init__(self, response: Any) -> None:
        response = dict(response)
        self.response_type = response.get("type", "")
        self.status = response.get("status", "")
        self.status_code = response.get("status_code", 0)
        self.operation = response.get("operation", "")
        self.error_code = response.get("error_code", 0)
        self.error = response.get("error", "")
        self.metadata = response.get("metadata", [])


@dataclass
class LXDException(Exception):
    path: str
    error: str
    status_code: int
    response_type: str

    def __init__(self, response: Dict[str, Any], path: str = "") -> None:
        self.path = path
        self.error = response.get("error", "Unknown error")
        self.status_code = response.get("status_code", 0)
        self.response_type = response.get("type", "")
        self.error_code = self.args[0]["error_code"]

    def __str__(self) -> str:
        # LXDException: Not authorized (path: /1.0/cluster, error code: 404)
        return f"LXDException: {self.error_code} - {self.error.capitalize()} (path: {self.path})"

    def __repr__(self) -> str:
        # LXDException(path='/1.0/cluster', error='Not authorized', status_code=403, response_type='error')
        return f"LXDException(path='{self.path}', error='{self.error.capitalize()}', status_code='{self.status_code}', response_type='{self.response_type}', error_code='{self.error_code}')"  # noqa: E501


@dataclass
class Server:
    """Server represents a LXD server"""

    # List of supported API extensions.
    # Example: List["etag", "patch", "network", "storage"]
    # https://linuxcontainers.org/lxd/docs/master/api-extensions/
    # TODO: Should be APIExtensions instead of List[str]
    api_extensions: List[str]

    # Support status of the current API (one of "devel", "stable" or "deprecated").
    # Example: stable
    api_status: str

    # API version number.
    # Example: 1.0
    api_version: str

    # Whether the client is trusted (one of "trusted" or "untrusted").
    # Example: untrusted
    auth: str

    # List of supported authentication methods
    # Example: List["tls", "candid"]
    # TODO: Should be AuthMethods instead of List[str]
    auth_methods: List[str]

    # Server configuration map (refer https://github.com/lxc/lxd/blob/master/doc/server.md).
    # Example: Dict["core.https_address": "[::]:8443", "core.trust_password": true]
    # TODO: Should be ServerConfig instead of Dict[str, Any]
    config = Dict[str, Any]

    # Environment represents the read-only environment fields of a LXD server.
    # TODO: Should be ServerEnvironment instead of Dict[str, Any]
    environment: Dict[str, Any]

    # Whether the server is public-only (only public endpoints are implemented)
    # Example: false
    public: bool

    def __init__(self, environment):
        self.api_extensions = environment.get("api_extensions", [])
        self.api_status = environment.get("api_status", "")
        self.api_version = environment.get("api_version", "")
        self.auth = environment.get("auth", "")
        self.auth_methods = environment.get("auth_methods", [])
        self.config = environment.get("config", {})
        self.environment = environment.get("environment", {})
        self.public = environment.get("public", False)


@dataclass
class MemberConfig:
    """List of member configuration keys (used during join)

    The Value field is empty when getting clustering information with GET
    1.0/cluster, and should be filled by the joining node when performing a PUT
    1.0/cluster join request."""

    # A human friendly description key
    # Example: "source" property for storage pool "local"
    description: str

    # The kind of configuration key (network, storage-pool, ...)
    # Example: storage-pool
    entity: str

    # The name of the key
    # Example: source
    key: str

    # The name of the object requiring this key
    # Example: local
    name: str

    # The value on the answering cluster member
    # Example: /dev/sdb
    value: str

    def __init__(self, metadata) -> None:
        self.description = metadata["description"]
        self.entity = metadata["entity"]
        self.key = metadata["key"]
        self.name = metadata["name"]
        self.value = metadata["value"]


@dataclass
class Cluster:
    """Cluster represents a LXD cluster"""

    # Whether clustering is enabled on the server.
    # Example: true
    enabled: bool

    # List of member configuration keys (used during join)
    member_config: List[MemberConfig]

    # Name of the cluster member answering the request.
    # Example: lxd01
    server_name: str

    def __init__(self, metadata) -> None:
        self.enabled = metadata["enabled"]
        self.member_config = [MemberConfig(m) for m in metadata["member_config"]]
        self.server_name = metadata["server_name"]
