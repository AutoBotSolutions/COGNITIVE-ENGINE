"""
Code Execution Tool for the Cognitive Agent

Provides safe code execution capabilities.
"""

from typing import Dict, Any
import asyncio
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from tools.registry import Tool


class CodeExecutionTool(Tool):
    """
    Code execution tool for running Python code safely.
    """
    
    def __init__(self):
        super().__init__(
            name="code_exec",
            description="Execute Python code"
        )
        self.max_execution_time = 5  # seconds
    
    async def execute(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Python code.
        
        Args:
            action: Python code to execute
            context: Execution context
            
        Returns:
            Execution results
        """
        try:
            # Capture stdout and stderr
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            # Execute with timeout
            result = await asyncio.wait_for(
                self._execute_code(action, stdout_capture, stderr_capture),
                timeout=self.max_execution_time
            )
            
            stdout = stdout_capture.getvalue()
            stderr = stderr_capture.getvalue()
            
            return {
                "success": True,
                "stdout": stdout,
                "stderr": stderr,
                "result": result
            }
            
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": f"Code execution timed out (max {self.max_execution_time}s)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _execute_code(self, code: str, stdout_capture, stderr_capture) -> Any:
        """Execute code in a safe context"""
        # Create a restricted globals dict
        safe_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'range': range,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'sum': sum,
                'max': max,
                'min': min,
                'abs': abs,
                'round': round,
                'any': any,
                'all': all,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
            }
        }
        
        # Execute the code
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(code, safe_globals)
        
        # Return the last expression if it was assigned to a variable named 'result'
        return safe_globals.get('result', None)
    
    def validate_action(self, action: str) -> bool:
        """Validate if action is valid Python code"""
        # Basic validation: check for dangerous operations
        dangerous_keywords = ['import', 'exec', 'eval', 'open', 'file', '__import__']
        
        for keyword in dangerous_keywords:
            if keyword in action:
                return False
        
        return len(action) > 0 and len(action) < 10000
