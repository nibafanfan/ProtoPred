#!/bin/bash

echo "🔧 Installing ProtoPRED API Client"
echo "=================================="

echo "1. Installing dependencies..."
pip install requests

echo "2. Testing client installation..."
python3 -c "
try:
    from protopred import ProtoPREDClient
    print('✅ ProtoPRED client imported successfully')
except ImportError as e:
    print(f'❌ Import failed: {e}')
    exit(1)
"

echo "3. Running simple prediction test..."
python3 -c "
from protopred import ProtoPREDClient

client = ProtoPREDClient(
    account_token='1JX3LP',
    account_secret_key='A8X9641JM',
    account_user='OOntox',
    log_file='install_test.log'
)

try:
    result = client.predict_single(
        smiles='CCCCC',
        module='ProtoPHYSCHEM', 
        models='model_phys:water_solubility'
    )
    print('✅ API call successful!')
    print(f'   Results: {len(result.predictions)} models')
    for model_name, predictions in result.predictions.items():
        for pred in predictions:
            print(f'   {model_name}: {pred.predicted_value}')
    
except Exception as e:
    print(f'❌ API call failed: {e}')
    print('📋 Check install_test.log for details')
"

echo ""
echo "🎉 Installation complete!"
echo "Check install_test.log for detailed logs"