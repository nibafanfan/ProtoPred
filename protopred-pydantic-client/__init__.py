"""Pydantic-based ProtoPRED API client."""

from client import ProtoPREDClient
from models import (
    APICredentials, ClientConfig, ModuleType, InputType, OutputType,
    Molecule, PredictionResponse, ModelResult, MoleculeResult
)
from exceptions import (
    ProtoPREDError, ValidationError, AuthenticationError,
    APIError, NetworkError, TimeoutError, FileError
)

__version__ = "1.0.0"
__all__ = [
    "ProtoPREDClient",
    "APICredentials",
    "ClientConfig", 
    "ModuleType",
    "InputType",
    "OutputType",
    "Molecule",
    "PredictionResponse",
    "ModelResult",
    "MoleculeResult",
    "ProtoPREDError",
    "ValidationError",
    "AuthenticationError",
    "APIError",
    "NetworkError", 
    "TimeoutError",
    "FileError"
]