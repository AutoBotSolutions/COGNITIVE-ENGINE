"""
CogChat Configuration

Configuration settings for the Cognitive Engine chat interface.
"""

from typing import Optional
from pydantic import BaseSettings


class CogChatConfig(BaseSettings):
    """Configuration for CogChat"""
    
    # Server settings
    host: str = "localhost"
    port: int = 8888
    debug: bool = False
    
    # Session settings
    max_sessions: int = 100
    session_timeout_minutes: int = 60
    max_messages_per_session: int = 1000
    
    # Cognitive Engine settings
    include_trace_by_default: bool = False
    show_cognitive_layers: bool = True
    show_thought_count: bool = True
    
    # UI settings
    theme: str = "dark"
    max_response_length: int = 2000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global config instance
cogchat_config = CogChatConfig()
