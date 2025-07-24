"""Basic usage examples for ProtoPRED API client"""

from protopred import ProtoPREDClient
from protopred.models import Module

# Initialize client with logging
client = ProtoPREDClient(
    account_token="1JX3LP",
    account_secret_key="A8X9641JM",
    account_user="OOntox",
    log_file="protopred_examples.log",  # All output will be logged here
    log_level="INFO"  # Log level: DEBUG, INFO, WARNING, ERROR
)

# Example 1: Single SMILES prediction
print("Example 1: Single SMILES prediction")
print("-" * 50)

result = client.predict_single(
    smiles="CCCCC",
    module=Module.PROTOPHYSCHEM,
    models=["model_phys:water_solubility", "model_phys:melting_point"]
)

for model_name, predictions in result.predictions.items():
    print(f"\n{model_name}:")
    for pred in predictions:
        print(f"  Predicted value: {pred.predicted_value}")
        print(f"  Numerical value: {pred.predicted_numerical}")
        print(f"  Applicability domain: {pred.applicability_domain}")

# Example 2: Batch prediction with metadata
print("\n\nExample 2: Batch prediction with metadata")
print("-" * 50)

molecules = {
    "pentane": {
        "SMILES": "CCCCC",
        "CAS": "109-66-0",
        "Chemical name": "Pentane"
    },
    "benzoquinone": {
        "SMILES": "C1=CC(=O)C=CC1=O",
        "CAS": "106-51-4",
        "Chemical name": "1,4-Benzoquinone"
    }
}

batch_result = client.predict_batch(
    molecules=molecules,
    module="ProtoPHYSCHEM",
    models=["model_phys:water_solubility", "model_phys:log_kow"]
)

# Get results for specific molecule
pentane_results = batch_result.get_molecule_results("pentane")
for model_name, pred in pentane_results.items():
    print(f"\nPentane - {model_name}:")
    print(f"  Chemical name: {pred.chemical_name}")
    print(f"  Predicted: {pred.predicted_value}")

# Example 3: Excel output
print("\n\nExample 3: Excel output")
print("-" * 50)

output_file = client.predict_batch(
    molecules=molecules,
    module="ProtoADME",
    models=[
        "model_abs:bioavailability30",
        "model_met:CYP450_3A4_inhibitor",
        "model_dist:blood-brain_barrier"
    ],
    output_format="XLSX",
    output_file="adme_predictions.xlsx"
)

print(f"Predictions saved to: {output_file}")

# Example 4: Using file input
print("\n\nExample 4: File input")
print("-" * 50)

# Assuming you have a JSON file with molecules
json_file_path = "molecules.json"
# file_result = client.predict(
#     module="ProtoPHYSCHEM",
#     models="model_phys:water_solubility",
#     input_data=json_file_path,
#     input_type="SMILES_FILE"
# )

print("\n" + "=" * 60)
print("LOGGING INFORMATION")
print("=" * 60)
print("All API calls, requests, responses, and errors have been logged to:")
print("📄 protopred_examples.log")
print("\nCheck this file to see:")
print("- Client initialization")
print("- API request details")
print("- Response status and sizes")
print("- Prediction summaries")
print("- Any errors or warnings")
print("- Timing information")
print("\nFor more detailed logging, use log_level='DEBUG'")