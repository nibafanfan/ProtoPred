"""Pydantic-based ProtoPRED API client."""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Union, BinaryIO
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from pydantic import ValidationError as PydanticValidationError

from models import (
    APICredentials, ClientConfig, ModuleType, InputType, OutputType,
    SingleSmilesRequest, BatchSmilesRequest, FileUploadRequest,
    PredictionResponse, Molecule, APIError as APIErrorModel
)
from exceptions import (
    ProtoPREDError, ValidationError, AuthenticationError,
    APIError, NetworkError, TimeoutError, FileError
)


class ProtoPREDClient:
    """Pydantic-based client for the ProtoPRED API."""
    
    def __init__(
        self,
        credentials: Union[APICredentials, Dict[str, str]],
        config: Optional[Union[ClientConfig, Dict[str, any]]] = None
    ):
        """
        Initialize the ProtoPRED client.
        
        Args:
            credentials: API credentials (APICredentials object or dict)
            config: Client configuration (ClientConfig object or dict)
        """
        # Validate and store credentials
        if isinstance(credentials, dict):
            self.credentials = APICredentials(**credentials)
        else:
            self.credentials = credentials
            
        # Validate and store config
        if config is None:
            self.config = ClientConfig()
        elif isinstance(config, dict):
            self.config = ClientConfig(**config)
        else:
            self.config = config
            
        # Create requests session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ProtoPRED-Pydantic-Client/1.0'
        })
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.session.close()
    
    def predict_single(
        self,
        smiles: str,
        module: Union[ModuleType, str],
        models: Union[List[str], str],
        output_type: Union[OutputType, str] = OutputType.JSON
    ) -> Union[PredictionResponse, bytes]:
        """
        Predict properties for a single SMILES string.
        
        Args:
            smiles: SMILES string of the molecule
            module: Module to use (ProtoPHYSCHEM or ProtoADME)
            models: List of models or comma-separated string
            output_type: Output format (JSON or XLSX)
            
        Returns:
            PredictionResponse for JSON output or bytes for XLSX
        """
        # Prepare models string
        if isinstance(models, list):
            models_str = ", ".join(models)
        else:
            models_str = models
        
        # Convert string enums
        if isinstance(module, str):
            module = ModuleType(module)
        if isinstance(output_type, str):
            output_type = OutputType(output_type)
        
        # Create request model
        try:
            request = SingleSmilesRequest(
                account_token=self.credentials.account_token,
                account_secret_key=self.credentials.account_secret_key,
                account_user=self.credentials.account_user,
                module=module,
                models_list=models_str,
                input_data=smiles,
                output_type=output_type if output_type != OutputType.JSON else None
            )
        except PydanticValidationError as e:
            raise ValidationError(f"Request validation failed: {e}")
        
        return self._make_request(request, output_type=output_type)
    
    def predict_batch(
        self,
        molecules: Dict[str, Union[str, Molecule, Dict]],
        module: Union[ModuleType, str],
        models: Union[List[str], str],
        output_type: Union[OutputType, str] = OutputType.JSON
    ) -> Union[PredictionResponse, bytes]:
        """
        Predict properties for multiple molecules.
        
        Args:
            molecules: Dictionary of molecules (ID -> SMILES/Molecule/dict)
            module: Module to use
            models: List of models or comma-separated string
            output_type: Output format (JSON or XLSX)
            
        Returns:
            PredictionResponse for JSON output or bytes for XLSX
        """
        # Prepare models string
        if isinstance(models, list):
            models_str = ", ".join(models)
        else:
            models_str = models
        
        # Convert string enums
        if isinstance(module, str):
            module = ModuleType(module)
        if isinstance(output_type, str):
            output_type = OutputType(output_type)
        
        # Convert molecules to proper format
        formatted_molecules = {}
        for mol_id, mol_data in molecules.items():
            if isinstance(mol_data, str):
                # Simple SMILES string
                formatted_molecules[mol_id] = Molecule(SMILES=mol_data)
            elif isinstance(mol_data, dict):
                # Dictionary data
                formatted_molecules[mol_id] = Molecule(**mol_data)
            elif isinstance(mol_data, Molecule):
                # Already a Molecule object
                formatted_molecules[mol_id] = mol_data
            else:
                raise ValidationError(f"Invalid molecule data type for {mol_id}: {type(mol_data)}")
        
        # Create request model
        try:
            request = BatchSmilesRequest(
                account_token=self.credentials.account_token,
                account_secret_key=self.credentials.account_secret_key,
                account_user=self.credentials.account_user,
                module=module,
                models_list=models_str,
                input_data=formatted_molecules,
                output_type=output_type if output_type != OutputType.JSON else None
            )
        except PydanticValidationError as e:
            raise ValidationError(f"Request validation failed: {e}")
        
        return self._make_request(request, output_type=output_type, json_body=True)
    
    def predict_from_file(
        self,
        file_path: Union[str, Path],
        module: Union[ModuleType, str],
        models: Union[List[str], str],
        output_type: Union[OutputType, str] = OutputType.JSON
    ) -> Union[PredictionResponse, bytes]:
        """
        Predict properties from file upload.
        
        Args:
            file_path: Path to input file (JSON or Excel)
            module: Module to use
            models: List of models or comma-separated string
            output_type: Output format (JSON or XLSX)
            
        Returns:
            PredictionResponse for JSON output or bytes for XLSX
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileError(f"File not found: {file_path}")
        
        # Prepare models string
        if isinstance(models, list):
            models_str = ", ".join(models)
        else:
            models_str = models
        
        # Convert string enums
        if isinstance(module, str):
            module = ModuleType(module)
        if isinstance(output_type, str):
            output_type = OutputType(output_type)
        
        # Create request model
        try:
            request = FileUploadRequest(
                account_token=self.credentials.account_token,
                account_secret_key=self.credentials.account_secret_key,
                account_user=self.credentials.account_user,
                module=module,
                models_list=models_str,
                output_type=output_type if output_type != OutputType.JSON else None
            )
        except PydanticValidationError as e:
            raise ValidationError(f"Request validation failed: {e}")
        
        return self._make_request(request, output_type=output_type, file_path=file_path)
    
    def _make_request(
        self,
        request_model: Union[SingleSmilesRequest, BatchSmilesRequest, FileUploadRequest],
        output_type: OutputType,
        json_body: bool = False,
        file_path: Optional[Path] = None
    ) -> Union[PredictionResponse, bytes]:
        """
        Make HTTP request to the API with retry logic.
        
        Args:
            request_model: Validated request model
            output_type: Expected output format
            json_body: Whether to send JSON body
            file_path: Path to file for upload
            
        Returns:
            PredictionResponse or raw bytes for XLSX
        """
        request_data = request_model.dict(exclude_none=True)
        
        for attempt in range(self.config.max_retries + 1):
            try:
                if json_body:
                    # Embedded JSON request (Option 4 from examples)
                    response = self.session.post(
                        self.config.base_url,
                        json=request_data,
                        timeout=self.config.timeout
                    )
                elif file_path:
                    # File upload request (Option 2/3 from examples)
                    with open(file_path, 'rb') as f:
                        files = {'input_data': f}
                        response = self.session.post(
                            self.config.base_url,
                            data=request_data,
                            files=files,
                            timeout=self.config.timeout
                        )
                else:
                    # Form data request (Option 1 from examples)
                    response = self.session.post(
                        self.config.base_url,
                        data=request_data,
                        timeout=self.config.timeout
                    )
                
                # Handle response
                return self._handle_response(response, output_type)
                
            except (Timeout, ConnectionError) as e:
                if attempt < self.config.max_retries:
                    time.sleep(self.config.retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    if isinstance(e, Timeout):
                        raise TimeoutError(f"Request timed out after {self.config.max_retries + 1} attempts")
                    else:
                        raise NetworkError(f"Connection failed after {self.config.max_retries + 1} attempts")
            
            except RequestException as e:
                raise NetworkError(f"Request failed: {str(e)}")
    
    def _handle_response(
        self,
        response: requests.Response,
        output_type: OutputType
    ) -> Union[PredictionResponse, bytes]:
        """
        Handle API response and parse it appropriately.
        
        Args:
            response: HTTP response object
            output_type: Expected output format
            
        Returns:
            Parsed response data
        """
        # Check for HTTP errors
        if response.status_code == 401:
            raise AuthenticationError("Invalid authentication credentials")
        elif response.status_code == 400:
            raise ValidationError(f"Bad request: {response.text}")
        elif not response.ok:
            raise APIError(
                f"HTTP {response.status_code}: {response.text}",
                status_code=response.status_code
            )
        
        # Handle XLSX output
        if output_type == OutputType.XLSX:
            return response.content
        
        # Handle JSON output
        try:
            response_data = response.json()
            
            # Get extra JSON from headers if available
            extra_json = None
            if 'X-Extra-JSON' in response.headers:
                try:
                    extra_json = json.loads(response.headers['X-Extra-JSON'])
                except json.JSONDecodeError:
                    pass  # Ignore if can't parse extra JSON
            
            # Check for API-level errors
            if isinstance(response_data, dict) and 'error' in response_data:
                raise APIError(response_data['error'])
            
            # Parse response into PredictionResponse
            return PredictionResponse.from_api_response(response_data, extra_json)
            
        except json.JSONDecodeError as e:
            raise APIError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise ProtoPREDError(f"Response parsing failed: {str(e)}")
    
    def save_xlsx_response(self, xlsx_data: bytes, output_path: Union[str, Path]) -> Path:
        """
        Save XLSX response data to file.
        
        Args:
            xlsx_data: Raw XLSX bytes from API
            output_path: Path to save the file
            
        Returns:
            Path to saved file
        """
        output_path = Path(output_path)
        try:
            with open(output_path, 'wb') as f:
                f.write(xlsx_data)
            return output_path
        except IOError as e:
            raise FileError(f"Failed to save XLSX file: {str(e)}")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()