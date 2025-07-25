#!/usr/bin/env python3
"""Final production-ready ProtoPRED Pydantic client."""

import json
import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from pydantic import BaseModel, Field, field_validator


# Constants
BASE_URL = "https://protopred.protoqsar.com/API/v2/"


# Exceptions hierarchy
class ProtoPREDError(Exception):
    """Base exception for ProtoPRED client errors."""
    pass

class ValidationError(ProtoPREDError):
    """Input validation failed."""
    pass

class AuthenticationError(ProtoPREDError):
    """API authentication failed."""
    pass

class APIError(ProtoPREDError):
    """API returned an error."""
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code

class NetworkError(ProtoPREDError):
    """Network request failed."""
    pass

class TimeoutError(ProtoPREDError):
    """Request timed out."""
    pass

class FileError(ProtoPREDError):
    """File operation failed."""
    pass


# Enums
class ModuleType(str, Enum):
    PROTOPHYSCHEM = "ProtoPHYSCHEM"
    PROTOADME = "ProtoADME"

class InputType(str, Enum):
    SMILES_TEXT = "SMILES_TEXT"
    SMILES_FILE = "SMILES_FILE"

class OutputType(str, Enum):
    JSON = "JSON"
    XLSX = "XLSX"


# Core models
class APICredentials(BaseModel):
    """API authentication credentials."""
    account_token: str
    account_secret_key: str 
    account_user: str


class ClientConfig(BaseModel):
    """Client configuration."""
    base_url: str = BASE_URL
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    
    @field_validator('base_url')
    @classmethod
    def validate_base_url(cls, v):
        return v if v.endswith('/') else v + '/'


class Molecule(BaseModel):
    """Molecule with SMILES and metadata."""
    SMILES: str
    CAS: Optional[str] = None
    chemical_name: Optional[str] = Field(None, alias="Chemical name")
    ec_number: Optional[str] = Field(None, alias="EC number") 
    structural_formula: Optional[str] = Field(None, alias="Structural formula")
    
    model_config = {"populate_by_name": True}


class PredictionResult(BaseModel):
    """Single model prediction result."""
    property_name: str
    predicted_value: str
    predicted_numerical: Optional[float] = None
    experimental_value: Optional[str] = None
    experimental_numerical: Optional[float] = None
    applicability_domain: Optional[str] = None
    unit: Optional[str] = None


class MoleculePrediction(BaseModel):
    """Complete prediction for one molecule."""
    molecule_id: str
    smiles: str
    cas: Optional[str] = None
    chemical_name: Optional[str] = None
    predictions: List[PredictionResult] = Field(default_factory=list)


class PredictionResponse(BaseModel):
    """API response with parsed results."""
    success: bool = True
    molecules: List[MoleculePrediction] = Field(default_factory=list)
    raw_response: Optional[Dict] = None
    extra_json: Optional[Dict] = None
    timestamp: datetime = Field(default_factory=datetime.now)


# Main client
class ProtoPREDClient:
    """Production-ready ProtoPRED API client."""
    
    def __init__(self, credentials: Union[APICredentials, Dict], config: Optional[Union[ClientConfig, Dict]] = None):
        self.credentials = APICredentials(**credentials) if isinstance(credentials, dict) else credentials
        self.config = ClientConfig(**config) if isinstance(config, dict) else (config or ClientConfig())
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'ProtoPRED-Client/2.0'})
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    def predict_single(self, smiles: str, module: Union[ModuleType, str], models: Union[List[str], str], 
                      output_type: Union[OutputType, str] = OutputType.JSON) -> Union[PredictionResponse, bytes]:
        """Predict for single SMILES."""
        return self._predict(
            module=module,
            models=models,
            input_type=InputType.SMILES_TEXT,
            input_data=smiles,
            output_type=output_type
        )
    
    def predict_batch(self, molecules: Dict[str, Union[str, Dict, Molecule]], module: Union[ModuleType, str], 
                     models: Union[List[str], str], output_type: Union[OutputType, str] = OutputType.JSON) -> Union[PredictionResponse, bytes]:
        """Predict for multiple molecules."""
        # Format molecules for API
        formatted = {}
        for mol_id, mol_data in molecules.items():
            if isinstance(mol_data, str):
                formatted[mol_id] = {"SMILES": mol_data}
            elif isinstance(mol_data, dict):
                formatted[mol_id] = mol_data
            elif isinstance(mol_data, Molecule):
                formatted[mol_id] = mol_data.model_dump(by_alias=True, exclude_none=True)
            else:
                raise ValidationError(f"Invalid molecule data for {mol_id}")
        
        return self._predict(
            module=module,
            models=models,
            input_type=InputType.SMILES_FILE,
            input_data=formatted,
            output_type=output_type,
            json_body=True
        )
    
    def predict_from_file(self, file_path: Union[str, Path], module: Union[ModuleType, str], 
                         models: Union[List[str], str], output_type: Union[OutputType, str] = OutputType.JSON) -> Union[PredictionResponse, bytes]:
        """Predict from file upload."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileError(f"File not found: {file_path}")
        
        return self._predict(
            module=module,
            models=models,
            input_type=InputType.SMILES_FILE,
            output_type=output_type,
            file_path=file_path
        )
    
    def _predict(self, module, models, input_type, input_data=None, output_type=OutputType.JSON, 
                json_body=False, file_path=None) -> Union[PredictionResponse, bytes]:
        """Core prediction method."""
        # Convert enums
        if isinstance(module, str):
            module = ModuleType(module)
        if isinstance(output_type, str):
            output_type = OutputType(output_type)
        
        # Format models
        models_str = ", ".join(models) if isinstance(models, list) else models
        
        # Build request
        request_data = {
            "account_token": self.credentials.account_token,
            "account_secret_key": self.credentials.account_secret_key,
            "account_user": self.credentials.account_user,
            "module": module.value,
            "models_list": models_str,
            "input_type": input_type.value
        }
        
        if input_data is not None:
            request_data["input_data"] = input_data
        
        if output_type != OutputType.JSON:
            request_data["output_type"] = output_type.value
        
        return self._make_request(request_data, output_type, json_body, file_path)
    
    def _make_request(self, request_data: Dict, output_type: OutputType, json_body: bool = False, 
                     file_path: Optional[Path] = None) -> Union[PredictionResponse, bytes]:
        """Execute HTTP request with retries."""
        for attempt in range(self.config.max_retries + 1):
            try:
                if json_body:
                    response = self.session.post(self.config.base_url, json=request_data, timeout=self.config.timeout)
                elif file_path:
                    with open(file_path, 'rb') as f:
                        files = {'input_data': f}
                        response = self.session.post(self.config.base_url, data=request_data, files=files, timeout=self.config.timeout)
                else:
                    response = self.session.post(self.config.base_url, data=request_data, timeout=self.config.timeout)
                
                return self._handle_response(response, output_type)
                
            except (Timeout, ConnectionError) as e:
                if attempt < self.config.max_retries:
                    time.sleep(self.config.retry_delay * (2 ** attempt))
                    continue
                else:
                    error_class = TimeoutError if isinstance(e, Timeout) else NetworkError
                    raise error_class(f"Request failed after {self.config.max_retries + 1} attempts")
            
            except RequestException as e:
                raise NetworkError(f"Request failed: {e}")
    
    def _handle_response(self, response: requests.Response, output_type: OutputType) -> Union[PredictionResponse, bytes]:
        """Parse API response."""
        # Check HTTP errors
        if response.status_code == 401:
            raise AuthenticationError("Invalid credentials")
        elif response.status_code == 400:
            raise ValidationError(f"Bad request: {response.text}")
        elif not response.ok:
            raise APIError(f"HTTP {response.status_code}: {response.text}", response.status_code)
        
        # Handle Excel
        if output_type == OutputType.XLSX:
            return response.content
        
        # Parse JSON
        try:
            data = response.json()
            
            # Get extra JSON from headers
            extra_json = None
            if 'X-Extra-JSON' in response.headers:
                try:
                    extra_json = json.loads(response.headers['X-Extra-JSON'])
                except json.JSONDecodeError:
                    pass
            
            # Check for API errors
            if isinstance(data, dict) and 'error' in data:
                raise APIError(data['error'])
            
            # Parse molecules
            molecules = self._parse_response(data)
            
            return PredictionResponse(
                success=True,
                molecules=molecules,
                raw_response=data,
                extra_json=extra_json
            )
            
        except json.JSONDecodeError as e:
            raise APIError(f"Invalid JSON: {e}")
        except Exception as e:
            raise ProtoPREDError(f"Response parsing failed: {e}")
    
    def _parse_response(self, data: Dict) -> List[MoleculePrediction]:
        """Parse structured API response into molecules."""
        molecules_dict = {}
        
        # Handle both single and batch response formats
        if isinstance(data, dict):
            for property_name, results in data.items():
                if isinstance(results, list):
                    # Batch format: property -> list of results
                    for result in results:
                        if isinstance(result, dict) and 'ID' in result and 'SMILES' in result:
                            mol_id = result['ID']
                            self._add_molecule_result(molecules_dict, mol_id, result, property_name)
                elif isinstance(results, dict) and 'SMILES' in results:
                    # Single format: property -> single result (create synthetic ID)
                    mol_id = "molecule_1"
                    result = results.copy()
                    result['ID'] = mol_id
                    self._add_molecule_result(molecules_dict, mol_id, result, property_name)
        
        return list(molecules_dict.values())
    
    def _add_molecule_result(self, molecules_dict: Dict, mol_id: str, result: Dict, property_name: str):
        """Add a single result to the molecules dictionary."""
        if mol_id not in molecules_dict:
            molecules_dict[mol_id] = MoleculePrediction(
                molecule_id=mol_id,
                smiles=result.get('SMILES', ''),
                cas=result.get('CAS'),
                chemical_name=result.get('Chemical name'),
                predictions=[]
            )
        
        # Create prediction result
        prediction = PredictionResult(
            property_name=property_name,
            predicted_value=result.get('Predicted value', ''),
            predicted_numerical=result.get('Predicted numerical'),
            experimental_value=result.get('Experimental value*'),
            experimental_numerical=result.get('Experimental numerical'),
            applicability_domain=result.get('Applicability domain**')
        )
        
        molecules_dict[mol_id].predictions.append(prediction)
    
    def save_xlsx(self, xlsx_data: bytes, path: Union[str, Path]) -> Path:
        """Save Excel data to file."""
        path = Path(path)
        try:
            with open(path, 'wb') as f:
                f.write(xlsx_data)
            return path
        except IOError as e:
            raise FileError(f"Failed to save Excel: {e}")
    
    def close(self):
        """Close session."""
        self.session.close()


# Usage examples
def main():
    """Complete usage demonstration."""
    print("🚀 ProtoPRED Final Client - Complete Test")
    print("=" * 50)
    
    credentials = APICredentials(
        account_token="1JX3LP",
        account_secret_key="A8X9641JM",
        account_user="OOntox"
    )
    
    with ProtoPREDClient(credentials) as client:
        
        # Test 1: Single prediction
        print("\n1. Single SMILES (Pentane):")
        print("-" * 28)
        try:
            response = client.predict_single(
                smiles="CCCCC",
                module="ProtoPHYSCHEM",
                models=["model_phys:water_solubility", "model_phys:melting_point"]
            )
            
            print(f"✅ Molecules: {len(response.molecules)}")
            for mol in response.molecules:
                print(f"🧬 {mol.smiles}")
                for pred in mol.predictions:
                    print(f"   📊 {pred.property_name}: {pred.predicted_value}")
                    if pred.experimental_value:
                        print(f"      (exp: {pred.experimental_value})")
                        
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 2: Batch prediction
        print("\n2. Batch prediction:")
        print("-" * 18)
        try:
            molecules = {
                "pentane": {"SMILES": "CCCCC", "Chemical name": "Pentane"},
                "benzene": {"SMILES": "c1ccccc1", "Chemical name": "Benzene"},
                "water": {"SMILES": "O", "Chemical name": "Water"}
            }
            
            response = client.predict_batch(
                molecules=molecules,
                module="ProtoPHYSCHEM", 
                models="model_phys:water_solubility"
            )
            
            print(f"✅ Molecules: {len(response.molecules)}")
            for mol in response.molecules:
                print(f"🧬 {mol.molecule_id}: {mol.smiles}")
                if mol.chemical_name:
                    print(f"   Name: {mol.chemical_name}")
                for pred in mol.predictions:
                    print(f"   📊 {pred.property_name}: {pred.predicted_value}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 3: Excel output
        print("\n3. Excel export:")
        print("-" * 15)
        try:
            xlsx_data = client.predict_single(
                smiles="CCCCC",
                module="ProtoPHYSCHEM",
                models="model_phys:water_solubility,model_phys:melting_point",
                output_type="XLSX"
            )
            
            file_path = client.save_xlsx(xlsx_data, "final_test_results.xlsx")
            print(f"✅ Saved: {file_path} ({len(xlsx_data):,} bytes)")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 4: Error handling
        print("\n4. Error handling test:")
        print("-" * 22)
        try:
            # This should fail with validation error
            response = client.predict_single(
                smiles="",  # Empty SMILES
                module="ProtoPHYSCHEM",
                models="invalid:model"
            )
        except ValidationError as e:
            print(f"✅ Caught validation error: {e}")
        except Exception as e:
            print(f"✅ Caught error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()