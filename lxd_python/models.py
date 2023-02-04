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

    def __init__(self, response: dict) -> None:
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

    def __str__(self) -> str:
        # LXDException: Not authorized (path: /1.0/cluster, status code: 403)
        return f"LXDException: {self.error.capitalize()} (path: {self.path}, status code: {self.status_code})"

    def __repr__(self) -> str:
        # LXDException(path='/1.0/cluster', error='Not authorized', status_code=403, response_type='error')
        return f"LXDException(path='{self.path}', error='{self.error.capitalize()}', status_code={self.status_code}, response_type='{self.response_type}')"  # noqa: E501
