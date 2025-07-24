"""Logging configuration for ProtoPRED API client"""

import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Optional


class ProtoPREDLogger:
    """Centralized logging configuration for ProtoPRED API client"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self, log_file: Optional[str] = None, log_level: str = "INFO"):
        """Setup logger with file and console handlers"""
        
        # Create logger
        self._logger = logging.getLogger("protopred")
        self._logger.setLevel(getattr(logging, log_level.upper()))
        
        # Avoid duplicate handlers
        if self._logger.handlers:
            return
        
        # Create formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Set default log file path
        if log_file is None:
            log_file = os.getenv('PROTOPRED_LOG_FILE', 'protopred_api.log')
        
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # File handler (append mode)
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
        
        # Console handler (optional, controlled by environment variable)
        if os.getenv('PROTOPRED_CONSOLE_LOG', 'true').lower() == 'true':
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, log_level.upper()))
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)
        
        # Log initial setup
        self._logger.info(f"ProtoPRED logging initialized - Log file: {log_file}")
    
    @property
    def logger(self):
        """Get the configured logger instance"""
        return self._logger
    
    def configure(self, log_file: str = None, log_level: str = "INFO"):
        """Reconfigure logging with new settings"""
        # Clear existing handlers
        if self._logger:
            for handler in self._logger.handlers[:]:
                self._logger.removeHandler(handler)
                handler.close()
        
        # Reset logger
        self._logger = None
        self._setup_logger(log_file, log_level)
    
    def log_api_request(self, method: str, url: str, data: dict = None):
        """Log API request details"""
        self._logger.info(f"API Request: {method} {url}")
        if data:
            # Log safe parameters (exclude sensitive data)
            safe_data = {k: v for k, v in data.items() 
                        if k not in ['account_token', 'account_secret_key']}
            if safe_data:
                self._logger.debug(f"Request data: {safe_data}")
    
    def log_api_response(self, status_code: int, response_size: int = None):
        """Log API response details"""
        self._logger.info(f"API Response: Status {status_code}")
        if response_size:
            self._logger.debug(f"Response size: {response_size} bytes")
    
    def log_prediction_summary(self, module: str, models: str, num_molecules: int):
        """Log prediction job summary"""
        self._logger.info(f"Prediction job - Module: {module}, Models: {models}, Molecules: {num_molecules}")
    
    def log_error(self, error: Exception, context: str = ""):
        """Log error with context"""
        if context:
            self._logger.error(f"{context}: {type(error).__name__}: {str(error)}")
        else:
            self._logger.error(f"{type(error).__name__}: {str(error)}")


# Global logger instance
def get_logger():
    """Get the global ProtoPRED logger instance"""
    return ProtoPREDLogger().logger


def configure_logging(log_file: str = None, log_level: str = "INFO"):
    """Configure ProtoPRED logging globally"""
    ProtoPREDLogger().configure(log_file, log_level)