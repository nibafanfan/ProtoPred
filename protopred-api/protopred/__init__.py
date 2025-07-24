"""ProtoPRED API Client Package"""

from .client import ProtoPREDClient
from .models import (
    Module, ModelType, InputType, OutputType,
    Molecule, PredictionResult, PredictionResponse
)
from .exceptions import ProtoPREDError, AuthenticationError, ValidationError
from .logging_config import configure_logging, get_logger

__version__ = "0.1.0"
__all__ = [
    "ProtoPREDClient",
    "Module", "ModelType", "InputType", "OutputType", 
    "Molecule", "PredictionResult", "PredictionResponse",
    "ProtoPREDError", "AuthenticationError", "ValidationError",
    "configure_logging", "get_logger"
]