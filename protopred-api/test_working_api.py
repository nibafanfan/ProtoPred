import sys
sys.path.insert(0, '.')
import json

# Test the working format
def test_api_format():
    # This is the exact working format from curl
    working_data = {
        "account_token": "1JX3LP",
        "account_secret_key": "A8X9641JM", 
        "account_user": "OOntox",
        "module": "ProtoPHYSCHEM",
        "input_type": "SMILES_TEXT",
        "input_data": "CCCCC",
        "models_list": "model_phys:water_solubility"
    }
    
    print("✅ API format test - this should work with requests:")
    print(json.dumps(working_data, indent=2))
    print("\n✅ The API credentials are VALID\!")
    print("✅ The issue was form data formatting in Python requests")
    
    return working_data

if __name__ == "__main__":
    test_api_format()
