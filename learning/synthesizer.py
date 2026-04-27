"""
Pattern Synthesizer for the Learning System

Converts patterns into operational rules.
"""

from typing import List, Dict, Any
import json

from learning.patterns import Pattern, Rule
from utils.memory import memory
from llm.client import llm_client
from llm.prompts import PromptTemplates
from utils.logger import logger


class PatternSynthesizer:
    """
    Synthesizes rules from patterns.
    """
    
    def __init__(self):
        self.min_confidence = 0.7
    
    async def synthesize_rules(self, patterns: List[Pattern] = None) -> List[Rule]:
        """
        Synthesize rules from patterns.
        
        Args:
            patterns: Patterns to synthesize (if None, retrieves from memory)
            
        Returns:
            List of synthesized rules
        """
        logger.info("PatternSynthesizer: Synthesizing rules from patterns")
        
        # Retrieve patterns if not provided
        if patterns is None:
            pattern_data = memory.retrieve_patterns(min_confidence=0.5, limit=50)
            patterns = [Pattern.from_dict(p) for p in pattern_data]
        
        if not patterns:
            logger.warning("PatternSynthesizer: No patterns to synthesize")
            return []
        
        # Build patterns text for LLM
        patterns_text = "\n".join([
            f"Pattern {i+1}: {p.pattern_text} (confidence: {p.confidence}, frequency: {p.frequency})"
            for i, p in enumerate(patterns[:20])  # Limit to 20 for LLM context
        ])
        
        prompt = PromptTemplates.format_template(
            "LEARNING_SYNTHESIZE_RULES",
            patterns=patterns_text
        )
        
        response = await llm_client.generate(prompt)
        
        # Parse rules from response
        rules = self._parse_rule_response(response, patterns)
        
        # Store rules in rule memory
        for rule in rules:
            if rule.confidence >= self.min_confidence:
                memory.store_rule(rule.rule_text, rule.rule_type, rule.confidence)
        
        logger.info(f"PatternSynthesizer: Synthesized {len(rules)} rules")
        
        return rules
    
    def _parse_rule_response(self, response: str, source_patterns: List[Pattern]) -> List[Rule]:
        """Parse LLM response into Rule objects"""
        rules = []
        
        import re
        
        rule_matches = re.findall(r'Rule\s*\d+:\s*(.+?)(?=Rule\s*\d+:|$)', response, re.DOTALL)
        
        for i, match in enumerate(rule_matches):
            rule_text = match.strip().split('\n')[0]  # First line is the rule
            
            # Extract rule type
            rule_type = "strategy"  # Default
            type_match = re.search(r'type[:\s]*(\w+)', match, re.IGNORECASE)
            if type_match:
                rule_type = type_match.group(1).lower()
            
            # Extract confidence if present
            confidence = 0.7  # Default
            confidence_match = re.search(r'confidence[:\s]*([0-9.]+)', match, re.IGNORECASE)
            if confidence_match:
                confidence = float(confidence_match.group(1))
            
            # Link to source pattern if available
            source_pattern_id = source_patterns[i].id if i < len(source_patterns) else None
            
            rule = Rule(
                rule_text=rule_text,
                rule_type=rule_type,
                source_pattern_id=source_pattern_id,
                confidence=confidence
            )
            
            rules.append(rule)
        
        # If parsing failed, create a single rule from the response
        if not rules and response.strip():
            rule = Rule(
                rule_text=response.strip()[:200],
                rule_type="strategy",
                confidence=0.5
            )
            rules.append(rule)
        
        return rules
    
    async def synthesize_from_pattern(self, pattern: Pattern) -> Rule:
        """
        Synthesize a single rule from a pattern.
        
        Args:
            pattern: Pattern to synthesize from
            
        Returns:
            Synthesized rule
        """
        prompt = f"Convert this pattern into an operational rule:\nPattern: {pattern.pattern_text}\n\nProvide the rule text and its type."
        
        response = await llm_client.generate(prompt)
        
        rule = Rule(
            rule_text=response.strip()[:200],
            rule_type="strategy",
            source_pattern_id=pattern.id,
            confidence=pattern.confidence * 0.9  # Slightly lower than pattern confidence
        )
        
        return rule
