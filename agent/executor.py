"""
Executor for the Cognitive Agent

Executes actions and uses tools to achieve goals.
"""

from typing import Dict, Any, Optional
import asyncio

from agent.planner import PlanStep
from tools.registry import ToolRegistry
from utils.logger import logger
from core.config import config


class Executor:
    """
    Executor: Execute actions/tools
    
    Executes planned actions using available tools.
    """
    
    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.step_count = 0
        self.max_steps = config.max_agent_steps
    
    async def execute_step(self, step: PlanStep, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single plan step.
        
        Args:
            step: Plan step to execute
            context: Current execution context
            
        Returns:
            Execution result
        """
        logger.info(f"Executor: Executing step: {step.action}")
        
        self.step_count += 1
        
        if self.step_count > self.max_steps:
            logger.warning(f"Executor: Reached max steps ({self.max_steps})")
            return {
                "success": False,
                "error": f"Maximum step limit ({self.max_steps}) reached",
                "step_count": self.step_count
            }
        
        try:
            if step.tool:
                # Execute using tool
                result = await self._execute_tool(step.tool, step.action, context)
            else:
                # Execute as a direct action (cognitive processing)
                result = await self._execute_direct_action(step.action, context)
            
            step.completed = True
            step.result = result
            
            logger.info(f"Executor: Step completed successfully")
            
            return {
                "success": True,
                "result": result,
                "step_count": self.step_count
            }
            
        except Exception as e:
            logger.error(f"Executor: Step execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "step_count": self.step_count
            }
    
    async def _execute_tool(self, tool_name: str, action: str, context: Dict[str, Any]) -> Any:
        """Execute an action using a specific tool"""
        tool = self.tool_registry.get_tool(tool_name)
        
        if not tool:
            raise ValueError(f"Tool not found: {tool_name}")
        
        # Execute the tool
        result = await tool.execute(action, context)
        
        return result
    
    async def _execute_direct_action(self, action: str, context: Dict[str, Any]) -> Any:
        """Execute a direct action without a tool"""
        # For now, just return the action as a result
        # In a full implementation, this might use the cognitive engine
        return {
            "action": action,
            "message": "Action executed (direct mode)",
            "context": context
        }
    
    async def execute_plan(self, plan_steps: list, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an entire plan step by step.
        
        Args:
            plan_steps: List of plan steps
            context: Current execution context
            
        Returns:
            Overall execution result
        """
        logger.info(f"Executor: Executing plan with {len(plan_steps)} steps")
        
        results = []
        
        for step in plan_steps:
            if step.completed:
                continue
            
            result = await self.execute_step(step, context)
            results.append(result)
            
            # Stop if step failed
            if not result["success"]:
                logger.warning(f"Executor: Plan execution stopped due to failure")
                break
            
            # Update context with result
            context["last_result"] = result
        
        # Calculate overall success
        success_count = sum(1 for r in results if r["success"])
        overall_success = success_count == len(results)
        
        return {
            "success": overall_success,
            "steps_executed": len(results),
            "steps_succeeded": success_count,
            "results": results,
            "final_context": context
        }
    
    def reset(self) -> None:
        """Reset executor state"""
        self.step_count = 0
        logger.info("Executor: Reset")
