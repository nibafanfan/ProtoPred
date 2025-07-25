# ProtoPRED Pydantic Client

A modern, type-safe Python client for the ProtoPRED API built with Pydantic for data validation and requests for HTTP communication.

## Features

- 🚀 **Type-safe**: Full Pydantic validation for requests and responses
- 🔄 **Automatic retries**: Built-in retry logic with exponential backoff  
- 📝 **Multiple input formats**: Single SMILES, batch dictionaries, or file uploads
- 📊 **Multiple output formats**: JSON responses or Excel files
- 🛡️ **Comprehensive error handling**: Detailed exception hierarchy
- 🧪 **Context manager support**: Automatic resource cleanup
- 📖 **Full API coverage**: All ProtoPRED API endpoints and options

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from protopred_pydantic_client import ProtoPREDClient, APICredentials, ModuleType

# Create credentials
credentials = APICredentials(
    account_token="your_token",
    account_secret_key="your_secret",
    account_user="your_username"
)

# Use client with context manager
with ProtoPREDClient(credentials) as client:
    # Single SMILES prediction
    response = client.predict_single(
        smiles="CCCCC",
        module=ModuleType.PROTOPHYSCHEM,
        models=["model_phys:water_solubility", "model_phys:melting_point"]
    )
    
    print(f"Predictions for {len(response.molecules)} molecules")
    for mol in response.molecules:
        for model_name, result in mol.models.items():
            print(f"{model_name}: {result.prediction}")
```

## API Reference

### Client Initialization

```python
from protopred_pydantic_client import ProtoPREDClient, APICredentials, ClientConfig

credentials = APICredentials(
    account_token="your_token",
    account_secret_key="your_secret", 
    account_user="your_username"
)

config = ClientConfig(
    timeout=30,           # Request timeout in seconds
    max_retries=3,        # Maximum retry attempts
    retry_delay=1.0       # Base delay between retries
)

client = ProtoPREDClient(credentials, config)
```

### Prediction Methods

#### Single SMILES Prediction

```python
response = client.predict_single(
    smiles="CCCCC",
    module=ModuleType.PROTOPHYSCHEM,
    models=["model_phys:water_solubility", "model_phys:melting_point"],
    output_type=OutputType.JSON  # or OutputType.XLSX
)
```

#### Batch Prediction

```python
molecules = {
    "mol1": "CCCCC",
    "mol2": Molecule(SMILES="C1=CC(=O)C=CC1=O", chemical_name="Benzoquinone"),
    "mol3": {"SMILES": "CCO", "CAS": "64-17-5"}
}

response = client.predict_batch(
    molecules=molecules,
    module=ModuleType.PROTOPHYSCHEM,
    models="model_phys:water_solubility, model_phys:melting_point"
)
```

#### File Upload Prediction

```python
response = client.predict_from_file(
    file_path="molecules.json",  # or "molecules.xlsx"
    module=ModuleType.PROTOPHYSCHEM,
    models=["model_phys:water_solubility"]
)
```

### Response Handling

```python
# JSON Response
response = client.predict_single(...)
for mol in response.molecules:
    print(f"Molecule: {mol.smiles}")
    for model_name, result in mol.models.items():
        print(f"  {model_name}: {result.prediction}")

# Excel Response  
xlsx_data = client.predict_single(..., output_type=OutputType.XLSX)
output_path = client.save_xlsx_response(xlsx_data, "results.xlsx")
```

### Data Models

#### Molecule

```python
from protopred_pydantic_client import Molecule

molecule = Molecule(
    SMILES="CCCCC",
    CAS="109-66-0",
    chemical_name="Pentane",
    ec_number="203-692-4",
    structural_formula="C5H12"
)
```

#### Response Objects

```python
# PredictionResponse contains:
response.success          # bool
response.message         # Optional[str] 
response.timestamp       # Optional[datetime]
response.molecules       # List[MoleculeResult]
response.metadata        # Optional[Dict]

# MoleculeResult contains:
mol.molecule_id          # str
mol.smiles              # str  
mol.models              # Dict[str, ModelResult]
mol.errors              # Optional[List[str]]

# ModelResult contains:
result.model_name        # str
result.prediction        # Union[float, str]
result.unit             # Optional[str]
result.confidence       # Optional[float]
```

### Error Handling

```python
from protopred_pydantic_client import (
    ValidationError, AuthenticationError, APIError, 
    NetworkError, TimeoutError, FileError
)

try:
    response = client.predict_single(...)
except ValidationError as e:
    print(f"Input validation failed: {e}")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except APIError as e:
    print(f"API error: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
```

## Supported Modules and Models

### ProtoPHYSCHEM
- `model_phys:water_solubility`
- `model_phys:melting_point`
- (Additional models as available)

### ProtoADME  
- `model_adme:bioavailability`
- (Additional models as available)

## Examples

See the `examples/` directory for complete usage examples:

- `basic_usage.py` - Simple prediction examples
- `advanced_usage.py` - Advanced features and error handling

## API Compatibility

This client supports all ProtoPRED API v2 features:

- ✅ Single SMILES text input (API Option 1)
- ✅ File upload with form data (API Option 2) 
- ✅ Excel output format (API Option 3)
- ✅ Embedded JSON requests (API Option 4)
- ✅ JSON file upload (API Option 5)

## Requirements

- Python 3.7+
- pydantic >= 1.8.0
- requests >= 2.25.0
- typing-extensions >= 3.7.4

## License

This client is provided as-is for use with the ProtoPRED API service.