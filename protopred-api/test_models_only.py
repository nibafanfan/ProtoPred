#!/usr/bin/env python3
"""Test just the models without importing requests"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json

# Import models directly
from protopred.models import PredictionResponse, PredictionResult

# Real API response format
real_api_response = {
    "Water solubility": {
        "Chemical name": "-",
        "EC number": "-", 
        "Other Regulatory ID": "-",
        "Structural formula": "-",
        "CAS": "-",
        "SMILES": "CCCCC",
        "Experimental value*": "0.038 g/L",
        "Predicted value": "0.066 g/L",
        "Experimental value (model units)*": "-3.28 log mol/L",
        "Predicted value (model units)": "-3.04 log mol/L",
        "Experimental numerical": 0.038,
        "Predicted numerical": 0.066,
        "Experimental numerical (model units)": -3.2785,
        "Predicted numerical (model units)": -3.0369,
        "Applicability domain**": "Inside (T/L/E/R)"
    }
}

def test_model_parsing():
    """Test the updated model parsing"""
    
    print("🧪 Testing updated model parsing...")
    
    try:
        # Test parsing with the real API response
        response = PredictionResponse.from_json(real_api_response)
        
        print("✅ PredictionResponse created successfully!")
        print(f"   Models: {list(response.predictions.keys())}")
        
        # Test accessing results
        water_sol_results = response.get_model_results("Water solubility")
        print(f"   Water solubility results: {len(water_sol_results)} found")
        
        if water_sol_results:
            result = water_sol_results[0]
            print(f"\n📊 First result details:")
            print(f"   ID: {result.ID}")
            print(f"   SMILES: {result.SMILES}")
            print(f"   Predicted value: {result.predicted_value}")
            print(f"   Experimental value: {result.experimental_value}")
            print(f"   Applicability domain: {result.applicability_domain}")
            print(f"   Other regulatory ID: {result.other_regulatory_id}")
            
        print("\n✅ All model parsing tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Model parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_model_parsing()