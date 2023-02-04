import httpx
from httpx import Client, HTTPTransport
from loguru import logger


class LXD:
    def __init__(self) -> None:
        transport: HTTPTransport = httpx.HTTPTransport(uds="/var/lib/lxd/unix.socket")
        self.client: Client = Client(
            transport=transport,
            event_hooks={
                "request": [self.log_request],
                "response": [self.log_response],
            },
        )

    def close(self) -> None:
        """Close the client."""
        self.client.close()

    def log_request(self, request) -> None:
        """Log the request."""
        logger.debug(f"Request: {request.method} {request.url}")

    def log_response(self, response) -> None:
        """Log the response."""
        logger.debug(f"Response: {response.status_code} {response.url}")

    def get(self, path: str) -> dict[str, str]:
        """Get a resource."""
        return self.client.get(f"http://localhost{path}").json()

    def get_api_endpoints(self) -> dict[str, str]:
        """Get API endpoints."""
        return self.get("/")

    def get_certificates(self) -> dict[str, str]:
        """Get certificates."""
        return self.get("/1.0/certificates")
