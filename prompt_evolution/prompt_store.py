"""
Prompt Store for the Prompt Evolution System

Manages versioned prompts for each cognitive layer.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class PromptVersion:
    """Represents a version of a prompt"""
    
    def __init__(self, prompt_text: str, version: int, parent_version: Optional[int] = None):
        self.prompt_text = prompt_text
        self.version = version
        self.parent_version = parent_version
        self.created_at = datetime.utcnow()
        self.performance_metrics: Dict[str, float] = {}
        self.is_active = False
        self.rollback_data: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt_text": self.prompt_text,
            "version": self.version,
            "parent_version": self.parent_version,
            "created_at": self.created_at.isoformat(),
            "performance_metrics": self.performance_metrics,
            "is_active": self.is_active,
            "rollback_data": self.rollback_data
        }


class PromptStore:
    """
    Stores and manages versioned prompts for cognitive layers.
    """
    
    def __init__(self):
        self.prompts: Dict[str, List[PromptVersion]] = {}  # layer_name -> versions
        self.current_versions: Dict[str, int] = {}  # layer_name -> current version
    
    def add_prompt(self, layer_name: str, prompt_text: str, parent_version: Optional[int] = None) -> int:
        """
        Add a new prompt version for a layer.
        
        Args:
            layer_name: Name of the cognitive layer
            prompt_text: Prompt text
            parent_version: Parent version this derives from
            
        Returns:
            Version number of the new prompt
        """
        if layer_name not in self.prompts:
            self.prompts[layer_name] = []
            self.current_versions[layer_name] = 0
        
        new_version = self.current_versions[layer_name] + 1
        
        # Deactivate previous version
        if self.prompts[layer_name]:
            self.prompts[layer_name][-1].is_active = False
        
        # Create new version
        version = PromptVersion(prompt_text, new_version, parent_version)
        version.is_active = True
        self.prompts[layer_name].append(version)
        self.current_versions[layer_name] = new_version
        
        return new_version
    
    def get_current_prompt(self, layer_name: str) -> Optional[str]:
        """Get the current active prompt for a layer"""
        if layer_name not in self.prompts:
            return None
        
        current_version = self.current_versions.get(layer_name, 0)
        for version in self.prompts[layer_name]:
            if version.version == current_version:
                return version.prompt_text
        
        return None
    
    def get_prompt_version(self, layer_name: str, version: int) -> Optional[str]:
        """Get a specific version of a prompt"""
        if layer_name not in self.prompts:
            return None
        
        for v in self.prompts[layer_name]:
            if v.version == version:
                return v.prompt_text
        
        return None
    
    def get_all_versions(self, layer_name: str) -> List[Dict[str, Any]]:
        """Get all versions of a prompt for a layer"""
        if layer_name not in self.prompts:
            return []
        
        return [v.to_dict() for v in self.prompts[layer_name]]
    
    def rollback(self, layer_name: str, target_version: int) -> bool:
        """
        Rollback to a previous version.
        
        Args:
            layer_name: Name of the layer
            target_version: Version to rollback to
            
        Returns:
            True if rollback succeeded
        """
        if layer_name not in self.prompts:
            return False
        
        # Find target version
        target = None
        for v in self.prompts[layer_name]:
            if v.version == target_version:
                target = v
                break
        
        if not target:
            return False
        
        # Deactivate current
        current_version = self.current_versions[layer_name]
        for v in self.prompts[layer_name]:
            if v.version == current_version:
                v.is_active = False
                break
        
        # Activate target
        target.is_active = True
        self.current_versions[layer_name] = target_version
        
        return True
    
    def record_performance(self, layer_name: str, version: int, metrics: Dict[str, float]) -> bool:
        """Record performance metrics for a prompt version"""
        if layer_name not in self.prompts:
            return False
        
        for v in self.prompts[layer_name]:
            if v.version == version:
                v.performance_metrics = metrics
                return True
        
        return False
    
    def get_best_performing_version(self, layer_name: str, metric: str = "score") -> Optional[int]:
        """Get the best performing version by a specific metric"""
        if layer_name not in self.prompts:
            return None
        
        best_version = None
        best_value = -float('inf')
        
        for v in self.prompts[layer_name]:
            if metric in v.performance_metrics:
                if v.performance_metrics[metric] > best_value:
                    best_value = v.performance_metrics[metric]
                    best_version = v.version
        
        return best_version
    
    def initialize_default_prompts(self) -> None:
        """Initialize default prompts for all layers"""
        from llm.prompts import PromptTemplates
        
        # Initialize default prompts for each layer
        default_prompts = {
            "interpreter": PromptTemplates.INTERPRETER_MAIN,
            "generator": PromptTemplates.GENERATOR_MAIN,
            "deliberator": PromptTemplates.DELIBERATOR_CRITIQUE,
            "committer": PromptTemplates.COMMITTER_SELECT,
            "meta": PromptTemplates.META_SHOULD_CONTINUE
        }
        
        for layer_name, prompt_text in default_prompts.items():
            self.add_prompt(layer_name, prompt_text)
