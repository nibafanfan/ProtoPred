#!/usr/bin/env python3
"""Test the real API response format"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import json
from protopred.logging_config import ProtoPREDLogger

def test_real_api():
    """Test with the exact working format from curl"""
    
    # Setup logging
    logger = ProtoPREDLogger()
    logger.configure("test_real_api.log", "DEBUG")
    
    # This is the exact working format
    query = {
        "account_token": "1JX3LP",
        "account_secret_key": "A8X9641JM", 
        "account_user": "OOntox",
        "module": "ProtoPHYSCHEM",
        "input_type": "SMILES_TEXT",
        "input_data": "CCCCC",
        "models_list": "model_phys:water_solubility"
    }
    
    url = "https://protopred.protoqsar.com/API/v2/"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    logger.logger.info(f"Testing API call to {url}")
    logger.logger.debug(f"Request data: {query}")
    
    try:
        response = requests.post(url, data=query, headers=headers, timeout=30)
        
        logger.logger.info(f"Response status: {response.status_code}")
        logger.logger.debug(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            logger.logger.info("✅ API call successful!")
            logger.logger.info(f"Response keys: {list(result.keys())}")
            
            print("✅ SUCCESS! API is working")
            print(f"Response: {json.dumps(result, indent=2)}")
            
            return result
        else:
            logger.logger.error(f"❌ API call failed: {response.status_code}")
            logger.logger.error(f"Response text: {response.text}")
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        logger.logger.error(f"❌ Exception: {e}")
        print(f"❌ ERROR: {e}")
        return None

if __name__ == "__main__":
    test_real_api()