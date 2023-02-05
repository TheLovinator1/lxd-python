from dataclasses import dataclass

from lxd_python.models import SyncResponse


@dataclass
class LXDBaseException(Exception):
    path: str
    error: str
    status_code: int
    response_type: str
    error_code: int

    def __init__(self, response: SyncResponse, path: str) -> None:
        self.path = path
        self.error = response.error
        self.status_code = response.status_code
        self.response_type = response.response_type
        self.error_code = self.error_code

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path='{self.path}', error='{self.error.capitalize()}', status_code='{self.status_code}', response_type='{self.response_type}', error_code='{self.error_code}')"  # noqa: E501


class LXDException(LXDBaseException):
    def __str__(self) -> str:
        return f"LXDException: {self.error_code} - {self.error.capitalize()} (path: {self.path})"


class LXDForbidden(LXDBaseException):
    def __str__(self) -> str:
        return f"LXDForbidden: You are not authorized to access this resource (path: {self.path})"


class LXDInternalServerError(LXDBaseException):
    def __str__(self) -> str:
        return f"LXDInternalServerError: Internal server error (path: {self.path})"
