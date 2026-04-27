"""
Prompt Controller for the Prompt Evolution System

Controls the prompt evolution process with safety checks and rollback capability.
"""

from typing import Dict, Any, List, Optional
import asyncio

from prompt_evolution.prompt_store import PromptStore
from prompt_evolution.proposer import PromptProposer
from prompt_evolution.evaluator import PromptEvaluator
from utils.logger import logger
from core.config import config


class PromptController:
    """
    Controller for the prompt evolution system.
    
    Manages the complete evolution cycle with safety checks and rollback capability.
    """
    
    def __init__(self):
        self.prompt_store = PromptStore()
        self.proposer = PromptProposer(self.prompt_store)
        self.evaluator = PromptEvaluator(self.prompt_store)
        self.enabled = config.enable_prompt_evolution
        self.evolution_history: List[Dict[str, Any]] = []
    
    def initialize(self) -> None:
        """Initialize the prompt evolution system"""
        logger.info("PromptController: Initializing")
        self.prompt_store.initialize_default_prompts()
    
    async def run_evolution_cycle(self, layer_names: List[str] = None) -> Dict[str, Any]:
        """
        Run a complete prompt evolution cycle.
        
        Args:
            layer_names: Layers to evolve (uses all if None)
            
        Returns:
            Evolution cycle results
        """
        if not self.enabled:
            logger.info("PromptController: Prompt evolution disabled")
            return {"enabled": False}
        
        logger.info("PromptController: Running evolution cycle")
        
        # Get layers to evolve
        if layer_names is None:
            layer_names = list(self.prompt_store.prompts.keys())
        
        # Propose improvements
        proposals = await self.proposer.propose_batch_improvements(layer_names)
        
        # Evaluate proposals
        evaluations = await self.evaluator.evaluate_batch(proposals)
        
        # Apply approved changes
        applied = {}
        for layer_name, evaluation in evaluations.items():
            if evaluation["should_adopt"]:
                proposed_prompt = proposals[layer_name]
                if proposed_prompt:
                    # Apply the new prompt
                    current_version = self.prompt_store.current_versions.get(layer_name, 0)
                    new_version = self.prompt_store.add_prompt(
                        layer_name,
                        proposed_prompt,
                        parent_version=current_version
                    )
                    
                    # Record performance metrics
                    metrics = evaluation.get("improvement_metrics", {})
                    self.prompt_store.record_performance(layer_name, current_version, metrics)
                    
                    applied[layer_name] = {
                        "old_version": current_version,
                        "new_version": new_version,
                        "improvement": metrics
                    }
        
        # Record history
        cycle_record = {
            "timestamp": str(asyncio.get_event_loop().time()),
            "layer_names": layer_names,
            "proposals": len(proposals),
            "evaluations": len(evaluations),
            "applied": len(applied),
            "applied_details": applied
        }
        self.evolution_history.append(cycle_record)
        
        logger.info(f"PromptController: Evolution cycle complete - Applied {len(applied)} changes")
        
        return {
            "enabled": True,
            "proposals": proposals,
            "evaluations": evaluations,
            "applied": applied,
            "history": cycle_record
        }
    
    def rollback_layer(self, layer_name: str, target_version: int) -> bool:
        """
        Rollback a layer to a specific version.
        
        Args:
            layer_name: Name of the layer
            target_version: Version to rollback to
            
        Returns:
            True if rollback succeeded
        """
        logger.info(f"PromptController: Rolling back {layer_name} to version {target_version}")
        
        success = self.prompt_store.rollback(layer_name, target_version)
        
        if success:
            logger.info(f"PromptController: Rollback successful")
        else:
            logger.warning(f"PromptController: Rollback failed")
        
        return success
    
    def rollback_all(self) -> Dict[str, bool]:
        """
        Rollback all layers to their initial versions.
        
        Returns:
            Dictionary mapping layer names to rollback success
        """
        logger.info("PromptController: Rolling back all layers")
        
        results = {}
        for layer_name in self.prompt_store.prompts:
            # Rollback to version 1 (initial)
            success = self.prompt_store.rollback(layer_name, 1)
            results[layer_name] = success
        
        return results
    
    def get_evolution_history(self) -> List[Dict[str, Any]]:
        """Get the evolution history"""
        return self.evolution_history
    
    def get_current_prompts(self) -> Dict[str, str]:
        """Get current prompts for all layers"""
        prompts = {}
        for layer_name in self.prompt_store.prompts:
            prompts[layer_name] = self.prompt_store.get_current_prompt(layer_name)
        return prompts
    
    def validate_coherence(self) -> Dict[str, Any]:
        """
        Validate that all prompts work together coherently.
        
        Returns:
            Validation results
        """
        logger.info("PromptController: Validating prompt coherence")
        
        # In a full implementation, this would test the entire pipeline
        # For now, we'll do a basic check
        all_prompts = self.get_current_prompts()
        
        validation = {
            "valid": True,
            "issues": [],
            "prompt_count": len(all_prompts)
        }
        
        # Check that all layers have prompts
        expected_layers = ["interpreter", "generator", "deliberator", "committer", "meta"]
        for layer in expected_layers:
            if layer not in all_prompts or not all_prompts[layer]:
                validation["valid"] = False
                validation["issues"].append(f"Missing or empty prompt for {layer}")
        
        return validation
