import os
import sys
from functools import lru_cache
from typing import Any, Dict, Optional

import httpx
from httpx import Client, HTTPTransport, Response
from loguru import logger

from lxd_python.models import SyncResponse


@lru_cache(maxsize=1)
def get_socket_location() -> str:
    """Get the location of the LXD socket.

    Snap and non-snap installations of LXD use different socket locations.

    Returns:
        str: The location of the LXD socket.
    """

    if os.path.exists("/var/snap/lxd/common/lxd/unix.socket"):
        logger.debug("Snap installation of LXD detected. Using /var/snap/lxd/common/lxd/unix.socket.")
        return "/var/snap/lxd/common/lxd/unix.socket"

    logger.debug("Non-snap installation of LXD detected. Using /var/lib/lxd/unix.socket.")
    return "/var/lib/lxd/unix.socket"


class LXD:
    def __init__(self) -> None:
        # TODO: Add a way to configure logging.
        log_format: str = (
            "<green>{time:YYYY-MM-DD at HH:mm:ss}</green>"
            " <level>{level: <5}</level>"
            " <magenta>{extra[method]}</magenta>"
            " <cyan>{extra[path]}</cyan>"
            " <white>{message}</white>"
            " <dim>{extra[response]}</dim>"
        )
        logger.configure(extra={"method": "", "path": "", "response": ""})
        logger.remove()
        logger.add(
            sys.stderr,
            format=log_format,
            level="DEBUG",
            colorize=True,
            backtrace=False,
            diagnose=False,
            catch=True,
        )

        transport: HTTPTransport = httpx.HTTPTransport(uds=get_socket_location())
        self.client: Client = Client(transport=transport)

    @logger.catch
    def close(self) -> None:
        """Close the client."""
        logger.info("Closing client.")
        self.client.close()

    @logger.catch
    def get(self, path: str, params: Optional[Dict[str, Any]] = None):
        """Get a resource.

        Args:
            path: The path to the resource. For example, /1.0/containers.
            params: The query parameters. Defaults to None.

        Returns:
            SyncResponse: The response from the LXD server.
        """
        response: Response = self.client.get(f"http://localhost{path}", params=params)
        logger.debug("", method="GET", path=path, response=response)
        return response.json()

    @logger.catch
    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> SyncResponse:
        """Post a resource.

        Args:
            path: The path to the resource. For example, /1.0/containers.
            data: The data to post. Defaults to None.

        Returns:
            SyncResponse: The response from the LXD server.
        """
        response = self.client.post(f"http://localhost{path}", json=data).json()
        logger.debug("", method="POST", path=path, response=response)
        return response

    @logger.catch
    def delete(self, path: str) -> SyncResponse:
        """Delete a resource.

        Args:
            path: The path to the resource.

        Returns:
            SyncResponse: The response from the LXD server.
        """
        response = self.client.delete(f"http://localhost{path}").json()
        logger.debug("", method="DELETE", path=path, response=response)
        return response

    @logger.catch
    def put(self, path: str, data: Optional[Dict[str, Any]] = None) -> SyncResponse:
        """Put a resource.

        Args:
            path: The path to the resource.
            data: The data to put. Defaults to None.

        Returns:
            SyncResponse: The response from the LXD server.
        """
        response = self.client.put(f"http://localhost{path}", json=data).json()
        logger.debug("", method="PUT", path=path, response=response)
        return response

    @logger.catch
    def patch(self, path: str, data: Optional[Dict[str, Any]] = None) -> SyncResponse:
        """Patch a resource.

        Args:
            path: The path to the resource.
            data: The data to patch. Defaults to None.

        Returns:
            SyncResponse: The response from the LXD server.
        """
        response = self.client.patch(f"http://localhost{path}", json=data).json()
        logger.debug("", method="PATCH", path=path, response=response)
        return response
