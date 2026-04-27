"""
Core modules for the Cognitive Engine
"""

from .config import config, CognitiveEngineConfig
from .engine import CognitiveEngine, engine

__all__ = [
    'config',
    'CognitiveEngineConfig',
    'CognitiveEngine',
    'engine'
]
