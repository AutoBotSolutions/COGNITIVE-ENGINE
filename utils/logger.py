"""
Logging utilities for the Cognitive Engine

Provides structured logging with color support for console output.
"""

import logging
import sys
from typing import Optional
from pathlib import Path
from datetime import datetime

from core.config import config


class CognitiveEngineLogger:
    """Custom logger for the Cognitive Engine"""
    
    def __init__(self, name: str = "cognitive_engine"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, config.log_level.upper()))
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Console handler with color
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, config.log_level.upper()))
        
        # File handler if configured
        if config.log_file:
            Path(config.log_file).parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(config.log_file)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        
        # Console formatter
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, extra=kwargs)
    
    def log_thought(self, thought_id: str, action: str, details: str):
        """Log a thought-related event"""
        self.info(f"Thought {thought_id}: {action} - {details}")
    
    def log_layer(self, layer: str, action: str, details: str):
        """Log a cognitive layer event"""
        self.info(f"[{layer}] {action}: {details}")
    
    def log_memory(self, memory_type: str, action: str, details: str):
        """Log a memory-related event"""
        self.debug(f"[Memory:{memory_type}] {action}: {details}")


# Singleton logger instance
logger = CognitiveEngineLogger()
