"""Custom exceptions for ProtoPRED Pydantic client."""


class ProtoPREDError(Exception):
    """Base exception for ProtoPRED client errors."""
    pass


class ValidationError(ProtoPREDError):
    """Raised when input validation fails."""
    pass


class AuthenticationError(ProtoPREDError):
    """Raised when API authentication fails."""
    pass


class APIError(ProtoPREDError):
    """Raised when API returns an error response."""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class NetworkError(ProtoPREDError):
    """Raised when network request fails."""
    pass


class TimeoutError(ProtoPREDError):
    """Raised when request times out."""
    pass


class FileError(ProtoPREDError):
    """Raised when file operations fail."""
    pass