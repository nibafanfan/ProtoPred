"""Main API client for ProtoPRED API"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import requests
from requests.exceptions import RequestException

from .models import (
    Module, ModelType, InputType, OutputType,
    Molecule, PredictionResponse
)
from .exceptions import (
    ProtoPREDError, AuthenticationError, ValidationError,
    APIError, NetworkError
)
from .constants import AVAILABLE_MODELS, BASE_URL
from .logging_config import ProtoPREDLogger


class ProtoPREDClient:
    """Client for interacting with the ProtoPRED API."""
    
    def __init__(
        self,
        account_token: str,
        account_secret_key: str,
        account_user: str,
        base_url: str = BASE_URL,
        timeout: int = 30,
        log_file: str = None,
        log_level: str = "INFO"
    ):
        """
        Initialize the ProtoPRED API client.
        
        Args:
            account_token: API account token
            account_secret_key: API secret key
            account_user: API account username
            base_url: Base URL for the API (default: official ProtoPRED API)
            timeout: Request timeout in seconds
            log_file: Path to log file (default: protopred_api.log)
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.account_token = account_token
        self.account_secret_key = account_secret_key
        self.account_user = account_user
        self.base_url = base_url  # Keep trailing slash for API endpoint
        self.timeout = timeout
        
        # Setup logging
        self._logger_instance = ProtoPREDLogger()
        if log_file or log_level != "INFO":
            self._logger_instance.configure(log_file, log_level)
        self.logger = self._logger_instance.logger
        
        self.logger.info(f"ProtoPRED client initialized for user: {account_user}")
        self.logger.debug(f"Base URL: {self.base_url}, Timeout: {timeout}s")
        
    def predict(
        self,
        module: Union[Module, str],
        models: Union[List[str], str],
        input_data: Union[str, Dict[str, Molecule], Path],
        input_type: Optional[Union[InputType, str]] = None,
        output_type: Union[OutputType, str] = OutputType.JSON,
        output_file: Optional[Path] = None
    ) -> Union[PredictionResponse, Path]:
        """
        Make predictions using ProtoPRED models.
        
        Args:
            module: Module to use (ProtoPHYSCHEM or ProtoADME)
            models: List of models or comma-separated string of models
            input_data: SMILES string, dictionary of molecules, or path to file
            input_type: Type of input (auto-detected if not specified)
            output_type: Format of output (JSON or XLSX)
            output_file: Path to save output file (for XLSX output)
            
        Returns:
            PredictionResponse object for JSON output, or Path to saved file for XLSX
            
        Raises:
            ValidationError: If input validation fails
            APIError: If API returns an error
            NetworkError: If network request fails
        """
        try:
            # Validate and prepare module
            if isinstance(module, str):
                module = Module(module)
                
            # Prepare models list
            if isinstance(models, list):
                models_str = ", ".join(models)
            else:
                models_str = models
                
            # Count molecules for logging
            if isinstance(input_data, dict):
                num_molecules = len(input_data)
            elif isinstance(input_data, str) and not Path(input_data).exists():
                num_molecules = 1  # Single SMILES
            else:
                num_molecules = "unknown"
            
            self.logger.info(f"Starting prediction - Module: {module.value}, Models: {models_str}")
            self._logger_instance.log_prediction_summary(module.value, models_str, num_molecules)
            
            # Validate models
            self._validate_models(module, models_str)
            self.logger.debug("Model validation passed")
            
            # Auto-detect input type if not specified
            if input_type is None:
                input_type = self._detect_input_type(input_data)
                self.logger.debug(f"Auto-detected input type: {input_type.value}")
            elif isinstance(input_type, str):
                input_type = InputType(input_type)
                
            # Prepare request data
            query = {
                "account_token": self.account_token,
                "account_secret_key": self.account_secret_key,
                "account_user": self.account_user,
                "module": module.value,
                "models_list": models_str,
                "input_type": input_type.value,
            }
            
            if isinstance(output_type, str):
                output_type = OutputType(output_type)
                
            if output_type == OutputType.XLSX:
                query["output_type"] = output_type.value
            
            self.logger.debug(f"Request prepared - Input type: {input_type.value}, Output type: {output_type.value}")
                
            # Prepare request based on input type
            files = None
            if input_type == InputType.SMILES_TEXT:
                if not isinstance(input_data, str):
                    raise ValidationError("input_data must be a SMILES string for SMILES_TEXT input type")
                query["input_data"] = input_data
                self.logger.debug(f"Single SMILES input: {input_data[:50]}{'...' if len(input_data) > 50 else ''}")
                response = self._make_request(query)
            elif input_type == InputType.SMILES_FILE:
                if isinstance(input_data, (str, Path)):
                    # File upload
                    self.logger.debug(f"File upload: {input_data}")
                    files = {"input_data": open(input_data, "rb")}
                    response = self._make_request(query, files=files)
                elif isinstance(input_data, dict):
                    # Embedded JSON
                    self.logger.debug(f"Embedded JSON with {len(input_data)} molecules")
                    query["input_data"] = input_data
                    response = self._make_request(query, json_body=True)
                else:
                    raise ValidationError("input_data must be a file path or dictionary for SMILES_FILE input type")
                    
            # Handle response
            if output_type == OutputType.XLSX:
                if output_file is None:
                    output_file = Path("protopred_predictions.xlsx")
                with open(output_file, "wb") as f:
                    f.write(response.content)
                self.logger.info(f"Excel output saved to: {output_file}")
                return output_file
            else:
                result = PredictionResponse.from_json(response.json())
                self.logger.info("Prediction completed successfully - JSON response received")
                self.logger.debug(f"Response contains {len(result.predictions)} model results")
                return result
                
        except Exception as e:
            self._logger_instance.log_error(e, "Prediction failed")
            raise
            
    def predict_single(
        self,
        smiles: str,
        module: Union[Module, str],
        models: Union[List[str], str]
    ) -> PredictionResponse:
        """
        Convenience method for single SMILES prediction.
        
        Args:
            smiles: SMILES string of the molecule
            module: Module to use
            models: Models to run
            
        Returns:
            PredictionResponse object
        """
        return self.predict(
            module=module,
            models=models,
            input_data=smiles,
            input_type=InputType.SMILES_TEXT
        )
        
    def predict_batch(
        self,
        molecules: Dict[str, Union[str, Molecule]],
        module: Union[Module, str],
        models: Union[List[str], str],
        output_format: Union[OutputType, str] = OutputType.JSON,
        output_file: Optional[Path] = None
    ) -> Union[PredictionResponse, Path]:
        """
        Convenience method for batch prediction.
        
        Args:
            molecules: Dictionary of molecules (ID -> SMILES string or Molecule object)
            module: Module to use
            models: Models to run
            output_format: Output format (JSON or XLSX)
            output_file: Path to save output file (for XLSX)
            
        Returns:
            PredictionResponse object or Path to saved file
        """
        # Convert to proper format
        formatted_molecules = {}
        for mol_id, mol_data in molecules.items():
            if isinstance(mol_data, str):
                formatted_molecules[mol_id] = {"SMILES": mol_data}
            elif isinstance(mol_data, dict):
                formatted_molecules[mol_id] = mol_data
            else:
                raise ValidationError(f"Invalid molecule data for ID {mol_id}")
                
        return self.predict(
            module=module,
            models=models,
            input_data=formatted_molecules,
            input_type=InputType.SMILES_FILE,
            output_type=output_format,
            output_file=output_file
        )
        
    def _detect_input_type(self, input_data: Any) -> InputType:
        """Auto-detect input type based on input data."""
        if isinstance(input_data, str):
            if Path(input_data).exists():
                return InputType.SMILES_FILE
            else:
                return InputType.SMILES_TEXT
        elif isinstance(input_data, Path):
            return InputType.SMILES_FILE
        elif isinstance(input_data, dict):
            return InputType.SMILES_FILE
        else:
            raise ValidationError("Unable to detect input type from input_data")
            
    def _validate_models(self, module: Module, models_str: str):
        """Validate that requested models are available for the module."""
        model_pairs = [m.strip() for m in models_str.split(",")]
        
        for model_pair in model_pairs:
            if ":" not in model_pair:
                raise ValidationError(f"Invalid model format: {model_pair}. Expected format: 'model_type:model_name'")
                
            model_type, model_name = model_pair.split(":", 1)
            model_type = model_type.strip().lower()
            model_name = model_name.strip().lower()
            
            if module.value not in AVAILABLE_MODELS:
                raise ValidationError(f"Unknown module: {module.value}")
                
            if model_type not in AVAILABLE_MODELS[module.value]:
                raise ValidationError(f"Unknown model type '{model_type}' for module {module.value}")
                
            available_model_names = [m.lower() for m in AVAILABLE_MODELS[module.value][model_type]]
            if model_name not in available_model_names:
                raise ValidationError(f"Unknown model '{model_name}' for {module.value}/{model_type}")
                
    def _make_request(
        self,
        query: Dict[str, Any],
        files: Optional[Dict] = None,
        json_body: bool = False
    ) -> requests.Response:
        """Make HTTP request to the API."""
        try:
            # Log request details
            method = "POST"
            self._logger_instance.log_api_request(method, self.base_url, query)
            
            # Ensure HTTPS URL (prevent HTTP redirects)
            url = self.base_url
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
                self.logger.warning(f"Upgraded HTTP to HTTPS: {url}")
            
            if json_body:
                self.logger.debug("Sending JSON request")
                headers = {"Content-Type": "application/json"}
                response = requests.post(
                    url,
                    json=query,
                    headers=headers,
                    timeout=self.timeout,
                    allow_redirects=False  # Prevent HTTP redirects
                )
            else:
                self.logger.debug("Sending form data request" + (" with file upload" if files else ""))
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                response = requests.post(
                    url,
                    data=query,
                    files=files,
                    headers=headers if not files else None,  # Don't set Content-Type with file uploads
                    timeout=self.timeout,
                    allow_redirects=False  # Prevent HTTP redirects
                )
                
            # Log response details
            response_size = len(response.content) if response.content else 0
            self._logger_instance.log_api_response(response.status_code, response_size)
            
            response.raise_for_status()
            
            # Check for API errors in response
            if response.headers.get("Content-Type", "").startswith("application/json"):
                data = response.json()
                if isinstance(data, dict) and "error" in data:
                    self.logger.error(f"API returned error: {data['error']}")
                    raise APIError(data["error"])
            
            self.logger.debug("Request completed successfully")
            return response
            
        except requests.exceptions.Timeout as e:
            self.logger.error(f"Request timed out after {self.timeout}s")
            raise NetworkError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Failed to connect to {self.base_url}")
            raise NetworkError("Failed to connect to API")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                self.logger.error("Authentication failed - check credentials")
                raise AuthenticationError("Invalid authentication credentials")
            elif e.response.status_code == 400:
                self.logger.error(f"Bad request: {e.response.text}")
                raise ValidationError(f"Bad request: {e.response.text}")
            else:
                self.logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                raise APIError(f"HTTP {e.response.status_code}: {e.response.text}")
        except RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise NetworkError(f"Request failed: {str(e)}")