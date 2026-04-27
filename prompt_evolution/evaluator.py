"""
Prompt Evaluator for the Prompt Evolution System

Evaluates prompt performance and scores improvements.
"""

from typing import Dict, Any, List
import asyncio

from prompt_evolution.prompt_store import PromptStore
from prompt_evolution.tester import PromptTester
from utils.logger import logger


class PromptEvaluator:
    """
    Evaluates prompt performance and determines if improvements should be adopted.
    """
    
    def __init__(self, prompt_store: PromptStore):
        self.prompt_store = prompt_store
        self.tester = PromptTester(prompt_store)
        self.baseline_threshold = 0.05  # 5% improvement required
    
    async def evaluate_proposal(
        self,
        layer_name: str,
        proposed_prompt: str
    ) -> Dict[str, Any]:
        """
        Evaluate a proposed prompt improvement.
        
        Args:
            layer_name: Name of the layer
            proposed_prompt: Proposed improved prompt
            
        Returns:
            Evaluation results
        """
        logger.info(f"PromptEvaluator: Evaluating proposal for {layer_name}")
        
        # Get current prompt
        current_prompt = self.prompt_store.get_current_prompt(layer_name)
        if not current_prompt:
            return {
                "should_adopt": False,
                "reason": "No current prompt to compare against"
            }
        
        # A/B test
        comparison = await self.tester.ab_test(layer_name, current_prompt, proposed_prompt)
        
        # Determine if should adopt
        should_adopt, reason = self._should_adopt(comparison)
        
        evaluation = {
            "layer_name": layer_name,
            "should_adopt": should_adopt,
            "reason": reason,
            "comparison": comparison,
            "improvement_metrics": self._calculate_improvement(comparison)
        }
        
        logger.info(f"PromptEvaluator: Evaluation complete - Should adopt: {should_adopt}")
        
        return evaluation
    
    def _should_adopt(self, comparison: Dict[str, Any]) -> tuple[bool, str]:
        """Determine if the new prompt should be adopted"""
        winner = comparison["winner"]
        
        if winner == "prompt_b":
            # Calculate improvement
            metrics_a = comparison["prompt_a"]["metrics"]
            metrics_b = comparison["prompt_b"]["metrics"]
            
            success_improvement = (metrics_b["success_rate"] - metrics_a["success_rate"]) / max(metrics_a["success_rate"], 0.01)
            
            if success_improvement >= self.baseline_threshold:
                return True, f"Success rate improved by {success_improvement:.1%}"
            else:
                return False, f"Improvement ({success_improvement:.1%}) below threshold ({self.baseline_threshold:.1%})"
        else:
            return False, "Proposed prompt did not outperform current"
    
    def _calculate_improvement(self, comparison: Dict[str, Any]) -> Dict[str, float]:
        """Calculate improvement metrics"""
        metrics_a = comparison["prompt_a"]["metrics"]
        metrics_b = comparison["prompt_b"]["metrics"]
        
        improvements = {}
        
        for key in metrics_a:
            if metrics_a[key] > 0:
                improvement = (metrics_b[key] - metrics_a[key]) / metrics_a[key]
                improvements[key] = improvement
            else:
                improvements[key] = 0.0
        
        return improvements
    
    async def evaluate_batch(
        self,
        proposals: Dict[str, str]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Evaluate multiple prompt proposals.
        
        Args:
            proposals: Dictionary mapping layer names to proposed prompts
            
        Returns:
            Dictionary mapping layer names to evaluation results
        """
        evaluations = {}
        
        for layer_name, proposed_prompt in proposals.items():
            if proposed_prompt:
                evaluation = await self.evaluate_proposal(layer_name, proposed_prompt)
                evaluations[layer_name] = evaluation
            else:
                evaluations[layer_name] = {
                    "should_adopt": False,
                    "reason": "No proposal provided"
                }
        
        return evaluations
