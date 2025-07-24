# ProtoPRED API Logging Guide

The ProtoPRED API client includes comprehensive logging functionality that automatically logs all API interactions, errors, and important events to a file. This helps with debugging, monitoring, and auditing API usage.

## Quick Start

```python
from protopred import ProtoPREDClient

# Initialize client with logging
client = ProtoPREDClient(
    account_token="your_token",
    account_secret_key="your_secret",
    account_user="your_user",
    log_file="my_protopred.log",  # Custom log file
    log_level="INFO"              # Logging level
)

# All operations are now automatically logged
result = client.predict_single(
    smiles="CCCCC",
    module="ProtoPHYSCHEM", 
    models=["model_phys:water_solubility"]
)
```

## Configuration Options

### 1. Client-Level Configuration

Configure logging when creating a client instance:

```python
client = ProtoPREDClient(
    account_token="token",
    account_secret_key="secret", 
    account_user="user",
    log_file="custom.log",     # Custom log file path
    log_level="DEBUG"          # Detailed logging
)
```

### 2. Global Configuration

Configure logging for all client instances:

```python
from protopred import configure_logging

# Set global logging configuration
configure_logging(
    log_file="global_protopred.log",
    log_level="INFO"
)

# All clients will now use this configuration
client = ProtoPREDClient(...)
```

### 3. Environment Variables

Control logging via environment variables:

```bash
# Set default log file
export PROTOPRED_LOG_FILE="protopred_api.log"

# Disable console output (log to file only)
export PROTOPRED_CONSOLE_LOG="false"
```

## Log Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| `DEBUG` | Detailed diagnostic information | Development, troubleshooting |
| `INFO` | General operational messages | Production monitoring |
| `WARNING` | Warning messages for unusual conditions | Production alerts |
| `ERROR` | Error messages for failures | Production error tracking |

## What Gets Logged

### Client Operations
- Client initialization with configuration
- Prediction job summaries (module, models, molecule count)
- Input validation results
- File operations (uploads, downloads)

### API Communications
- HTTP request details (method, URL, parameters)
- Response status codes and sizes
- Request/response timing
- Authentication attempts

### Errors and Exceptions
- Validation errors with context
- Network errors and timeouts
- API errors from server
- Authentication failures

### Example Log Output

```
2024-01-15 10:30:15 - protopred - INFO - ProtoPRED logging initialized - Log file: protopred_api.log
2024-01-15 10:30:15 - protopred - INFO - ProtoPRED client initialized for user: MyUser
2024-01-15 10:30:15 - protopred - DEBUG - Base URL: https://protopred.protoqsar.com/API/v2/, Timeout: 30s
2024-01-15 10:30:16 - protopred - INFO - Starting prediction - Module: ProtoPHYSCHEM, Models: model_phys:water_solubility
2024-01-15 10:30:16 - protopred - INFO - Prediction job - Module: ProtoPHYSCHEM, Models: model_phys:water_solubility, Molecules: 1
2024-01-15 10:30:16 - protopred - DEBUG - Model validation passed
2024-01-15 10:30:16 - protopred - DEBUG - Auto-detected input type: SMILES_TEXT
2024-01-15 10:30:16 - protopred - DEBUG - Request prepared - Input type: SMILES_TEXT, Output type: JSON
2024-01-15 10:30:16 - protopred - DEBUG - Single SMILES input: CCCCC
2024-01-15 10:30:16 - protopred - INFO - API Request: POST https://protopred.protoqsar.com/API/v2/
2024-01-15 10:30:16 - protopred - DEBUG - Sending form data request
2024-01-15 10:30:18 - protopred - INFO - API Response: Status 200
2024-01-15 10:30:18 - protopred - DEBUG - Response size: 1542 bytes
2024-01-15 10:30:18 - protopred - DEBUG - Request completed successfully
2024-01-15 10:30:18 - protopred - INFO - Prediction completed successfully - JSON response received
2024-01-15 10:30:18 - protopred - DEBUG - Response contains 1 model results
```

## Log File Management

### Default Behavior
- **Default file**: `protopred_api.log` in current directory
- **Mode**: Append (new logs added to existing file)
- **Encoding**: UTF-8
- **Format**: Timestamp - Logger - Level - Message

### Custom File Locations
```python
# Absolute path
client = ProtoPREDClient(..., log_file="/var/log/protopred.log")

# Relative path
client = ProtoPREDClient(..., log_file="logs/my_session.log")

# Create directories automatically
client = ProtoPREDClient(..., log_file="data/2024/january/protopred.log")
```

### Log Rotation
For production use, consider implementing log rotation:

```python
import logging.handlers

# Manual log rotation setup (advanced)
from protopred.logging_config import ProtoPREDLogger

logger_instance = ProtoPREDLogger()
# Add rotating file handler
handler = logging.handlers.RotatingFileHandler(
    "protopred.log", 
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
logger_instance.logger.addHandler(handler)
```

## Best Practices

### Development
```python
# Use DEBUG level for detailed troubleshooting
client = ProtoPREDClient(..., log_level="DEBUG")
```

### Production
```python
# Use INFO level and disable console output
import os
os.environ['PROTOPRED_CONSOLE_LOG'] = 'false'

client = ProtoPREDClient(
    ...,
    log_file="/var/log/protopred/api.log",
    log_level="INFO"
)
```

### Monitoring
```python
# Monitor specific events
from protopred import get_logger

logger = get_logger()

# Add custom log entries
def my_analysis_function():
    logger.info("Starting custom analysis")
    # ... your code ...
    logger.info("Analysis completed")
```

## Security Considerations

### Sensitive Data Protection
The logger automatically filters sensitive information:
- ✅ **Logged**: Request parameters, molecule data, model names
- ❌ **Not Logged**: Account tokens, secret keys, passwords

### Log File Permissions
Ensure log files have appropriate permissions:
```bash
# Secure log file permissions
chmod 640 protopred_api.log
chown user:group protopred_api.log
```

## Troubleshooting

### Common Issues

**Problem**: No log file created
```python
# Solution: Check permissions and path
import os
log_path = "/path/to/logs"
os.makedirs(log_path, exist_ok=True)
client = ProtoPREDClient(..., log_file=f"{log_path}/protopred.log")
```

**Problem**: Too much/too little logging
```python
# Solution: Adjust log level
client = ProtoPREDClient(..., log_level="WARNING")  # Less verbose
client = ProtoPREDClient(..., log_level="DEBUG")    # More verbose
```

**Problem**: Console output interfering
```python
# Solution: Disable console logging
import os
os.environ['PROTOPRED_CONSOLE_LOG'] = 'false'
```

### Accessing Logger Directly
```python
from protopred import get_logger

logger = get_logger()
logger.info("Custom log message")
logger.error("Something went wrong")
```

## Integration Examples

### With Jupyter Notebooks
```python
# In Jupyter cells
from protopred import ProtoPREDClient

client = ProtoPREDClient(
    ...,
    log_file="notebook_session.log",
    log_level="INFO"
)

# Run your predictions - all logged to file
# Check log file for complete history
```

### With Web Applications
```python
# Flask/Django integration
import os
from protopred import configure_logging

# Configure once at application startup
configure_logging(
    log_file=os.path.join("logs", "protopred_webapp.log"),
    log_level="INFO"
)

# Use throughout application
def predict_for_user(user_id, smiles):
    client = ProtoPREDClient(...)
    # Automatically logs with user context
    return client.predict_single(smiles, ...)
```

### With Batch Processing
```python
# For batch jobs
from datetime import datetime

log_file = f"batch_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

client = ProtoPREDClient(
    ...,
    log_file=log_file,
    log_level="INFO"
)

# Process hundreds of molecules - all logged
for molecule_batch in batches:
    results = client.predict_batch(molecule_batch, ...)
```

The logging system provides complete visibility into your ProtoPRED API usage, making it easy to debug issues, monitor performance, and maintain audit trails.