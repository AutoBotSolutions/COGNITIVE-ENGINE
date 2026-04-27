"""
Tools for the Cognitive Agent
"""

from .registry import ToolRegistry, Tool
from .web_search import WebSearchTool
from .code_exec import CodeExecutionTool

__all__ = [
    'ToolRegistry',
    'Tool',
    'WebSearchTool',
    'CodeExecutionTool'
]
