# ProtoPRED API Python Client

A Python client library for the ProtoPRED prediction platform API, providing easy access to physicochemical and ADME property predictions for molecules.

## Installation

```bash
pip install protopred-api
```

## Quick Start

```python
from protopred import ProtoPREDClient

# Initialize client with your credentials
client = ProtoPREDClient(
    account_token="your_token",
    account_secret_key="your_secret_key",
    account_user="your_username",
    log_file="protopred_api.log",  # All API calls logged here
    log_level="INFO"               # Logging detail level
)

# Single molecule prediction
result = client.predict_single(
    smiles="CCCCC",
    module="ProtoPHYSCHEM",
    models=["model_phys:water_solubility", "model_phys:melting_point"]
)

# Access results
for model_name, predictions in result.predictions.items():
    for pred in predictions:
        print(f"{model_name}: {pred.predicted_value}")
```

## Features

- Simple and intuitive API
- Support for single and batch predictions
- Automatic input type detection
- Type hints and data validation
- Comprehensive error handling
- Support for both JSON and Excel output formats
- **Comprehensive logging** - All API calls automatically logged to file

## Examples

### Batch Prediction

```python
# Define molecules
molecules = {
    "compound_1": "CCCCC",
    "compound_2": {
        "SMILES": "C1=CC(=O)C=CC1=O",
        "CAS": "106-51-4",
        "Chemical name": "Benzoquinone"
    }
}

# Run batch prediction
result = client.predict_batch(
    molecules=molecules,
    module="ProtoPHYSCHEM",
    models=["model_phys:water_solubility", "model_phys:log_kow"]
)
```

### Excel Output

```python
# Save predictions to Excel file
output_path = client.predict_batch(
    molecules=molecules,
    module="ProtoADME",
    models=["model_abs:bioavailability30", "model_met:CYP450_3A4_inhibitor"],
    output_format="XLSX",
    output_file="predictions.xlsx"
)
```

## Logging

All API interactions are automatically logged to help with debugging and monitoring:

```python
# Custom logging configuration
client = ProtoPREDClient(
    ...,
    log_file="my_predictions.log",  # Custom log file
    log_level="DEBUG"               # Detailed logging
)

# Global logging configuration
from protopred import configure_logging
configure_logging(log_file="global.log", log_level="INFO")
```

**What gets logged:**
- Client initialization and configuration
- API requests and responses
- Prediction summaries (module, models, molecule count)
- Errors and exceptions with context
- File operations and timing information

See [LOGGING.md](LOGGING.md) for detailed logging documentation.

## Available Modules and Models

### ProtoPHYSCHEM
- **model_phys**: melting_point, boiling_point, vapour_pressure, water_solubility, log_kow, log_d, surface_tension

### ProtoADME
- **model_abs**: bioavailability20/30, caco-2_permeability, p-gp_inhibitor/substrate, skin_permeability, human_intestinal_absorption
- **model_met**: CYP450 inhibitors and substrates (1A2, 2C19, 2C9, 2D6, 3A4)
- **model_dist**: blood-brain_barrier, plasma-protein_binding, volume_of_distribution
- **model_exc**: half-life, human_liver_microsomal, OATP1B1, OATP1B3, BSEP

## Documentation

For detailed documentation, visit [https://protopred-api.readthedocs.io](https://protopred-api.readthedocs.io)

## License

This project is licensed under the MIT License - see the LICENSE file for details.