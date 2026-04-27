"""
Self-Doubt System

Provides active self-questioning, counter-argument generation,
and adaptive confidence modeling for the Cognitive Engine.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum
import random


class DoubtLevel(str, Enum):
    """Levels of self-doubt"""
    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    SEVERE = "severe"


class SelfDoubt:
    """
    Manages the Cognitive Engine's self-doubt capabilities.
    
    Provides active self-questioning, counter-argument generation,
    confidence uncertainty modeling, and adaptive confidence adjustment.
    """
    
    def __init__(self):
        # Doubt tracking
        self.doubt_history: List[Dict[str, Any]] = []
        self.current_doubt_level = DoubtLevel.MODERATE
        
        # Self-questioning patterns
        self.questioning_patterns = [
            "What assumptions am I making?",
            "What evidence supports this?",
            "What evidence contradicts this?",
            "What alternative explanations exist?",
            "What would a critic say?",
            "What are the weaknesses in this reasoning?",
            "Am I being too confident?",
            "What information am I missing?"
        ]
        
        # Confidence uncertainty model
        self.uncertainty_factors: Dict[str, float] = {
            "complexity": 0.0,
            "ambiguity": 0.0,
            "novelty": 0.0,
            "information_gaps": 0.0
        }
        
    def assess_doubt_level(self, thought_premise: str, confidence: float, 
                          context: Dict[str, Any]) -> DoubtLevel:
        """
        Assess the appropriate doubt level for a thought.
        
        Args:
            thought_premise: The thought's premise
            confidence: Current confidence score
            context: Current context
            
        Returns:
            Appropriate doubt level
        """
        uncertainty_score = self._calculate_uncertainty(thought_premise, context)
        
        # Combine with existing confidence
        combined_score = uncertainty_score * (1.0 - confidence)
        
        if combined_score > 0.7:
            return DoubtLevel.SEVERE
        elif combined_score > 0.5:
            return DoubtLevel.HIGH
        elif combined_score > 0.3:
            return DoubtLevel.MODERATE
        elif combined_score > 0.1:
            return DoubtLevel.LOW
        else:
            return DoubtLevel.NONE
    
    def _calculate_uncertainty(self, thought_premise: str, context: Dict[str, Any]) -> float:
        """
        Calculate uncertainty score for a thought.
        
        Args:
            thought_premise: The thought's premise
            context: Current context
            
        Returns:
            Uncertainty score (0.0 to 1.0)
        """
        uncertainty = 0.0
        
        # Complexity factor
        complexity = len(thought_premise.split()) / 100.0
        self.uncertainty_factors["complexity"] = min(1.0, complexity)
        uncertainty += complexity * 0.2
        
        # Ambiguity factor (check for vague terms)
        vague_terms = ["might", "could", "possibly", "perhaps", "maybe", "seems"]
        ambiguity = sum(1 for term in vague_terms if term in thought_premise.lower()) / len(vague_terms)
        self.uncertainty_factors["ambiguity"] = ambiguity
        uncertainty += ambiguity * 0.3
        
        # Novelty factor (check against context)
        if context.get("knowns"):
            known_keys = str(context["knowns"]).lower()
            novelty = 1.0 - (sum(1 for word in thought_premise.lower().split() if word in known_keys) / len(thought_premise.split()))
            self.uncertainty_factors["novelty"] = min(1.0, novelty)
            uncertainty += novelty * 0.3
        
        # Information gaps
        if context.get("unknowns"):
            information_gaps = len(context["unknowns"]) / 10.0
            self.uncertainty_factors["information_gaps"] = min(1.0, information_gaps)
            uncertainty += information_gaps * 0.2
        
        return min(1.0, uncertainty)
    
    def generate_self_questions(self, thought_premise: str, doubt_level: DoubtLevel) -> List[str]:
        """
        Generate self-questions based on doubt level.
        
        Args:
            thought_premise: The thought's premise
            doubt_level: Current doubt level
            
        Returns:
            List of self-questions
        """
        num_questions = {
            DoubtLevel.NONE: 0,
            DoubtLevel.LOW: 1,
            DoubtLevel.MODERATE: 2,
            DoubtLevel.HIGH: 3,
            DoubtLevel.SEVERE: 5
        }.get(doubt_level, 2)
        
        questions = []
        for _ in range(num_questions):
            question = random.choice(self.questioning_patterns)
            # Make question specific to the thought
            if "this" in question.lower():
                question = question.replace("this", f"the thought: {thought_premise[:50]}")
            questions.append(question)
        
        return questions
    
    def generate_counter_argument(self, thought_premise: str) -> str:
        """
        Generate a counter-argument to a thought.
        
        Args:
            thought_premise: The thought's premise
            
        Returns:
            Counter-argument
        """
        # Simple counter-argument patterns
        counter_patterns = [
            f"However, {thought_premise.lower()} might not be true because...",
            f"On the other hand, {thought_premise.lower()} could be challenged by...",
            f"An alternative perspective is that {thought_premise.lower()} overlooks...",
            f"Contrary to {thought_premise.lower()}, one could argue that...",
            f"While {thought_premise.lower()} seems plausible, it fails to consider..."
        ]
        
        return random.choice(counter_patterns)
    
    def adjust_confidence_with_doubt(self, original_confidence: float, 
                                     doubt_level: DoubtLevel) -> float:
        """
        Adjust confidence based on doubt level.
        
        Args:
            original_confidence: Original confidence score
            doubt_level: Current doubt level
            
        Returns:
            Adjusted confidence score
        """
        doubt_reduction = {
            DoubtLevel.NONE: 0.0,
            DoubtLevel.LOW: 0.05,
            DoubtLevel.MODERATE: 0.15,
            DoubtLevel.HIGH: 0.25,
            DoubtLevel.SEVERE: 0.40
        }.get(doubt_level, 0.15)
        
        return max(0.0, original_confidence - doubt_reduction)
    
    def challenge_assumption(self, assumption: str) -> Dict[str, Any]:
        """
        Challenge an assumption with counter-arguments and questions.
        
        Args:
            assumption: The assumption to challenge
            
        Returns:
            Challenge result with counter-arguments and questions
        """
        counter_arg = self.generate_counter_argument(assumption)
        questions = self.generate_self_questions(assumption, DoubtLevel.HIGH)
        
        return {
            "assumption": assumption,
            "counter_argument": counter_arg,
            "challenging_questions": questions,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def record_doubt_event(self, thought_id: str, doubt_level: DoubtLevel, 
                          questions: List[str], resolution: str) -> None:
        """
        Record a doubt event for tracking.
        
        Args:
            thought_id: ID of the thought
            doubt_level: Level of doubt
            questions: Self-questions asked
            resolution: How the doubt was resolved
        """
        self.doubt_history.append({
            "thought_id": thought_id,
            "doubt_level": doubt_level.value,
            "questions": questions,
            "resolution": resolution,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_doubt_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about doubt events.
        
        Returns:
            Doubt statistics
        """
        if not self.doubt_history:
            return {
                "total_doubt_events": 0,
                "by_level": {},
                "current_uncertainty_factors": self.uncertainty_factors,
                "recent_events": []
            }
        
        level_counts = {}
        for event in self.doubt_history:
            level = event["doubt_level"]
            level_counts[level] = level_counts.get(level, 0) + 1
        
        return {
            "total_doubt_events": len(self.doubt_history),
            "by_level": level_counts,
            "current_uncertainty_factors": self.uncertainty_factors,
            "recent_events": self.doubt_history[-5:]
        }


# Singleton instance
self_doubt = SelfDoubt()
