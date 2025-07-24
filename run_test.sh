#!/bin/bash

echo "🚀 Running ProtoPRED API Test"
echo "============================="
echo "Date: $(date)"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the API directory
cd "$SCRIPT_DIR/protopred-api"

# Set Python path
export PYTHONPATH="$SCRIPT_DIR/protopred-api:$PYTHONPATH"

# Run the basic example and log output
echo "Running basic prediction example..."
python3 examples/basic_usage.py 2>&1 | tee -a protopred_test_$(date +%Y%m%d_%H%M%S).log

echo ""
echo "✅ Test complete. Check the log file for details."
echo "Log files: protopred_*.log"