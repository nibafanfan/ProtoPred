#!/usr/bin/env python3
"""Usage examples based on official ProtoPRED API documentation."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from client import ProtoPREDClient
from models import APICredentials, ModuleType, OutputType


def main():
    """Demonstrate usage with official API examples and model names."""
    
    print("🔬 ProtoPRED Pydantic Client - Official Examples")
    print("=" * 55)
    
    # Use official credentials from documentation
    credentials = APICredentials(
        account_token="1JX3LP",
        account_secret_key="A8X9641JM",
        account_user="OOntox"
    )
    
    with ProtoPREDClient(credentials) as client:
        
        # Example 1: Basic ProtoPHYSCHEM models (from documentation)
        print("\n1. ProtoPHYSCHEM - Physical properties:")
        print("-" * 40)
        
        try:
            response = client.predict_single(
                smiles="CCCCC",  # Pentane from docs
                module=ModuleType.PROTOPHYSCHEM,
                models=["model_phys:water_solubility", "model_phys:melting_point"]
            )
            
            print(f"✅ Success: {len(response.molecules)} molecules processed")
            for mol in response.molecules:
                print(f"🧬 SMILES: {mol.smiles}")
                for model_name, result in mol.models.items():
                    print(f"  📊 {model_name}: {result.prediction}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Example 2: Additional ProtoPHYSCHEM models
        print("\n2. ProtoPHYSCHEM - More properties:")
        print("-" * 35)
        
        try:
            response = client.predict_single(
                smiles="CCCCC",
                module=ModuleType.PROTOPHYSCHEM,
                models=[
                    "model_phys:boiling_point",
                    "model_phys:vapour_pressure", 
                    "model_phys:log_kow"
                ]
            )
            
            print(f"✅ Success: {len(response.molecules)} molecules processed")
            for mol in response.molecules:
                for model_name, result in mol.models.items():
                    print(f"  📊 {model_name}: {result.prediction}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Example 3: ProtoADME - Absorption models
        print("\n3. ProtoADME - Absorption properties:")
        print("-" * 35)
        
        try:
            response = client.predict_single(
                smiles="CCCCC",
                module=ModuleType.PROTOADME,
                models=[
                    "model_abs:bioavailability20",
                    "model_abs:caco-2_permeability",
                    "model_abs:human_intestinal_absorption"
                ]
            )
            
            print(f"✅ Success: {len(response.molecules)} molecules processed")
            for mol in response.molecules:
                for model_name, result in mol.models.items():
                    print(f"  📊 {model_name}: {result.prediction}")
                    
        except Exception as e:
            print(f"❌ ProtoADME error (may need subscription): {e}")
        
        # Example 4: ProtoADME - Metabolism models
        print("\n4. ProtoADME - Metabolism properties:")
        print("-" * 36)
        
        try:
            response = client.predict_single(
                smiles="CCCCC",
                module=ModuleType.PROTOADME,
                models=[
                    "model_met:CYP450_1A2_inhibitor",
                    "model_met:CYP450_3A4_substrate"
                ]
            )
            
            print(f"✅ Success: {len(response.molecules)} molecules processed")
            for mol in response.molecules:
                for model_name, result in mol.models.items():
                    print(f"  📊 {model_name}: {result.prediction}")
                    
        except Exception as e:
            print(f"❌ ProtoADME metabolism error: {e}")
        
        # Example 5: Batch prediction with molecules from documentation
        print("\n5. Batch prediction (from docs):")
        print("-" * 30)
        
        molecules = {
            "ID_1": "C1=CC(=O)C=CC1=O",  # Benzoquinone from docs
            "ID_2": {
                "SMILES": "CCCCC",
                "CAS": "109-66-0",
                "Chemical name": "Pentane",
                "EC number": "203-692-4",
                "Structural formula": "C5H12"
            },
            "ID_3": {
                "SMILES": "O=[N+]([O-])c1ccc2nc[nH]c2c1",
                "CAS": "94-52-0", 
                "Chemical name": "6-nitro-1H-benzimidazole",
                "EC number": "202-341-2",
                "Structural formula": "C7H5N3O2"
            }
        }
        
        try:
            response = client.predict_batch(
                molecules=molecules,
                module=ModuleType.PROTOPHYSCHEM,
                models="model_phys:water_solubility, model_phys:melting_point"
            )
            
            print(f"✅ Batch success: {len(response.molecules)} molecules processed")
            for mol in response.molecules:
                print(f"🧬 {mol.molecule_id}: {mol.smiles}")
                for model_name, result in mol.models.items():
                    print(f"  📊 {model_name}: {result.prediction}")
                    
        except Exception as e:
            print(f"❌ Batch error: {e}")
        
        # Example 6: Excel output
        print("\n6. Excel output:")
        print("-" * 15)
        
        try:
            xlsx_data = client.predict_single(
                smiles="CCCCC",
                module=ModuleType.PROTOPHYSCHEM,
                models="model_phys:water_solubility",
                output_type=OutputType.XLSX
            )
            
            output_file = client.save_xlsx_response(xlsx_data, "protopred_results.xlsx")
            print(f"✅ Excel file saved: {output_file}")
            print(f"📏 File size: {len(xlsx_data)} bytes")
            
        except Exception as e:
            print(f"❌ Excel error: {e}")


if __name__ == "__main__":
    main()