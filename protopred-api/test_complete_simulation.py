#!/usr/bin/env python3
"""Complete simulation of the working ProtoPRED client"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
import importlib.util

# Load models directly
spec = importlib.util.spec_from_file_location('models', 'protopred/models.py')
models_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models_module)

# Load logging directly  
spec_log = importlib.util.spec_from_file_location('logging_config', 'protopred/logging_config.py')
logging_config = importlib.util.module_from_spec(spec_log)
spec_log.loader.exec_module(logging_config)

class MockProtoPREDClient:
    """Mock client that simulates real API behavior"""
    
    def __init__(self, account_token, account_secret_key, account_user, log_file="test_simulation.log"):
        self.account_token = account_token
        self.account_secret_key = account_secret_key
        self.account_user = account_user
        
        # Setup logging
        self.logger_instance = logging_config.ProtoPREDLogger()
        self.logger_instance.configure(log_file, "INFO")
        self.logger = self.logger_instance.logger
        
        self.logger.info(f"Mock ProtoPRED client initialized for user: {account_user}")
        
    def predict_single(self, smiles, module, models):
        """Simulate single prediction"""
        
        self.logger.info(f"Starting prediction - Module: {module}, Models: {models}")
        self.logger.info(f"Single SMILES input: {smiles}")
        
        # Simulate the real API response format based on the working curl
        mock_response = {
            "Water solubility": {
                "Chemical name": "-",
                "EC number": "-", 
                "Other Regulatory ID": "-",
                "Structural formula": "-",
                "CAS": "-",
                "SMILES": smiles,
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
        
        self.logger.info("Mock API call completed successfully")
        
        # Parse using real models
        result = models_module.PredictionResponse.from_json(mock_response)
        self.logger.info(f"Response contains {len(result.predictions)} model results")
        
        return result

def test_complete_workflow():
    """Test the complete workflow"""
    
    print("🚀 Testing Complete ProtoPRED Workflow")
    print("=" * 50)
    
    # Initialize mock client (same interface as real client)
    client = MockProtoPREDClient(
        account_token="1JX3LP",
        account_secret_key="A8X9641JM",
        account_user="OOntox",
        log_file="complete_test.log"
    )
    
    print("✅ Client initialized")
    
    # Make prediction 
    result = client.predict_single(
        smiles="CCCCC",
        module="ProtoPHYSCHEM",
        models=["model_phys:water_solubility"]
    )
    
    print("✅ Prediction completed")
    
    # Display results (same as real client)
    print("\n📊 Results:")
    for model_name, predictions in result.predictions.items():
        print(f"\n{model_name}:")
        for pred in predictions:
            print(f"  SMILES: {pred.SMILES}")
            print(f"  Predicted value: {pred.predicted_value}")
            print(f"  Experimental value: {pred.experimental_value}")
            print(f"  Applicability domain: {pred.applicability_domain}")
    
    # Test logging
    print(f"\n📋 Check log file: complete_test.log")
    
    print("\n🎉 Complete workflow test successful!")
    print("\n✅ Ready for real API with proper requests installation!")
    
    return True

if __name__ == "__main__":
    test_complete_workflow()