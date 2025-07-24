"""Example demonstrating logging functionality in ProtoPRED API client"""

from protopred import ProtoPREDClient, configure_logging
from protopred.models import Module
import os

# Example 1: Basic logging to default file
print("=== Example 1: Basic logging (default file) ===")

client = ProtoPREDClient(
    account_token="1JX3LP",
    account_secret_key="A8X9641JM",
    account_user="OOntox"
)

# Make a simple prediction
result = client.predict_single(
    smiles="CCCCC",
    module=Module.PROTOPHYSCHEM,
    models=["model_phys:water_solubility"]
)

print(f"Check the log file: protopred_api.log")

# Example 2: Custom log file and level
print("\n=== Example 2: Custom log file and DEBUG level ===")

client_debug = ProtoPREDClient(
    account_token="1JX3LP",
    account_secret_key="A8X9641JM",
    account_user="OOntox",
    log_file="protopred_debug.log",
    log_level="DEBUG"
)

# Batch prediction with debug logging
molecules = {
    "mol1": "CCCCC",
    "mol2": {"SMILES": "C1=CC(=O)C=CC1=O", "Chemical name": "Benzoquinone"}
}

batch_result = client_debug.predict_batch(
    molecules=molecules,
    module="ProtoPHYSCHEM",
    models=["model_phys:water_solubility", "model_phys:melting_point"]
)

print(f"Check the debug log file: protopred_debug.log")

# Example 3: Console logging disabled
print("\n=== Example 3: File-only logging (no console output) ===")

# Set environment variable to disable console logging
os.environ['PROTOPRED_CONSOLE_LOG'] = 'false'

client_quiet = ProtoPREDClient(
    account_token="1JX3LP",
    account_secret_key="A8X9641JM",
    account_user="OOntox",
    log_file="protopred_quiet.log",
    log_level="INFO"
)

# This will only log to file, not console
quiet_result = client_quiet.predict_single(
    smiles="CN1C=NC2=C1C(=O)N(C(=O)N2C)C",  # Caffeine
    module="ProtoADME",
    models=["model_abs:bioavailability30"]
)

print(f"Check the quiet log file: protopred_quiet.log (no console output from client)")

# Reset environment variable
os.environ['PROTOPRED_CONSOLE_LOG'] = 'true'

# Example 4: Global logging configuration
print("\n=== Example 4: Global logging configuration ===")

# Configure logging globally for all instances
configure_logging(log_file="protopred_global.log", log_level="WARNING")

client_global = ProtoPREDClient(
    account_token="1JX3LP",
    account_secret_key="A8X9641JM",
    account_user="OOntox"
)

# Only warnings and errors will be logged
try:
    # This will cause a validation error (invalid model)
    client_global.predict_single(
        smiles="CCCCC",
        module="ProtoPHYSCHEM",
        models=["model_phys:invalid_model"]
    )
except Exception as e:
    print(f"Expected error: {e}")

print(f"Check the global log file: protopred_global.log (only warnings/errors)")

# Example 5: Using environment variable for log file
print("\n=== Example 5: Environment variable configuration ===")

# Set log file via environment variable
os.environ['PROTOPRED_LOG_FILE'] = 'protopred_env.log'

client_env = ProtoPREDClient(
    account_token="1JX3LP",
    account_secret_key="A8X9641JM",
    account_user="OOntox"
)

env_result = client_env.predict_single(
    smiles="CC(=O)OC1=CC=CC=C1C(=O)O",  # Aspirin
    module="ProtoADME",
    models=["model_met:CYP450_3A4_substrate"]
)

print(f"Check the environment log file: protopred_env.log")

print("\n=== Log Files Created ===")
print("- protopred_api.log (default logging)")
print("- protopred_debug.log (debug level)")
print("- protopred_quiet.log (file-only)")
print("- protopred_global.log (warnings/errors only)")
print("- protopred_env.log (via environment variable)")

print("\nAll API calls and their details are now logged to these files!")
print("You can monitor API usage, debug issues, and track all predictions.")