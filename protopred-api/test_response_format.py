#!/usr/bin/env python3
"""Test parsing the real API response format"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json

# This is the actual response format from the working curl command
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

def test_response_parsing():
    """Test how to parse the real API response"""
    
    print("🔍 Real API Response Format:")
    print(json.dumps(real_api_response, indent=2))
    
    print("\n📋 Analysis:")
    print(f"- Top level keys: {list(real_api_response.keys())}")
    
    for model_name, result_data in real_api_response.items():
        print(f"\n📊 Model: {model_name}")
        print(f"   - SMILES: {result_data['SMILES']}")
        print(f"   - Predicted: {result_data['Predicted value']}")
        print(f"   - Experimental: {result_data['Experimental value*']}")
        print(f"   - Applicability: {result_data['Applicability domain**']}")
        
    print("\n✅ Key insights:")
    print("1. Response is {model_name: result_data} not {model_name: [result_data]}")
    print("2. Single molecule returns single object, not array")
    print("3. No 'ID' field - would need to be generated")
    print("4. Has 'Other Regulatory ID' field not in our model")
    
    return real_api_response

if __name__ == "__main__":
    test_response_parsing()