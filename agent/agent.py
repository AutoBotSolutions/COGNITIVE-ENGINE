"""
Main Autonomous Agent for the Cognitive Engine

Implements the Think → Plan → Act → Observe → Reflect → Repeat loop.
"""

from typing import Dict, Any, Optional
import asyncio

from agent.goals import Goal, GoalManager, GoalPriority, GoalStatus
from agent.planner import Planner
from agent.executor import Executor
from agent.observer import Observer
from core.engine import CognitiveEngine
from utils.logger import logger
from core.config import config


class CognitiveAgent:
    """
    Autonomous Agent with internal deliberation.
    
    Core Loop: Think → Plan → Act → Observe → Reflect → Repeat
    """
    
    def __init__(self):
        self.cognitive_engine = CognitiveEngine()
        self.cognitive_engine.initialize_layers()
        
        self.goal_manager = GoalManager()
        self.planner = Planner()
        self.executor = Executor()
        self.observer = Observer()
        
        self.current_context: Dict[str, Any] = {}
        self.is_running = False
    
    async def set_goal(self, description: str, priority: GoalPriority = GoalPriority.MEDIUM) -> str:
        """
        Set a goal for the agent.
        
        Args:
            description: Goal description
            priority: Goal priority
            
        Returns:
            Goal ID
        """
        goal = Goal(description=description, priority=priority)
        goal_id = self.goal_manager.add_goal(goal)
        
        logger.info(f"Agent: Set goal {goal_id}: {description}")
        
        return goal_id
    
    async def think(self, query: str) -> Dict[str, Any]:
        """
        Think phase: Use cognitive engine to process a query.
        
        Args:
            query: Query to think about
            
        Returns:
            Result from cognitive engine
        """
        logger.info(f"Agent: Thinking about: {query}")
        
        result = await self.cognitive_engine.process(query)
        
        self.current_context["last_thought_result"] = result
        
        return result
    
    async def plan(self, goal: Goal) -> list:
        """
        Plan phase: Create a plan to achieve the goal.
        
        Args:
            goal: Goal to plan for
            
        Returns:
            Plan steps
        """
        logger.info(f"Agent: Planning for goal: {goal.description}")
        
        available_tools = self.executor.tool_registry.list_tools()
        plan_steps = await self.planner.create_plan(goal, self.current_context, available_tools)
        
        self.current_context["current_plan"] = plan_steps
        
        return plan_steps
    
    async def act(self, plan_steps: list) -> Dict[str, Any]:
        """
        Act phase: Execute the plan.
        
        Args:
            plan_steps: Plan steps to execute
            
        Returns:
            Execution result
        """
        logger.info(f"Agent: Acting on plan with {len(plan_steps)} steps")
        
        result = await self.executor.execute_plan(plan_steps, self.current_context)
        
        self.current_context["last_execution_result"] = result
        
        return result
    
    async def observe(self, action: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Observe phase: Observe the results of actions.
        
        Args:
            action: Action that was executed
            result: Result of the action
            
        Returns:
            Observation summary
        """
        logger.info(f"Agent: Observing results")
        
        observation = await self.observer.observe(action, result, self.current_context)
        
        self.current_context["last_observation"] = observation
        
        return observation
    
    async def reflect(self, goal: Goal, observation: Dict[str, Any]) -> str:
        """
        Reflect phase: Reflect on the observation and update understanding.
        
        Args:
            goal: Current goal
            observation: Observation to reflect on
            
        Returns:
            Reflection summary
        """
        logger.info(f"Agent: Reflecting on observation")
        
        # Update goal progress based on observation
        self.observer.update_goal_progress(goal, observation["observation"])
        
        # Use cognitive engine for deeper reflection
        reflection_prompt = f"Reflect on this action and result:\nAction: {observation['observation']['action']}\nResult: {observation['observation']['result']}\nGoal: {goal.description}"
        
        reflection_result = await self.cognitive_engine.process(reflection_prompt)
        
        self.current_context["last_reflection"] = reflection_result
        
        return reflection_result.get("output", "Reflection complete")
    
    async def run_cycle(self, goal_id: str) -> Dict[str, Any]:
        """
        Run a single Think-Plan-Act-Observe-Reflect cycle.
        
        Args:
            goal_id: ID of the goal to work on
            
        Returns:
            Cycle result
        """
        goal = self.goal_manager.get_goal(goal_id)
        if not goal:
            return {"success": False, "error": "Goal not found"}
        
        logger.info(f"Agent: Running cycle for goal {goal_id}")
        
        # Think
        think_result = await self.think(goal.description)
        
        # Update goal status to in_progress
        if goal.status == GoalStatus.PENDING:
            goal.set_status(GoalStatus.IN_PROGRESS)
        
        # Plan
        plan_steps = await self.plan(goal)
        
        # Act
        act_result = await self.act(plan_steps)
        
        # Integrate tool results into context
        if act_result.get("success") and act_result.get("results"):
            tool_results = act_result.get("results", [])
            if tool_results:
                last_result = tool_results[-1]
                if last_result.get("result"):
                    self.current_context["tool_outputs"] = self.current_context.get("tool_outputs", [])
                    self.current_context["tool_outputs"].append(last_result["result"])
                    logger.info(f"Agent: Tool output integrated into context")
        
        # Observe (observe the last action)
        last_action = plan_steps[-1].action if plan_steps else "unknown"
        observation = await self.observe(last_action, act_result)
        
        # Reflect
        reflection = await self.reflect(goal, observation)
        
        # Update goal progress based on observation
        if observation.get("observation", {}).get("success"):
            goal.update_progress(min(1.0, goal.progress + 0.2))
        
        # Check if goal is complete
        is_complete = goal.status == GoalStatus.COMPLETED
        
        return {
            "success": True,
            "goal_id": goal_id,
            "goal_complete": is_complete,
            "think_result": think_result,
            "plan_steps": len(plan_steps),
            "act_result": act_result["success"],
            "observation": observation["observation"]["success"],
            "reflection": reflection[:200] if reflection else "",
            "goal_progress": goal.progress
        }
    
    async def run_autonomous(self, goal_id: str, max_cycles: int = 10) -> Dict[str, Any]:
        """
        Run autonomous cycles until goal is complete or max cycles reached.
        
        Args:
            goal_id: ID of the goal to work on
            max_cycles: Maximum number of cycles to run
            
        Returns:
            Overall result
        """
        logger.info(f"Agent: Starting autonomous run for goal {goal_id} (max {max_cycles} cycles)")
        
        self.is_running = True
        cycles_completed = 0
        
        for cycle in range(max_cycles):
            if not self.is_running:
                logger.info("Agent: Autonomous run stopped")
                break
            
            cycle_result = await self.run_cycle(goal_id)
            cycles_completed += 1
            
            if cycle_result["goal_complete"]:
                logger.info(f"Agent: Goal completed in {cycles_completed} cycles")
                break
        
        goal = self.goal_manager.get_goal(goal_id)
        
        return {
            "success": goal.status == GoalStatus.COMPLETED if goal else False,
            "cycles_completed": cycles_completed,
            "goal_status": goal.status.value if goal else "unknown",
            "goal_progress": goal.progress if goal else 0.0
        }
    
    def stop(self) -> None:
        """Stop autonomous execution"""
        self.is_running = False
        logger.info("Agent: Stop requested")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "is_running": self.is_running,
            "goals": self.goal_manager.get_goal_statistics(),
            "executor_step_count": self.executor.step_count,
            "observer_summary": self.observer.get_observation_summary()
        }
    
    def reset(self) -> None:
        """Reset agent state"""
        self.goal_manager = GoalManager()
        self.executor.reset()
        self.observer.reset()
        self.current_context = {}
        self.is_running = False
        logger.info("Agent: Reset")
