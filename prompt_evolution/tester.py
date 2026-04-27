"""
Prompt Tester for the Prompt Evolution System

A/B tests prompt candidates before adoption.
"""

from typing import Dict, Any, List, Optional
import asyncio

from prompt_evolution.prompt_store import PromptStore
from core.engine import CognitiveEngine
from utils.logger import logger


class PromptTester:
    """
    Tests prompt candidates through A/B testing.
    """
    
    def __init__(self, prompt_store: PromptStore):
        self.prompt_store = prompt_store
        self.test_inputs = [
            "What is the meaning of life?",
            "Explain quantum computing in simple terms.",
            "How can I improve my productivity?"
        ]
    
    async def test_prompt(
        self,
        layer_name: str,
        prompt_text: str,
        test_inputs: List[str] = None
    ) -> Dict[str, Any]:
        """
        Test a prompt candidate.
        
        Args:
            layer_name: Name of the layer
            prompt_text: Prompt text to test
            test_inputs: Test inputs (uses defaults if None)
            
        Returns:
            Test results
        """
        logger.info(f"PromptTester: Testing prompt for {layer_name}")
        
        test_inputs = test_inputs or self.test_inputs
        
        # Temporarily replace the prompt
        original_prompt = self.prompt_store.get_current_prompt(layer_name)
        original_version = self.prompt_store.current_versions.get(layer_name, 0)
        
        # Add test version
        test_version = self.prompt_store.add_prompt(layer_name, prompt_text)
        
        # Run tests
        results = []
        for test_input in test_inputs:
            try:
                # Create a fresh engine for each test
                engine = CognitiveEngine()
                engine.initialize_layers()
                
                # Run the test
                result = await engine.process(test_input)
                
                results.append({
                    "input": test_input,
                    "success": result.get("success", False),
                    "duration": result.get("duration_seconds", 0),
                    "thought_count": result.get("thought_count", 0),
                    "iterations": result.get("iterations", 0)
                })
            except Exception as e:
                logger.error(f"PromptTester: Test failed: {e}")
                results.append({
                    "input": test_input,
                    "success": False,
                    "error": str(e)
                })
        
        # Calculate metrics
        success_rate = sum(1 for r in results if r["success"]) / len(results) if results else 0
        avg_duration = sum(r.get("duration", 0) for r in results) / len(results) if results else 0
        avg_thoughts = sum(r.get("thought_count", 0) for r in results) / len(results) if results else 0
        
        # Rollback to original
        self.prompt_store.rollback(layer_name, original_version)
        
        test_results = {
            "layer_name": layer_name,
            "test_version": test_version,
            "results": results,
            "metrics": {
                "success_rate": success_rate,
                "avg_duration": avg_duration,
                "avg_thoughts": avg_thoughts
            }
        }
        
        logger.info(f"PromptTester: Test complete - Success rate: {success_rate:.2f}")
        
        return test_results
    
    async def ab_test(
        self,
        layer_name: str,
        prompt_a: str,
        prompt_b: str,
        test_inputs: List[str] = None
    ) -> Dict[str, Any]:
        """
        A/B test two prompts.
        
        Args:
            layer_name: Name of the layer
            prompt_a: First prompt to test
            prompt_b: Second prompt to test
            test_inputs: Test inputs
            
        Returns:
            Comparison results
        """
        logger.info(f"PromptTester: A/B testing prompts for {layer_name}")
        
        # Test both prompts
        results_a = await self.test_prompt(layer_name, prompt_a, test_inputs)
        results_b = await self.test_prompt(layer_name, prompt_b, test_inputs)
        
        # Compare
        comparison = {
            "prompt_a": results_a,
            "prompt_b": results_b,
            "winner": self._determine_winner(results_a, results_b)
        }
        
        return comparison
    
    def _determine_winner(self, results_a: Dict[str, Any], results_b: Dict[str, Any]) -> str:
        """Determine which prompt performed better"""
        metrics_a = results_a["metrics"]
        metrics_b = results_b["metrics"]
        
        # Simple comparison based on success rate
        if metrics_a["success_rate"] > metrics_b["success_rate"]:
            return "prompt_a"
        elif metrics_b["success_rate"] > metrics_a["success_rate"]:
            return "prompt_b"
        else:
            # If tied, compare by average duration (faster is better)
            if metrics_a["avg_duration"] < metrics_b["avg_duration"]:
                return "prompt_a"
            else:
                return "prompt_b"
