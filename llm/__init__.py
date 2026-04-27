"""
LLM integration for the Cognitive Engine
"""

from .client import LLMClient, llm_client, OpenAIProvider, AnthropicProvider
from .prompts import PromptTemplates

__all__ = [
    'LLMClient',
    'llm_client',
    'OpenAIProvider',
    'AnthropicProvider',
    'PromptTemplates'
]
