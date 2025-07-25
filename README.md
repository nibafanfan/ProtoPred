# ProtoPRED API Python Client

Python wrapper for the ProtoPRED molecular property prediction API (https://protopred.protoqsar.com/).

## Overview

This repository contains two Python client implementations for the ProtoPRED API:

1. **protopred-api/** - Original client with dataclasses and logging
2. **protopred-pydantic-client/** - Enhanced client with Pydantic validation

Both clients support all ProtoPRED API features including ProtoPHYSCHEM and ProtoADME modules.

## Features

- 🧪 Single and batch SMILES predictions
- 📊 JSON and Excel output formats
- 📁 File upload support (JSON/Excel)
- 🔄 Automatic retry with exponential backoff
- 📝 Comprehensive logging
- ✅ Type safety with Pydantic models
- 🛡️ Robust error handling

## Quick Start

### Using the Pydantic Client (Recommended)

```python
from protopred_pydantic_client.final_client import ProtoPREDClient, APICredentials

credentials = APICredentials(
    account_token="your_token",
    account_secret_key="your_secret",
    account_user="your_username"
)

with ProtoPREDClient(credentials) as client:
    # Single molecule prediction
    response = client.predict_single(
        smiles="CCCCC",
        module="ProtoPHYSCHEM",
        models=["model_phys:water_solubility", "model_phys:melting_point"]
    )
    
    for mol in response.molecules:
        for pred in mol.predictions:
            print(f"{pred.property_name}: {pred.predicted_value}")
```

### Using the Original Client

```python
from protopred import ProtoPREDClient

client = ProtoPREDClient(
    account_token="your_token",
    account_secret_key="your_secret",
    account_user="your_username"
)

response = client.predict_single(
    smiles="CCCCC",
    module="ProtoPHYSCHEM", 
    models=["model_phys:water_solubility"]
)
```

## Available Models

### ProtoPHYSCHEM
- `model_phys:melting_point`
- `model_phys:boiling_point`
- `model_phys:vapour_pressure`
- `model_phys:water_solubility`
- `model_phys:log_kow`
- `model_phys:log_d`
- `model_phys:surface_tension`

### ProtoADME
- Absorption: `model_abs:bioavailability20`, `model_abs:caco-2_permeability`, etc.
- Metabolism: `model_met:CYP450_1A2_inhibitor`, etc.
- Distribution: `model_dist:blood-brain_barrier`, etc.
- Excretion: `model_exc:half-life`, etc.

## Documentation

- [API Documentation](ProtoPRED_API_ProtoQSAR_v2.pdf) - Official API specification
- [Results Verification](RESULTS_VERIFICATION.md) - How we validate predictions
- [Packaging Verification](PACKAGING_VERIFICATION.md) - Implementation details

## Requirements

- Python 3.7+
- requests
- pydantic (for enhanced client)

## License

This is a third-party client for the ProtoPRED API. Please refer to ProtoQSAR's terms of service for API usage.

## Acknowledgments

API credentials in examples are test credentials provided in the official documentation.