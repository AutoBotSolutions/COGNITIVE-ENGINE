"""
Configuration and tunable parameters for the Cognitive Engine
"""

from typing import Optional
import os


class CognitiveEngineConfig:
    """Configuration settings for the Cognitive Engine"""
    
    def __init__(self):
        # LLM Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.default_llm_provider = os.getenv("DEFAULT_LLM_PROVIDER", "custom")  # or "anthropic" or "openai"
        self.default_model = os.getenv("DEFAULT_MODEL", "gpt-4")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        
        # Custom Provider Configuration
        self.enable_custom_provider = os.getenv("ENABLE_CUSTOM_PROVIDER", "true").lower() == "true"
        self.custom_api_endpoint = os.getenv("CUSTOM_API_ENDPOINT")
        self.custom_api_key = os.getenv("CUSTOM_API_KEY")
        
        # Cognitive Layer Configuration
        self.max_thoughts_per_generation = int(os.getenv("MAX_THOUGHTS_PER_GENERATION", "5"))
        self.max_deliberation_iterations = int(os.getenv("MAX_DELIBERATION_ITERATIONS", "3"))
        self.confidence_threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
        self.score_threshold = float(os.getenv("SCORE_THRESHOLD", "0.5"))
        
        # Meta-Cognition Configuration
        self.min_iterations = int(os.getenv("MIN_ITERATIONS", "1"))
        self.max_iterations = int(os.getenv("MAX_ITERATIONS", "10"))
        self.early_stop_confidence = float(os.getenv("EARLY_STOP_CONFIDENCE", "0.95"))
        
        # Memory Configuration
        self.memory_backend = os.getenv("MEMORY_BACKEND", "sqlite")  # or "redis", "postgres"
        self.memory_path = os.getenv("MEMORY_PATH", "cognitive_engine.db")
        self.max_memory_entries = int(os.getenv("MAX_MEMORY_ENTRIES", "10000"))
        
        # Agent Configuration
        self.max_agent_steps = int(os.getenv("MAX_AGENT_STEPS", "50"))
        self.agent_timeout_seconds = int(os.getenv("AGENT_TIMEOUT_SECONDS", "300"))
        
        # Learning Configuration
        self.pattern_extraction_interval = int(os.getenv("PATTERN_EXTRACTION_INTERVAL", "100"))  # Run every N thoughts
        self.pattern_confidence_threshold = float(os.getenv("PATTERN_CONFIDENCE_THRESHOLD", "0.8"))
        
        # Prompt Evolution Configuration
        self.enable_prompt_evolution = os.getenv("ENABLE_PROMPT_EVOLUTION", "false").lower() == "true"
        self.prompt_evolution_interval = int(os.getenv("PROMPT_EVOLUTION_INTERVAL", "1000"))
        self.mutation_rate = float(os.getenv("MUTATION_RATE", "0.1"))
        
        # Dashboard Configuration
        self.enable_dashboard = os.getenv("ENABLE_DASHBOARD", "true").lower() == "true"
        self.dashboard_host = os.getenv("DASHBOARD_HOST", "localhost")
        self.dashboard_port = int(os.getenv("DASHBOARD_PORT", "8000"))
        
        # Logging Configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "cognitive_engine.log")


# Global config instance
config = CognitiveEngineConfig()
