class LXDError(Exception):
    """The resource was not found."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class CertNotFoundError(LXDError):
    """The certificate was not found."""

    def __init__(self, fingerprint: str, certs) -> None:
        certs_str: str = "/n".join(certs) if certs else "No certificates found."
        super().__init__(
            f"404 - Certificate not found\n\nThe certificate with fingerprint '{fingerprint}' was not found. Available certificates:\n{certs_str}"  # noqa: E501
        )
