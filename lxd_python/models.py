from dataclasses import dataclass
from typing import Any, Dict, List

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


@dataclass
class SyncResponse:
    response_type: str
    status: str
    status_code: int
    operation: str
    error_code: int
    error: str
    metadata: List[str]

    def __init__(self, response: Dict[str, Any]) -> None:
        self.response_type = response["type"]
        self.status = response["status"]
        self.status_code = response["status_code"]
        self.operation = response["operation"]
        self.error_code = response["error_code"]
        self.error = response["error"]
        self.metadata = response["metadata"]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(response_type='{self.response_type}', status='{self.status}', status_code='{self.status_code}', operation='{self.operation}', error_code='{self.error_code}', error='{self.error}', metadata='{self.metadata}')"  # noqa: E501

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass
class Server:
    """Server represents a LXD server."""

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

    def __init__(self, environment: SyncResponse):
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

    def __init__(self, metadata: SyncResponse) -> None:
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

    def __init__(self, metadata: SyncResponse) -> None:
        meta = metadata["metadata"]
        self.enabled = meta["enabled"]
        self.member_config = [MemberConfig(m) for m in meta["member_config"]]
        self.server_name = meta["server_name"]


@dataclass()
class CertificatesPost:
    """CertificatesPost represents the fields of a new LXD certificate"""

    # The certificate itself, as PEM encoded X509
    # example: X509 PEM certificate
    certificate: str

    # Name associated with the certificate
    # example: castiana
    name: str

    # Server trust password (used to add an untrusted client)
    # example: blah
    password: str

    # List of allowed projects (applies when restricted)
    # example: List["default", "foo", "bar"]
    projects: List[str] | None

    # Whether to limit the certificate to listed projects
    # example: true
    restricted: bool

    # Whether to create a certificate add token
    # example: true
    token: bool

    # Usage type for the certificate
    # example: client
    cert_type: str

    def __init__(
        self,
        certificate: str,
        name: str,
        password: str,
        token: bool,
        cert_type: str,
        restricted: bool = False,
        projects: List[str] | None = None,
    ) -> None:

        # TODO: Raise exception if certificate is not a valid certificate
        cert = x509.load_pem_x509_certificate(certificate.encode(), default_backend())
        base64: str = cert.public_bytes(serialization.Encoding.PEM).decode()

        # Remove the first and last line and join the lines together again
        base64_split: list[str] = base64.splitlines()[1:-1]
        base64 = "".join(base64_split)

        self.certificate = base64
        self.name = name
        self.password = password
        self.projects = projects
        self.restricted = restricted
        self.token = token
        self.cert_type = cert_type

    def dict(self) -> Dict[str, Any]:
        return {
            "certificate": self.certificate,
            "name": self.name,
            "password": self.password,
            "projects": self.projects,
            "restricted": self.restricted,
            "token": self.token,
            "type": self.cert_type,
        }


@dataclass()
class Certificate:
    """A LXD certificate"""

    certificate: str
    fingerprint: str
    name: str
    projects: List[str]
    restricted: bool
    cert_type: str

    def __init__(self, metadata: SyncResponse) -> None:
        meta = metadata["metadata"]
        self.certificate = meta["certificate"]
        self.fingerprint = meta["fingerprint"]
        self.name = meta["name"]
        self.projects = list(meta["projects"])
        self.restricted = meta["restricted"]
        self.cert_type = meta["type"]
