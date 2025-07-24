#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$SCRIPT_DIR/protopred_terminal_$(date +%Y%m%d).log"

echo "📝 Logging all output to: $LOG_FILE"
echo "======================================"

# Function to log with timestamp
log_with_timestamp() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $@" | tee -a "$LOG_FILE"
}

# Start logging
log_with_timestamp "Starting ProtoPRED API Test Session"
log_with_timestamp "Current directory: $(pwd)"
log_with_timestamp "Python version: $(python3 --version)"

# Change to the API directory
cd "$SCRIPT_DIR/protopred-api"

# Run basic usage example
log_with_timestamp "Running basic_usage.py"
python3 examples/basic_usage.py 2>&1 | tee -a "$LOG_FILE"

# Run logging example
log_with_timestamp "Running logging_example.py"
python3 examples/logging_example.py 2>&1 | tee -a "$LOG_FILE"

# Run advanced usage
log_with_timestamp "Running advanced_usage.py"
python3 examples/advanced_usage.py 2>&1 | tee -a "$LOG_FILE"

# Show log file location
echo ""
log_with_timestamp "Session complete"
echo "📋 All output saved to: $LOG_FILE"