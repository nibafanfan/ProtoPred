"""Advanced usage examples for ProtoPRED API client"""

from pathlib import Path
from protopred import ProtoPREDClient
from protopred.models import Module, Molecule
from protopred.exceptions import ValidationError, APIError

# Initialize client
client = ProtoPREDClient(
    account_token="1JX3LP",
    account_secret_key="A8X9641JM",
    account_user="OOntox"
)

# Example 1: Using Molecule objects
print("Example 1: Using Molecule objects")
print("-" * 50)

molecules = {
    "drug1": Molecule(
        SMILES="CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
        CAS="15687-27-1",
        chemical_name="Ibuprofen",
        structural_formula="C13H18O2"
    ),
    "drug2": Molecule(
        SMILES="CC(=O)OC1=CC=CC=C1C(=O)O",
        CAS="50-78-2",
        chemical_name="Aspirin",
        EC_number="200-064-1"
    )
}

# Convert to dict format
molecules_dict = {
    mol_id: mol.to_dict() for mol_id, mol in molecules.items()
}

result = client.predict_batch(
    molecules=molecules_dict,
    module="ProtoADME",
    models=[
        "model_abs:bioavailability30",
        "model_abs:human_intestinal_absorption",
        "model_met:CYP450_3A4_substrate"
    ]
)

# Example 2: Error handling
print("\n\nExample 2: Error handling")
print("-" * 50)

try:
    # Try with invalid model
    client.predict_single(
        smiles="CCCCC",
        module="ProtoPHYSCHEM",
        models=["model_phys:invalid_model"]
    )
except ValidationError as e:
    print(f"Validation error caught: {e}")

# Example 3: Multiple modules in one session
print("\n\nExample 3: Multiple predictions")
print("-" * 50)

smiles = "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"  # Caffeine

# Physicochemical properties
physchem_result = client.predict_single(
    smiles=smiles,
    module="ProtoPHYSCHEM",
    models=[
        "model_phys:water_solubility",
        "model_phys:log_kow",
        "model_phys:melting_point"
    ]
)

# ADME properties
adme_result = client.predict_single(
    smiles=smiles,
    module="ProtoADME",
    models=[
        "model_abs:bioavailability30",
        "model_dist:blood-brain_barrier",
        "model_met:CYP450_1A2_substrate"
    ]
)

print("Caffeine predictions:")
print("\nPhysicochemical properties:")
for model, preds in physchem_result.predictions.items():
    if preds:
        print(f"  {model}: {preds[0].predicted_value}")

print("\nADME properties:")
for model, preds in adme_result.predictions.items():
    if preds:
        print(f"  {model}: {preds[0].predicted_value}")

# Example 4: Processing results
print("\n\nExample 4: Processing results")
print("-" * 50)

# Get all water solubility predictions
water_sol_results = physchem_result.get_model_results("Water solubility")
if water_sol_results:
    pred = water_sol_results[0]
    print(f"Water solubility prediction details:")
    print(f"  Value: {pred.predicted_value}")
    print(f"  Numerical: {pred.predicted_numerical} g/L")
    print(f"  Log units: {pred.predicted_numerical_model_units} log mol/L")
    print(f"  Applicability: {pred.applicability_domain}")

# Example 5: Saving different output formats
print("\n\nExample 5: Output formats")
print("-" * 50)

# JSON output (default)
json_result = client.predict_batch(
    molecules={"caffeine": smiles},
    module="ProtoPHYSCHEM",
    models=["model_phys:water_solubility"]
)

# Excel output
excel_path = client.predict_batch(
    molecules={"caffeine": smiles},
    module="ProtoPHYSCHEM",
    models=["model_phys:water_solubility"],
    output_format="XLSX",
    output_file=Path("caffeine_predictions.xlsx")
)

print(f"JSON result type: {type(json_result)}")
print(f"Excel saved to: {excel_path}")