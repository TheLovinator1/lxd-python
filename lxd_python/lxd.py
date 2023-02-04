import httpx
from httpx import Client, HTTPTransport

from lxd_python.models import LXDException, SyncResponse


class LXD:
    def __init__(self) -> None:
        transport: HTTPTransport = httpx.HTTPTransport(uds="/var/lib/lxd/unix.socket")
        self.client: Client = Client(transport=transport)

    def close(self) -> None:
        """Close the client."""
        self.client.close()

    def get(self, path: str) -> SyncResponse:
        """Get a resource.

        Args:
            path (str): The path to the resource.

        Returns:
            SyncResponse: The response from the LXD server.

        Raises:
            LXDException: If the response contains an error.
        """
        response = self.client.get(f"http://localhost{path}").json()
        if response.get("type", "").lower == "error":
            raise LXDException(response)
        return SyncResponse(response)
