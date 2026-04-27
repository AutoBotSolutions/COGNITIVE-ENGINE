"""
Meta-Cognition Layer

Governs thinking itself - determines when to continue thinking, when to stop,
confidence levels. Controls iteration depth, stopping conditions, confidence thresholds.
"""

from typing import Tuple

from models.state import ProblemState
from models.thought import ThoughtGraph
from llm.client import llm_client
from llm.prompts import PromptTemplates
from utils.logger import logger
from core.config import config


class MetaCognition:
    """
    Meta-Cognition Layer: Oversight
    
    Governs thinking itself - when to think, when to stop, confidence levels.
    """
    
    def __init__(self):
        self.use_llm = True
        self.min_iterations = config.min_iterations
        self.max_iterations = config.max_iterations
        self.early_stop_confidence = config.early_stop_confidence
    
    async def should_continue_thinking(self, state: ProblemState, thought_graph: ThoughtGraph, iteration: int) -> bool:
        """
        Determine if we should proceed to the generation phase.
        
        Args:
            state: Current problem state
            thought_graph: Current thought graph
            iteration: Current iteration number
            
        Returns:
            True if should continue, False otherwise
        """
        logger.log_layer("Meta-Cognition", "evaluating", f"Should continue to generation? Iteration: {iteration}")
        
        # Check if problem is well-defined
        if not state.is_well_defined():
            logger.log_layer("Meta-Cognition", "decision", "Stop - problem not well-defined")
            return False
        
        # Check minimum iterations
        if iteration < self.min_iterations:
            logger.log_layer("Meta-Cognition", "decision", f"Continue - below min iterations ({iteration} < {self.min_iterations})")
            return True
        
        logger.log_layer("Meta-Cognition", "decision", "Continue - problem well-defined")
        return True
    
    async def should_continue_deliberation(self, thought_graph: ThoughtGraph, state: ProblemState, iteration: int) -> Tuple[bool, str]:
        """
        Determine if we should continue deliberating.
        
        Args:
            thought_graph: Current thought graph
            state: Current problem state
            iteration: Current iteration number
            
        Returns:
            Tuple of (should_continue, reason)
        """
        logger.log_layer("Meta-Cognition", "evaluating", f"Should continue deliberation? Iteration: {iteration}")
        
        # Check maximum iterations
        if iteration >= self.max_iterations:
            reason = f"Reached maximum iterations ({self.max_iterations})"
            logger.log_layer("Meta-Cognition", "decision", f"Stop - {reason}")
            return False, reason
        
        # Check if we have a high-confidence thought
        top_thoughts = thought_graph.get_top_scoring_thoughts(1)
        if top_thoughts:
            best_thought = top_thoughts[0]
            if best_thought.confidence >= self.early_stop_confidence and iteration >= self.min_iterations:
                reason = f"High confidence reached ({best_thought.confidence:.2f} >= {self.early_stop_confidence})"
                logger.log_layer("Meta-Cognition", "decision", f"Stop - {reason}")
                return False, reason
        
        # Check if we have accepted thoughts
        from models.thought import ThoughtStatus
        accepted = [t for t in thought_graph.thoughts.values() if t.status == ThoughtStatus.ACCEPTED]
        
        if accepted and iteration >= self.min_iterations:
            # We have accepted thoughts and met minimum iterations - stop and commit
            reason = f"Have {len(accepted)} accepted thought(s), ready to commit"
            logger.log_layer("Meta-Cognition", "decision", f"Stop - {reason}")
            return False, reason
        
        if not accepted and iteration > 0:
            # Continue to try to generate better thoughts
            reason = "No accepted thoughts yet, continue deliberating"
            logger.log_layer("Meta-Cognition", "decision", f"Continue - {reason}")
            return True, reason
        
        # LLM-based decision if available
        if self.use_llm:
            should_continue, llm_reason = await self._llm_should_continue(thought_graph, state, iteration)
            if not should_continue:
                return False, llm_reason
        
        reason = "Continue deliberation"
        logger.log_layer("Meta-Cognition", "decision", f"Continue - {reason}")
        return True, reason
    
    async def _llm_should_continue(self, thought_graph: ThoughtGraph, state: ProblemState, iteration: int) -> Tuple[bool, str]:
        """Use LLM to decide if deliberation should continue"""
        top_thoughts = thought_graph.get_top_scoring_thoughts(3)
        best_score = top_thoughts[0].score if top_thoughts else 0.0
        best_confidence = top_thoughts[0].confidence if top_thoughts else 0.0
        
        prompt = PromptTemplates.format_template(
            "META_SHOULD_CONTINUE",
            iteration=iteration,
            thought_count=len(thought_graph.thoughts),
            best_score=best_score,
            confidence=best_confidence,
            clarity=state.clarity_score,
            completeness=state.completeness_score
        )
        
        response = await llm_client.generate(prompt)
        
        # Parse the response
        if "NO" in response.upper():
            reason = self._extract_reason(response)
            return False, reason
        else:
            return True, "LLM recommends continue"
    
    def _extract_reason(self, text: str) -> str:
        """Extract the reason from an LLM response"""
        # Look for "Reason:" pattern
        if "reason:" in text.lower():
            parts = text.split("reason:", 1)
            if len(parts) > 1:
                return parts[1].strip()
        return "LLM decision"
    
    async def get_stop_reason(self, thought_graph: ThoughtGraph, state: ProblemState) -> str:
        """
        Get a detailed explanation of why thinking should stop.
        
        Args:
            thought_graph: Current thought graph
            state: Current problem state
            
        Returns:
            Explanation string
        """
        logger.log_layer("Meta-Cognition", "explaining", "Generating stop reason")
        
        top_thoughts = thought_graph.get_top_scoring_thoughts(3)
        state_summary = {
            "thought_count": len(thought_graph.thoughts),
            "best_score": top_thoughts[0].score if top_thoughts else 0.0,
            "best_confidence": top_thoughts[0].confidence if top_thoughts else 0.0,
            "clarity": state.clarity_score,
            "completeness": state.completeness_score
        }
        
        prompt = PromptTemplates.format_template(
            "META_STOP_REASON",
            state=state_summary
        )
        
        response = await llm_client.generate(prompt)
        
        return response
    
    def adjust_confidence_threshold(self, current_threshold: float, performance_history: list) -> float:
        """
        Adjust confidence threshold based on historical performance.
        
        Args:
            current_threshold: Current confidence threshold
            performance_history: List of past performance metrics
            
        Returns:
            Adjusted threshold
        """
        if not performance_history:
            return current_threshold
        
        # Calculate average performance
        avg_performance = sum(performance_history) / len(performance_history)
        
        # Adjust threshold based on performance
        if avg_performance > 0.8:
            # Good performance, can be more selective
            return min(0.95, current_threshold + 0.05)
        elif avg_performance < 0.5:
            # Poor performance, be less selective
            return max(0.5, current_threshold - 0.05)
        
        return current_threshold
    
    def calculate_optimal_iterations(self, problem_complexity: float) -> int:
        """
        Calculate optimal number of iterations based on problem complexity.
        
        Args:
            problem_complexity: Complexity score (0-1)
            
        Returns:
            Optimal iteration count
        """
        base_iterations = self.min_iterations
        additional_iterations = int(problem_complexity * (self.max_iterations - self.min_iterations))
        
        return min(self.max_iterations, base_iterations + additional_iterations)
