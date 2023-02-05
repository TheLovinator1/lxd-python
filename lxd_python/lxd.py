from typing import Any, Dict, Optional

import httpx
from httpx import Client, HTTPTransport

from lxd_python.exceptions import LXDException, LXDForbidden, LXDInternalServerError
from lxd_python.models import SyncResponse


class LXD:
    def __init__(self) -> None:
        transport: HTTPTransport = httpx.HTTPTransport(uds="/var/lib/lxd/unix.socket")
        self.client: Client = Client(transport=transport)

    def close(self) -> None:
        """Close the client."""
        self.client.close()

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> SyncResponse:
        """Get a resource.

        Args:
            path: The path to the resource.
            params: The query parameters. Defaults to None.

        Returns:
            SyncResponse: The response from the LXD server.

        Raises:
            LXDException: If the response contains an error.
        """
        response = self.client.get(f"http://localhost{path}", params=params).json()

        if response.error_code == 403:
            raise LXDForbidden(response=response, path=path)
        elif response.error_code == 500:
            raise LXDInternalServerError(response=response, path=path)
        elif response.error_code != 200:
            raise LXDException(response=response, path=path)

        return SyncResponse(response)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> SyncResponse:
        """Post a resource.

        Args:
            path: The path to the resource.
            data: The data to post. Defaults to None.

        Returns:
            SyncResponse: The response from the LXD server.

        Raises:
            LXDException: If the response contains an error.
        """
        response = self.client.post(f"http://localhost{path}", json=data).json()
        if response["type"] == "error":
            raise LXDForbidden(response, path=path)

        return SyncResponse(response)
