"""
Planner for the Cognitive Agent

Converts goals into actionable plans using the cognitive engine.
"""

from typing import List, Dict, Any, Optional
import re

from agent.goals import Goal
from llm.client import llm_client
from llm.prompts import PromptTemplates
from utils.logger import logger
from core.config import config


class PlanStep:
    """Represents a single step in a plan"""
    
    def __init__(self, action: str, tool: Optional[str] = None, reasoning: str = ""):
        self.action = action
        self.tool = tool
        self.reasoning = reasoning
        self.completed = False
        self.result: Optional[Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "tool": self.tool,
            "reasoning": self.reasoning,
            "completed": self.completed,
            "result": str(self.result) if self.result else None
        }


class Planner:
    """
    Planner: Goal → Plan conversion
    
    Creates actionable plans from goals using LLM-driven planning.
    """
    
    def __init__(self):
        self.use_llm = True
    
    async def create_plan(self, goal: Goal, current_state: Dict[str, Any], available_tools: List[str]) -> List[PlanStep]:
        """
        Create a plan to achieve a goal.
        
        Args:
            goal: Goal to achieve
            current_state: Current state of the agent/environment
            available_tools: List of available tool names
            
        Returns:
            List of plan steps
        """
        logger.info(f"Planner: Creating plan for goal: {goal.description}")
        
        if self.use_llm:
            plan = await self._deliberative_plan(goal, current_state, available_tools)
        else:
            plan = self._rule_based_plan(goal, current_state, available_tools)
        
        logger.info(f"Planner: Created plan with {len(plan)} steps")
        
        return plan
    
    async def _deliberative_plan(self, goal: Goal, current_state: Dict[str, Any], available_tools: List[str]) -> List[PlanStep]:
        """
        Generate multiple plans and evaluate them through deliberation.
        
        This is the deliberative planning approach that generates multiple
        alternative plans, evaluates them, and selects the best one.
        """
        from core.engine import CognitiveEngine
        
        logger.info("Planner: Generating multiple alternative plans")
        
        # Generate 3 alternative plans
        num_alternatives = 3
        alternative_plans = []
        
        for i in range(num_alternatives):
            prompt = PromptTemplates.format_template(
                "AGENT_PLAN",
                goal=goal.description,
                current_state=str(current_state),
                tools=", ".join(available_tools),
                variant=f"Alternative {i+1}"
            )
            
            response = await llm_client.generate(prompt)
            plan = self._parse_plan_response(response)
            alternative_plans.append(plan)
        
        logger.info(f"Planner: Generated {len(alternative_plans)} alternative plans")
        
        # Evaluate plans through cognitive engine
        best_plan = await self._evaluate_plans(goal, alternative_plans, current_state)
        
        logger.info(f"Planner: Selected best plan with {len(best_plan)} steps")
        
        return best_plan
    
    async def _evaluate_plans(self, goal: Goal, plans: List[List[PlanStep]], current_state: Dict[str, Any]) -> List[PlanStep]:
        """
        Evaluate multiple plans through deliberation and select the best one.
        
        Uses the cognitive engine to evaluate each plan's quality.
        """
        from core.engine import CognitiveEngine
        
        engine = CognitiveEngine()
        engine.initialize_layers()
        
        best_plan = plans[0]
        best_score = 0.0
        
        for i, plan in enumerate(plans):
            # Create a prompt for evaluation
            plan_summary = "\n".join([
                f"Step {j+1}: {step.action} (tool: {step.tool}) - {step.reasoning}"
                for j, step in enumerate(plan)
            ])
            
            evaluation_prompt = f"""
Evaluate this plan for the goal: {goal.description}

Plan:
{plan_summary}

Current context: {current_state}

Evaluate the plan on:
1. Clarity and specificity
2. Feasibility with available tools
3. Likelihood of achieving the goal
4. Efficiency (number of steps)

Provide a score from 0.0 to 1.0 and a brief justification.
"""
            
            result = await engine.process(evaluation_prompt)
            
            # Extract score from result
            if result.get("success"):
                output = result.get("output", "")
                # Try to extract a score from the output
                import re
                score_match = re.search(r'(\d+\.?\d*)', output)
                if score_match:
                    score = float(score_match.group(1))
                    # Normalize to 0-1 range
                    score = min(1.0, score / 10.0) if score > 1 else score
                else:
                    score = 0.5  # Default score if no number found
                
                logger.info(f"Planner: Plan {i+1} score: {score}")
                
                if score > best_score:
                    best_score = score
                    best_plan = plan
            else:
                logger.warning(f"Planner: Plan {i+1} evaluation failed")
        
        return best_plan
    
    async def _llm_plan(self, goal: Goal, current_state: Dict[str, Any], available_tools: List[str]) -> List[PlanStep]:
        """Use LLM to create a plan"""
        prompt = PromptTemplates.format_template(
            "AGENT_PLAN",
            goal=goal.description,
            current_state=str(current_state),
            tools=", ".join(available_tools)
        )
        
        response = await llm_client.generate(prompt)
        
        return self._parse_plan_response(response)
    
    def _rule_based_plan(self, goal: Goal, current_state: Dict[str, Any], available_tools: List[str]) -> List[PlanStep]:
        """Rule-based planning (fallback)"""
        steps = []
        
        # Simple heuristic: if goal mentions "search", add web search step
        if "search" in goal.description.lower() and "web_search" in available_tools:
            steps.append(PlanStep(
                action="Search for information",
                tool="web_search",
                reasoning="Goal requires information search"
            ))
        
        # If goal mentions "code" or "execute", add code execution step
        if "code" in goal.description.lower() or "execute" in goal.description.lower():
            if "code_exec" in available_tools:
                steps.append(PlanStep(
                    action="Execute code",
                    tool="code_exec",
                    reasoning="Goal requires code execution"
                ))
        
        # Add a final step to verify goal completion
        steps.append(PlanStep(
            action="Verify goal completion",
            tool=None,
            reasoning="Verify that the goal has been achieved"
        ))
        
        return steps
    
    def _parse_plan_response(self, response: str) -> List[PlanStep]:
        """Parse LLM response into plan steps"""
        steps = []
        
        # Pattern: "Step N: [action] - [tool] - [reasoning]"
        pattern = r'Step\s+(\d+):\s*(.+?)\s*-\s*(.+?)\s*-\s*(.+?)(?=Step\s+\d+:|$)'
        matches = re.findall(pattern, response, re.DOTALL)
        
        for match in matches:
            step_num, action, tool, reasoning = match
            step = PlanStep(
                action=action.strip(),
                tool=tool.strip() if tool.strip() != "none" else None,
                reasoning=reasoning.strip()
            )
            steps.append(step)
        
        # If parsing failed, create a single step from the response
        if not steps:
            step = PlanStep(
                action=response.strip()[:200],
                tool=None,
                reasoning="Parsed from full response"
            )
            steps.append(step)
        
        return steps
    
    async def revise_plan(self, current_plan: List[PlanStep], execution_feedback: str) -> List[PlanStep]:
        """
        Revise a plan based on execution feedback.
        
        Args:
            current_plan: Current plan steps
            execution_feedback: Feedback from plan execution
            
        Returns:
            Revised plan steps
        """
        logger.info("Planner: Revising plan based on feedback")
        
        # Simple revision: remove completed steps and add new steps based on feedback
        remaining_steps = [s for s in current_plan if not s.completed]
        
        # If feedback indicates a step failed, try to add an alternative
        if "failed" in execution_feedback.lower():
            failed_step = next((s for s in current_plan if not s.completed), None)
            if failed_step:
                alternative = PlanStep(
                    action=f"Alternative: {failed_step.action}",
                    tool=failed_step.tool,
                    reasoning="Original step failed, trying alternative approach"
                )
                remaining_steps.insert(0, alternative)
        
        return remaining_steps
    
    def get_plan_summary(self, plan: List[PlanStep]) -> Dict[str, Any]:
        """Get a summary of the plan"""
        completed = sum(1 for s in plan if s.completed)
        total = len(plan)
        
        return {
            "total_steps": total,
            "completed_steps": completed,
            "remaining_steps": total - completed,
            "progress": completed / total if total > 0 else 0.0,
            "steps": [s.to_dict() for s in plan]
        }
