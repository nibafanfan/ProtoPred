"""Pydantic models for ProtoPRED API client."""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, field_validator, model_validator
from constants import AVAILABLE_MODELS


class ModuleType(str, Enum):
    """Available ProtoPRED modules."""
    PROTOPHYSCHEM = "ProtoPHYSCHEM"
    PROTOADME = "ProtoADME"


class InputType(str, Enum):
    """Input data types."""
    SMILES_TEXT = "SMILES_TEXT"
    SMILES_FILE = "SMILES_FILE"


class OutputType(str, Enum):
    """Output format types."""
    JSON = "JSON"
    XLSX = "XLSX"


class Molecule(BaseModel):
    """Represents a molecule with SMILES and optional metadata."""
    SMILES: str = Field(..., description="SMILES string representation")
    CAS: Optional[str] = Field(None, description="CAS number")
    chemical_name: Optional[str] = Field(None, alias="Chemical name")
    ec_number: Optional[str] = Field(None, alias="EC number")
    structural_formula: Optional[str] = Field(None, alias="Structural formula")
    
    class Config:
        populate_by_name = True


class APICredentials(BaseModel):
    """API authentication credentials."""
    account_token: str = Field(..., description="API account token")
    account_secret_key: str = Field(..., description="API secret key")
    account_user: str = Field(..., description="API account username")


class PredictionRequest(BaseModel):
    """Base prediction request model."""
    account_token: str
    account_secret_key: str
    account_user: str
    module: ModuleType
    input_type: InputType
    models_list: str = Field(..., description="Comma-separated list of models")
    output_type: Optional[OutputType] = None
    
    @field_validator('models_list')
    @classmethod
    def validate_models_list(cls, v):
        """Validate models list format and availability."""
        if not v.strip():
            raise ValueError("models_list cannot be empty")
        
        models = [m.strip() for m in v.split(',')]
        for model in models:
            if ':' not in model:
                raise ValueError(f"Invalid model format: {model}. Expected 'model_type:model_name'")
        return v
    
    @model_validator(mode='after')
    def validate_models_for_module(self):
        """Validate that models are available for the specified module."""
        module = self.module
        models_list = self.models_list
        
        if module and models_list and hasattr(module, 'value'):
            module_name = module.value
            if module_name in AVAILABLE_MODELS:
                models = [m.strip() for m in models_list.split(',')]
                for model in models:
                    if ':' in model:
                        model_type, model_name = [part.strip().lower() for part in model.split(':', 1)]
                        
                        # Check if model type exists for this module
                        available_types = {k.lower(): v for k, v in AVAILABLE_MODELS[module_name].items()}
                        if model_type not in available_types:
                            available = ', '.join(AVAILABLE_MODELS[module_name].keys())
                            raise ValueError(f"Unknown model type '{model_type}' for {module_name}. Available: {available}")
                        
                        # Check if model name exists for this type
                        available_models = [m.lower().replace('-', '_') for m in available_types[model_type]]
                        model_name_normalized = model_name.replace('-', '_')
                        if model_name_normalized not in available_models:
                            available = ', '.join(available_types[model_type])
                            raise ValueError(f"Unknown model '{model_name}' for {module_name}/{model_type}. Available: {available}")
        
        return self


class SingleSmilesRequest(PredictionRequest):
    """Request for single SMILES prediction."""
    input_data: str = Field(..., description="SMILES string")
    input_type: InputType = Field(InputType.SMILES_TEXT, const=True)


class BatchSmilesRequest(PredictionRequest):
    """Request for batch SMILES prediction with embedded JSON."""
    input_data: Dict[str, Molecule] = Field(..., description="Dictionary of molecules")
    input_type: InputType = Field(InputType.SMILES_FILE, const=True)


class FileUploadRequest(PredictionRequest):
    """Request for file upload prediction."""
    input_type: InputType = Field(InputType.SMILES_FILE, const=True)
    # Note: file data handled separately in client


class ModelResult(BaseModel):
    """Result from a single model prediction."""
    model_name: str = Field(..., description="Name of the model")
    prediction: Union[float, str] = Field(..., description="Prediction value")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    confidence: Optional[float] = Field(None, description="Prediction confidence")
    
    model_config = {"extra": "allow"}  # Allow additional fields from API response


class MoleculeResult(BaseModel):
    """Results for a single molecule."""
    molecule_id: str = Field(..., description="Molecule identifier")
    smiles: str = Field(..., description="SMILES string")
    models: Dict[str, ModelResult] = Field(..., description="Model results")
    errors: Optional[List[str]] = Field(None, description="Any errors for this molecule")
    
    model_config = {"extra": "allow"}


class PredictionResponse(BaseModel):
    """Complete prediction response."""
    success: bool = Field(..., description="Whether the request was successful")
    message: Optional[str] = Field(None, description="Response message")
    timestamp: Optional[datetime] = Field(None, description="Response timestamp")
    molecules: List[MoleculeResult] = Field(default_factory=list, description="Molecule results")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    @classmethod
    def from_api_response(cls, response_data: dict, extra_json: dict = None) -> "PredictionResponse":
        """Create PredictionResponse from API response data."""
        # Handle different response formats from the API
        molecules = []
        
        if isinstance(response_data, dict):
            # If response_data contains molecule results directly
            for mol_id, mol_data in response_data.items():
                if isinstance(mol_data, dict) and 'SMILES' in mol_data:
                    # Extract model results
                    models = {}
                    smiles = mol_data.get('SMILES', '')
                    
                    for key, value in mol_data.items():
                        if key not in ['SMILES', 'CAS', 'Chemical name', 'EC number', 'Structural formula']:
                            # This is likely a model result
                            models[key] = ModelResult(
                                model_name=key,
                                prediction=value,
                                unit=None,
                                confidence=None
                            )
                    
                    molecules.append(MoleculeResult(
                        molecule_id=mol_id,
                        smiles=smiles,
                        models=models
                    ))
        
        return cls(
            success=True,
            molecules=molecules,
            metadata=extra_json if extra_json else None
        )
    
    model_config = {"extra": "allow"}


class APIError(BaseModel):
    """API error response."""
    error: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class ClientConfig(BaseModel):
    """Configuration for the ProtoPRED client."""
    base_url: str = Field("https://protopred.protoqsar.com/API/v2/", description="API base URL")
    timeout: int = Field(30, description="Request timeout in seconds")
    max_retries: int = Field(3, description="Maximum number of retries")
    retry_delay: float = Field(1.0, description="Delay between retries in seconds")
    
    @field_validator('base_url')
    @classmethod
    def validate_base_url(cls, v):
        """Ensure base URL ends with slash."""
        if not v.endswith('/'):
            v += '/'
        return v