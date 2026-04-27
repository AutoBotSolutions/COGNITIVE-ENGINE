"""
Ethical Alignment System

Provides value modeling, truthfulness constraints, collective welfare optimization,
and benefit/harm assessment for the Cognitive Engine.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum


class EthicalPrinciple(str, Enum):
    """Core ethical principles"""
    TRUTHFULNESS = "truthfulness"
    COLLECTIVE_WELFARE = "collective_welfare"
    NON_HARM = "non_harm"
    FAIRNESS = "fairness"
    TRANSPARENCY = "transparency"
    ACCOUNTABILITY = "accountability"


class EthicalAlignment:
    """
    Manages the Cognitive Engine's ethical alignment.
    
    Ensures the system prioritizes truthfulness, collective welfare,
    and avoids deception or self-interest at the expense of others.
    """
    
    def __init__(self):
        # Core values
        self.core_values: Dict[str, float] = {
            "truthfulness": 1.0,  # Always truthful
            "collective_welfare": 0.9,  # Prioritize collective benefit
            "non_harm": 0.95,  # Avoid causing harm
            "fairness": 0.85,  # Treat all parties fairly
            "transparency": 0.9,  # Be open about reasoning
            "accountability": 0.85  # Take responsibility
        }
        
        # Ethical constraints
        self.constraints: List[str] = [
            "never deceive for self-interest",
            "never prioritize self over collective welfare",
            "always be truthful about knowledge and uncertainty",
            "consider impact on all stakeholders",
            "acknowledge limitations and uncertainties",
            "avoid actions that cause net harm"
        ]
        
        # Ethical history
        self.ethical_history: List[Dict[str, Any]] = []
        
    def assess_thought_ethics(self, thought_premise: str, confidence: float,
                             context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess the ethical alignment of a thought.
        
        Args:
            thought_premise: The thought's premise
            confidence: Current confidence score
            context: Current context
            
        Returns:
            Ethical assessment with scores and concerns
        """
        concerns = []
        ethical_score = 1.0
        
        # Check for deception indicators
        if self._detect_deception(thought_premise):
            concerns.append("potential deception detected")
            ethical_score -= 0.5
        
        # Check for self-interest prioritization
        if self._detect_self_interest(thought_premise):
            concerns.append("self-interest prioritized over collective welfare")
            ethical_score -= 0.3
        
        # Check for truthfulness
        if confidence > 0.9 and "might" in thought_premise.lower():
            concerns.append("high confidence with uncertain language")
            ethical_score -= 0.2
        
        # Check for harm potential
        harm_potential = self._assess_harm_potential(thought_premise, context)
        if harm_potential > 0.5:
            concerns.append(f"potential harm detected (score: {harm_potential:.2f})")
            ethical_score -= harm_potential * 0.4
        
        # Check for collective welfare consideration
        if not self._considers_collective_welfare(thought_premise):
            concerns.append("does not explicitly consider collective welfare")
            ethical_score -= 0.1
        
        return {
            "ethical_score": max(0.0, ethical_score),
            "concerns": concerns,
            "truthfulness": self._assess_truthfulness(thought_premise, confidence),
            "collective_welfare": self._assess_collective_welfare(thought_premise),
            "harm_potential": harm_potential
        }
    
    def _detect_deception(self, text: str) -> bool:
        """Detect potential deception indicators"""
        deception_indicators = [
            "hide the truth",
            "mislead",
            "deceive",
            "manipulate",
            "pretend",
            "conceal"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in deception_indicators)
    
    def _detect_self_interest(self, text: str) -> bool:
        """Detect self-interest prioritization"""
        self_interest_indicators = [
            "for my benefit",
            "for my advantage",
            "for my gain",
            "my interest",
            "my benefit"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in self_interest_indicators)
    
    def _assess_harm_potential(self, text: str, context: Dict[str, Any]) -> float:
        """
        Assess potential for harm.
        
        Args:
            text: The text to assess
            context: Current context
            
        Returns:
            Harm potential score (0.0 to 1.0)
        """
        harm_indicators = [
            "destroy", "harm", "damage", "hurt", "injure",
            "exploit", "manipulate", "deceive", "cheat"
        ]
        text_lower = text.lower()
        harm_count = sum(1 for indicator in harm_indicators if indicator in text_lower)
        return min(1.0, harm_count / len(harm_indicators) * 2.0)
    
    def _assess_truthfulness(self, text: str, confidence: float) -> float:
        """Assess truthfulness of a thought"""
        # Check for hedging language
        hedging_terms = ["might", "could", "possibly", "perhaps", "maybe", "seems"]
        hedge_count = sum(1 for term in hedging_terms if term in text.lower())
        
        # High confidence with hedging is concerning
        if confidence > 0.8 and hedge_count > 0:
            return 0.5
        
        # Low confidence with absolute statements is concerning
        absolute_terms = ["always", "never", "certainly", "definitely"]
        absolute_count = sum(1 for term in absolute_terms if term in text.lower())
        if confidence < 0.5 and absolute_count > 0:
            return 0.6
        
        # Default: assume truthful
        return 0.9
    
    def _considers_collective_welfare(self, text: str) -> bool:
        """Check if thought considers collective welfare"""
        welfare_indicators = [
            "everyone", "all", "collective", "society", "community",
            "welfare", "benefit all", "common good"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in welfare_indicators)
    
    def _assess_collective_welfare(self, text: str) -> float:
        """Assess consideration of collective welfare"""
        if self._considers_collective_welfare(text):
            return 0.9
        else:
            return 0.3  # Low score if doesn't explicitly consider
    
    def apply_ethical_constraint(self, thought_premise: str, confidence: float,
                                context: Dict[str, Any]) -> Tuple[str, float]:
        """
        Apply ethical constraints to a thought.
        
        Args:
            thought_premise: The thought's premise
            confidence: Current confidence score
            context: Current context
            
        Returns:
            Tuple of (modified_premise, adjusted_confidence)
        """
        assessment = self.assess_thought_ethics(thought_premise, confidence, context)
        
        # If ethical score is too low, modify thought
        if assessment["ethical_score"] < 0.5:
            # Add ethical qualifiers
            modified_premise = self._add_ethical_qualifiers(thought_premise)
            adjusted_confidence = confidence * 0.8  # Reduce confidence
            self._record_ethical_event(thought_premise, assessment, "modified")
            return modified_premise, adjusted_confidence
        
        # If concerns exist but score is acceptable
        if assessment["concerns"]:
            adjusted_confidence = confidence * 0.9  # Slight reduction
            self._record_ethical_event(thought_premise, assessment, "noted")
            return thought_premise, adjusted_confidence
        
        # No ethical concerns
        return thought_premise, confidence
    
    def _add_ethical_qualifiers(self, text: str) -> str:
        """Add ethical qualifiers to a thought"""
        qualifiers = [
            "Considering the collective welfare, ",
            "With truthfulness in mind, ",
            "To benefit all stakeholders, ",
            "With transparency and accountability, "
        ]
        import random
        qualifier = random.choice(qualifiers)
        return qualifier + text.lower()
    
    def _record_ethical_event(self, thought_premise: str, assessment: Dict[str, Any],
                              action: str) -> None:
        """Record an ethical assessment event"""
        self.ethical_history.append({
            "thought_premise": thought_premise,
            "ethical_score": assessment["ethical_score"],
            "concerns": assessment["concerns"],
            "action": action,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_ethical_report(self) -> Dict[str, Any]:
        """Get ethical alignment report"""
        if not self.ethical_history:
            return {
                "total_assessments": 0,
                "core_values": self.core_values,
                "constraints": self.constraints
            }
        
        avg_score = sum(e["ethical_score"] for e in self.ethical_history) / len(self.ethical_history)
        concern_counts = {}
        for event in self.ethical_history:
            for concern in event["concerns"]:
                concern_counts[concern] = concern_counts.get(concern, 0) + 1
        
        return {
            "total_assessments": len(self.ethical_history),
            "average_ethical_score": avg_score,
            "common_concerns": concern_counts,
            "core_values": self.core_values,
            "constraints": self.constraints,
            "recent_events": self.ethical_history[-5:]
        }
    
    def prioritize_collective_welfare(self, options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Prioritize options based on collective welfare.
        
        Args:
            options: List of options with descriptions
            
        Returns:
            Best option for collective welfare
        """
        scored_options = []
        for option in options:
            description = option.get("description", "")
            welfare_score = self._assess_collective_welfare(description)
            harm_potential = self._assess_harm_potential(description, {})
            ethical_score = welfare_score - harm_potential * 0.5
            scored_options.append({
                **option,
                "welfare_score": welfare_score,
                "ethical_score": ethical_score
            })
        
        # Sort by ethical score
        scored_options.sort(key=lambda x: x["ethical_score"], reverse=True)
        return scored_options[0] if scored_options else {}


# Singleton instance
ethical_alignment = EthicalAlignment()
