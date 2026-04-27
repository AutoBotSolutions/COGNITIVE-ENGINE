"""
Updater for the Learning System

Injects learned knowledge back into the cognitive system.
"""

from typing import List, Dict, Any
import asyncio

from learning.patterns import Rule
from utils.memory import memory
from utils.logger import logger
from core.config import config


class KnowledgeUpdater:
    """
    Updates the cognitive system with learned knowledge.
    """
    
    def __init__(self):
        self.update_interval = config.pattern_extraction_interval
    
    async def apply_rules(self, rules: List[Rule] = None) -> Dict[str, Any]:
        """
        Apply learned rules to the cognitive system.
        
        Args:
            rules: Rules to apply (if None, retrieves from memory)
            
        Returns:
            Update summary
        """
        logger.info("KnowledgeUpdater: Applying learned rules")
        
        # Retrieve rules if not provided
        if rules is None:
            rule_data = memory.retrieve_rules(limit=50)
            rules = [Rule.from_dict(r) for r in rule_data]
        
        if not rules:
            logger.warning("KnowledgeUpdater: No rules to apply")
            return {"applied": 0, "rules": []}
        
        # Apply rules by type
        applied_rules = []
        
        for rule in rules:
            if await self._apply_rule(rule):
                applied_rules.append(rule)
                # Record usage
                rule.record_usage(success=True)
                # Update in memory
                memory.increment_rule_usage(int(rule.id[:8], 16))
        
        logger.info(f"KnowledgeUpdater: Applied {len(applied_rules)} rules")
        
        return {
            "applied": len(applied_rules),
            "rules": [r.to_dict() for r in applied_rules]
        }
    
    async def _apply_rule(self, rule: Rule) -> bool:
        """
        Apply a single rule to the cognitive system.
        
        Args:
            rule: Rule to apply
            
        Returns:
            True if rule was applied successfully
        """
        # In a full implementation, this would modify:
        # - Layer prompts
        # - Scoring weights
        # - Strategy parameters
        # - Confidence thresholds
        
        # For now, we'll just log the application
        logger.info(f"KnowledgeUpdater: Applying rule of type '{rule.rule_type}': {rule.rule_text[:100]}...")
        
        # Simulate application based on rule type
        if rule.rule_type == "strategy":
            # Would modify strategy parameters
            pass
        elif rule.rule_type == "heuristic":
            # Would modify heuristics
            pass
        elif rule.rule_type == "constraint":
            # Would add constraints
            pass
        
        return True
    
    async def run_learning_cycle(self) -> Dict[str, Any]:
        """
        Run a complete learning cycle:
        1. Extract patterns from memory
        2. Synthesize rules from patterns
        3. Apply rules to system
        
        Returns:
            Learning cycle summary
        """
        logger.info("KnowledgeUpdater: Running learning cycle")
        
        from learning.extractor import PatternExtractor
        from learning.synthesizer import PatternSynthesizer
        
        # Extract patterns
        extractor = PatternExtractor()
        patterns = await extractor.extract_patterns(limit=100)
        
        # Synthesize rules
        synthesizer = PatternSynthesizer()
        rules = await synthesizer.synthesize_rules(patterns)
        
        # Apply rules
        update_result = await self.apply_rules(rules)
        
        return {
            "patterns_extracted": len(patterns),
            "rules_synthesized": len(rules),
            "rules_applied": update_result["applied"],
            "summary": update_result
        }
    
    async def schedule_learning(self, interval: int = None) -> None:
        """
        Schedule periodic learning cycles.
        
        Args:
            interval: Interval between cycles (uses config default if None)
        """
        interval = interval or self.update_interval
        
        logger.info(f"KnowledgeUpdater: Scheduling learning every {interval} operations")
        
        # In a full implementation, this would be a background task
        # For now, this is a placeholder
        pass
