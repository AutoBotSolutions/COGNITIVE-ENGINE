"""
Tool Registry for the Cognitive Agent

Manages available tools that the agent can use.
"""

from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import asyncio


class Tool(ABC):
    """Abstract base class for tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, action: str, context: Dict[str, Any]) -> Any:
        """Execute the tool"""
        pass
    
    @abstractmethod
    def validate_action(self, action: str) -> bool:
        """Validate if an action is appropriate for this tool"""
        pass


class ToolRegistry:
    """
    Registry for managing available tools.
    """
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()
    
    def register_tool(self, tool: Tool) -> None:
        """Register a tool"""
        self.tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all available tool names"""
        return list(self.tools.keys())
    
    def get_tool_descriptions(self) -> Dict[str, str]:
        """Get descriptions of all tools"""
        return {name: tool.description for name, tool in self.tools.items()}
    
    def _register_default_tools(self) -> None:
        """Register default tools"""
        from tools.web_search import WebSearchTool
        from tools.code_exec import CodeExecutionTool
        
        self.register_tool(WebSearchTool())
        self.register_tool(CodeExecutionTool())
