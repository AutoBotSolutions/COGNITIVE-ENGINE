"""
Prompt Proposer for the Prompt Evolution System

Proposes improvements to prompts using LLM.
"""

from typing import Dict, Any, Optional
import json

from prompt_evolution.prompt_store import PromptStore
from llm.client import llm_client
from llm.prompts import PromptTemplates
from utils.logger import logger
from core.config import config


class PromptProposer:
    """
    Proposes improved prompts using LLM analysis.
    """
    
    def __init__(self, prompt_store: PromptStore):
        self.prompt_store = prompt_store
        self.enabled = config.enable_prompt_evolution
    
    async def propose_improvement(self, layer_name: str, performance_data: Dict[str, Any] = None) -> Optional[str]:
        """
        Propose an improved version of a prompt.
        
        Args:
            layer_name: Name of the layer to improve
            performance_data: Performance data to inform improvement
            
        Returns:
            Proposed improved prompt text, or None if proposal failed
        """
        if not self.enabled:
            logger.info("PromptProposer: Prompt evolution disabled")
            return None
        
        logger.info(f"PromptProposer: Proposing improvement for {layer_name}")
        
        current_prompt = self.prompt_store.get_current_prompt(layer_name)
        if not current_prompt:
            logger.warning(f"PromptProposer: No current prompt for {layer_name}")
            return None
        
        prompt = PromptTemplates.format_template(
            "PROMPT_EVOLUTION_PROPOSE",
            current_prompt=current_prompt,
            layer=layer_name,
            performance_data=json.dumps(performance_data or {}, default=str)
        )
        
        response = await llm_client.generate(prompt)
        
        # Extract the improved prompt from response
        improved_prompt = self._extract_improved_prompt(response)
        
        if improved_prompt:
            logger.info(f"PromptProposer: Proposed improvement for {layer_name}")
            return improved_prompt
        
        logger.warning(f"PromptProposer: Failed to extract improved prompt for {layer_name}")
        return None
    
    def _extract_improved_prompt(self, response: str) -> Optional[str]:
        """Extract the improved prompt from LLM response"""
        # Look for patterns like "Improved prompt:" or "New version:"
        import re
        
        patterns = [
            r'Improved prompt:\s*(.+?)(?=\n\n|$)',
            r'New version:\s*(.+?)(?=\n\n|$)',
            r'Proposed prompt:\s*(.+?)(?=\n\n|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # If no pattern found, use the whole response
        if response.strip():
            return response.strip()
        
        return None
    
    async def propose_batch_improvements(self, layer_names: list, performance_data: Dict[str, Any] = None) -> Dict[str, Optional[str]]:
        """
        Propose improvements for multiple layers.
        
        Args:
            layer_names: List of layer names to improve
            performance_data: Performance data dictionary
            
        Returns:
            Dictionary mapping layer names to proposed prompts
        """
        proposals = {}
        
        for layer_name in layer_names:
            layer_performance = performance_data.get(layer_name, {}) if performance_data else {}
            proposal = await self.propose_improvement(layer_name, layer_performance)
            proposals[layer_name] = proposal
        
        return proposals
