"""
Observer for the Cognitive Agent

Interprets results and updates state based on observations.
"""

from typing import Dict, Any, Optional
import json

from agent.goals import Goal, GoalStatus
from utils.logger import logger
from utils.memory import memory


class Observer:
    """
    Observer: Interpret results and update state
    
    Observes the results of actions and updates the agent's understanding.
    """
    
    def __init__(self):
        self.observation_history = []
    
    async def observe(self, action: str, result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Observe the result of an action.
        
        Args:
            action: Action that was executed
            result: Result of the action
            context: Context in which action was executed
            
        Returns:
            Observation summary
        """
        logger.info(f"Observer: Observing result of action: {action}")
        
        observation = {
            "action": action,
            "result": result,
            "context": context,
            "timestamp": str(context.get("timestamp", "now")),
            "success": result.get("success", False)
        }
        
        self.observation_history.append(observation)
        
        # Store in episodic memory
        memory.store_episodic(
            event_type="agent_observation",
            data=observation,
            metadata={"layer": "observer"}
        )
        
        # Analyze the observation
        analysis = self._analyze_observation(observation)
        
        logger.info(f"Observer: Observation complete - Success: {observation['success']}")
        
        return {
            "observation": observation,
            "analysis": analysis
        }
    
    def _analyze_observation(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze an observation"""
        analysis = {
            "outcome": "success" if observation["success"] else "failure",
            "key_findings": [],
            "recommendations": []
        }
        
        result = observation["result"]
        
        if observation["success"]:
            analysis["key_findings"].append("Action executed successfully")
            if "result" in result:
                analysis["key_findings"].append(f"Result obtained: {str(result['result'])[:100]}")
        else:
            analysis["key_findings"].append("Action failed")
            if "error" in result:
                analysis["key_findings"].append(f"Error: {result['error']}")
                analysis["recommendations"].append("Consider alternative approach")
        
        return analysis
    
    def update_goal_progress(self, goal: Goal, observation: Dict[str, Any]) -> bool:
        """
        Update goal progress based on observation.
        
        Args:
            goal: Goal to update
            observation: Observation data
            
        Returns:
            True if goal was updated
        """
        if not observation["success"]:
            return False
        
        # Simple heuristic: increment progress on successful observation
        new_progress = min(1.0, goal.progress + 0.1)
        goal.update_progress(new_progress)
        
        if goal.progress >= 1.0:
            goal.set_status(GoalStatus.COMPLETED)
            logger.info(f"Observer: Goal {goal.id} completed")
        
        return True
    
    def get_observation_summary(self) -> Dict[str, Any]:
        """Get a summary of all observations"""
        total = len(self.observation_history)
        successful = sum(1 for o in self.observation_history if o["success"])
        
        return {
            "total_observations": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": successful / total if total > 0 else 0.0
        }
    
    def reset(self) -> None:
        """Reset observer state"""
        self.observation_history = []
        logger.info("Observer: Reset")
