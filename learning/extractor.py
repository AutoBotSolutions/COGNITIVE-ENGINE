"""
Pattern Extractor for the Learning System

Extracts recurring patterns from episodic memory.
"""

from typing import List, Dict, Any
import json

from learning.patterns import Pattern
from utils.memory import memory
from llm.client import llm_client
from llm.prompts import PromptTemplates
from utils.logger import logger
from core.config import config


class PatternExtractor:
    """
    Extracts recurring patterns from experiences stored in episodic memory.
    """
    
    def __init__(self):
        self.min_confidence = config.pattern_confidence_threshold
    
    async def extract_patterns(self, limit: int = 100) -> List[Pattern]:
        """
        Extract patterns from episodic memory.
        
        Args:
            limit: Number of recent experiences to analyze
            
        Returns:
            List of extracted patterns
        """
        logger.info(f"PatternExtractor: Extracting patterns from {limit} experiences")
        
        # Retrieve recent experiences
        experiences = memory.retrieve_episodic(limit=limit)
        
        if not experiences:
            logger.warning("PatternExtractor: No experiences to analyze")
            return []
        
        # Group experiences by type
        grouped = self._group_experiences(experiences)
        
        # Extract patterns from each group
        all_patterns = []
        for event_type, exps in grouped.items():
            patterns = await self._extract_from_group(event_type, exps)
            all_patterns.extend(patterns)
        
        logger.info(f"PatternExtractor: Extracted {len(all_patterns)} patterns")
        
        return all_patterns
    
    def _group_experiences(self, experiences: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group experiences by event type"""
        grouped = {}
        for exp in experiences:
            event_type = exp.get("event_type", "unknown")
            if event_type not in grouped:
                grouped[event_type] = []
            grouped[event_type].append(exp)
        return grouped
    
    async def _extract_from_group(self, event_type: str, experiences: List[Dict[str, Any]]) -> List[Pattern]:
        """Extract patterns from a group of experiences"""
        # Build summary of experiences
        experiences_text = "\n".join([
            f"Experience {i+1}: {json.dumps(exp, default=str)}"
            for i, exp in enumerate(experiences[:20])  # Limit to 20 for LLM context
        ])
        
        prompt = PromptTemplates.format_template(
            "LEARNING_EXTRACT_PATTERNS",
            experiences=experiences_text
        )
        
        response = await llm_client.generate(prompt)
        
        # Parse patterns from response
        patterns = self._parse_pattern_response(response, event_type, experiences)
        
        # Store patterns in pattern memory
        for pattern in patterns:
            if pattern.confidence >= self.min_confidence:
                memory.store_pattern(pattern.pattern_text, pattern.confidence)
        
        return patterns
    
    def _parse_pattern_response(self, response: str, event_type: str, experiences: List[Dict[str, Any]]) -> List[Pattern]:
        """Parse LLM response into Pattern objects"""
        patterns = []
        
        # Simple parsing - look for numbered patterns
        import re
        
        pattern_matches = re.findall(r'Pattern\s*\d+:\s*(.+?)(?=Pattern\s*\d+:|$)', response, re.DOTALL)
        
        for i, match in enumerate(pattern_matches):
            pattern_text = match.strip().split('\n')[0]  # First line is the pattern
            
            # Extract confidence if present
            confidence = 0.7  # Default
            confidence_match = re.search(r'confidence[:\s]*([0-9.]+)', match, re.IGNORECASE)
            if confidence_match:
                confidence = float(confidence_match.group(1))
            
            pattern = Pattern(
                pattern_text=pattern_text,
                pattern_type=event_type,
                confidence=confidence,
                source_experiences=[exp.get("id", "") for exp in experiences[:5]]
            )
            
            patterns.append(pattern)
        
        # If parsing failed, create a single pattern from the response
        if not patterns and response.strip():
            pattern = Pattern(
                pattern_text=response.strip()[:200],
                pattern_type=event_type,
                confidence=0.5
            )
            patterns.append(pattern)
        
        return patterns
    
    async def extract_from_specific_event(self, event_type: str, limit: int = 50) -> List[Pattern]:
        """
        Extract patterns from a specific event type.
        
        Args:
            event_type: Type of events to analyze
            limit: Number of events to retrieve
            
        Returns:
            List of extracted patterns
        """
        experiences = memory.retrieve_episodic(limit=limit, event_type=event_type)
        
        if not experiences:
            return []
        
        return await self._extract_from_group(event_type, experiences)
