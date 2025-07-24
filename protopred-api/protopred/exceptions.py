"""Custom exceptions for ProtoPRED API client"""


class ProtoPREDError(Exception):
    """Base exception for ProtoPRED API errors"""
    pass


class AuthenticationError(ProtoPREDError):
    """Raised when authentication fails"""
    pass


class ValidationError(ProtoPREDError):
    """Raised when input validation fails"""
    pass


class APIError(ProtoPREDError):
    """Raised when API returns an error"""
    pass


class NetworkError(ProtoPREDError):
    """Raised when network request fails"""
    pass