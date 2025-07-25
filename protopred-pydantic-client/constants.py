"""Constants for ProtoPRED API based on official documentation."""

# Available models by module (from ProtoPRED_API_ProtoQSAR_v2.txt)
AVAILABLE_MODELS = {
    "ProtoPHYSCHEM": {
        "model_phys": [
            "melting_point",
            "boiling_point", 
            "vapour_pressure",
            "water_solubility",
            "log_kow",
            "log_d",
            "surface_tension"
        ]
    },
    "ProtoADME": {
        "model_abs": [
            "bioavailability20",
            "bioavailability30",
            "caco-2_permeability",
            "p-gp_inhibitor",
            "p-gp_substrate", 
            "skin_permeability",
            "human_intestinal_absorption"
        ],
        "model_met": [
            "CYP450_1A2_inhibitor",
            "CYP450_1A2_substrate",
            "CYP450_2C19_inhibitor",
            "CYP450_2C19_substrate",
            "CYP450_2C9_inhibitor",
            "CYP450_2D6_inhibitor",
            "CYP450_2D6_substrate",
            "CYP450_3A4_inhibitor",
            "CYP450_3A4_substrate",
            "human_liver_microsomal"
        ],
        "model_dist": [
            "blood-brain_barrier",
            "plasma-protein_binding",
            "volume_of_distribution"
        ],
        "model_exc": [
            "half-life",
            "OATP1B1",
            "OATP1B3", 
            "BSEP"
        ]
    }
}

# Base API URL
BASE_URL = "https://protopred.protoqsar.com/API/v2/"

# Supported metadata fields
METADATA_FIELDS = [
    "SMILES",
    "CAS", 
    "Chemical name",
    "EC number",
    "Structural formula"
]