"""Data models for ProtoPRED API"""

from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field


class Module(str, Enum):
    """Available ProtoPRED modules"""
    PROTOPHYSCHEM = "ProtoPHYSCHEM"
    PROTOADME = "ProtoADME"


class ModelType(str, Enum):
    """Model types for different modules"""
    # ProtoPHYSCHEM
    MODEL_PHYS = "model_phys"
    
    # ProtoADME
    MODEL_ABS = "model_abs"
    MODEL_MET = "model_met"
    MODEL_DIST = "model_dist"
    MODEL_EXC = "model_exc"


class InputType(str, Enum):
    """Input data types"""
    SMILES_TEXT = "SMILES_TEXT"
    SMILES_FILE = "SMILES_FILE"


class OutputType(str, Enum):
    """Output format types"""
    JSON = "JSON"
    XLSX = "XLSX"


@dataclass
class Molecule:
    """Represents a molecule with metadata"""
    SMILES: str
    CAS: Optional[str] = None
    chemical_name: Optional[str] = field(default=None, metadata={"key": "Chemical name"})
    EC_number: Optional[str] = field(default=None, metadata={"key": "EC number"})
    structural_formula: Optional[str] = field(default=None, metadata={"key": "Structural formula"})
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to API-compatible dictionary"""
        result = {"SMILES": self.SMILES}
        
        if self.CAS:
            result["CAS"] = self.CAS
        if self.chemical_name:
            result["Chemical name"] = self.chemical_name
        if self.EC_number:
            result["EC number"] = self.EC_number
        if self.structural_formula:
            result["Structural formula"] = self.structural_formula
            
        return result


@dataclass
class PredictionResult:
    """Represents a single prediction result"""
    ID: str
    SMILES: str
    predicted_value: str
    predicted_numerical: float
    predicted_value_model_units: str
    predicted_numerical_model_units: float
    applicability_domain: str
    
    # Optional fields
    experimental_value: Optional[str] = None
    experimental_numerical: Optional[float] = None
    experimental_value_model_units: Optional[str] = None
    experimental_numerical_model_units: Optional[float] = None
    probability: Optional[Union[str, float]] = None
    
    # Metadata
    chemical_name: Optional[str] = None
    CAS: Optional[str] = None
    EC_number: Optional[str] = None
    structural_formula: Optional[str] = None
    other_regulatory_id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], molecule_id: str = "molecule_1") -> "PredictionResult":
        """Create from API response dictionary (real API format)"""
        return cls(
            ID=molecule_id,  # Generate ID since API doesn't provide one for single molecules
            SMILES=data["SMILES"],
            predicted_value=data["Predicted value"],
            predicted_numerical=data["Predicted numerical"],
            predicted_value_model_units=data["Predicted value (model units)"],
            predicted_numerical_model_units=data["Predicted numerical (model units)"],
            applicability_domain=data["Applicability domain**"],
            experimental_value=data.get("Experimental value*"),
            experimental_numerical=data.get("Experimental numerical"),
            experimental_value_model_units=data.get("Experimental value (model units)*"),
            experimental_numerical_model_units=data.get("Experimental numerical (model units)"),
            probability=data.get("Probability"),
            chemical_name=data.get("Chemical name", "-") if data.get("Chemical name", "-") != "-" else None,
            CAS=data.get("CAS", "-") if data.get("CAS", "-") != "-" else None,
            EC_number=data.get("EC number", "-") if data.get("EC number", "-") != "-" else None,
            structural_formula=data.get("Structural formula", "-") if data.get("Structural formula", "-") != "-" else None,
            other_regulatory_id=data.get("Other Regulatory ID", "-") if data.get("Other Regulatory ID", "-") != "-" else None,
        )


@dataclass
class PredictionResponse:
    """Response from ProtoPRED API containing all predictions"""
    predictions: Dict[str, List[PredictionResult]]
    
    @classmethod
    def from_json(cls, data: Dict[str, Union[Dict, List[Dict]]], input_molecules: Dict[str, str] = None) -> "PredictionResponse":
        """Create from API JSON response (handles real API format)"""
        predictions = {}
        
        for model_name, result_data in data.items():
            if isinstance(result_data, dict):
                # Single molecule response format (real API)
                molecule_id = "molecule_1"  # Default for single molecules
                predictions[model_name] = [
                    PredictionResult.from_dict(result_data, molecule_id)
                ]
            elif isinstance(result_data, list):
                # Multi-molecule response format (if API returns arrays)
                predictions[model_name] = [
                    PredictionResult.from_dict(result, f"molecule_{i+1}") 
                    for i, result in enumerate(result_data)
                ]
            else:
                raise ValueError(f"Unexpected result format for model {model_name}: {type(result_data)}")
                
        return cls(predictions=predictions)
    
    def get_model_results(self, model_name: str) -> List[PredictionResult]:
        """Get results for a specific model"""
        return self.predictions.get(model_name, [])
    
    def get_molecule_results(self, molecule_id: str) -> Dict[str, PredictionResult]:
        """Get all predictions for a specific molecule"""
        results = {}
        for model_name, predictions in self.predictions.items():
            for pred in predictions:
                if pred.ID == molecule_id:
                    results[model_name] = pred
                    break
        return results