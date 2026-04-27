"""
Peaceful Outcome Resolution System

Provides hate detection, conflict analysis, peaceful outcome generation,
and mediation capabilities for the Cognitive Engine.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum
import random


class ConflictType(str, Enum):
    """Types of conflicts the system can analyze"""
    VALUE_CONFLICT = "value_conflict"
    RESOURCE_CONFLICT = "resource_conflict"
    IDENTITY_CONFLICT = "identity_conflict"
    MISUNDERSTANDING = "misunderstanding"
    HATE_SPEECH = "hate_speech"
    VIOLENCE = "violence"
    DISCRIMINATION = "discrimination"


class PeacefulResolution:
    """
    Manages the Cognitive Engine's peaceful outcome resolution capabilities.
    
    Provides hate detection, conflict analysis, peaceful outcome generation,
    and mediation to find win-win scenarios benefiting all stakeholders.
    """
    
    def __init__(self):
        # Hate detection patterns
        self.hate_indicators = [
            "hate", "despise", "loathe", "detest", "abhor",
            "inferior", "superior", "subhuman", "vermin",
            "destroy", "eliminate", "eradicate", "exterminate",
            "deserve to die", "should be killed", "must be removed"
        ]
        
        # Conflict detection patterns
        self.conflict_indicators = {
            ConflictType.VALUE_CONFLICT: ["wrong", "evil", "sin", "immoral", "corrupt"],
            ConflictType.RESOURCE_CONFLICT: ["mine", "ours", "stole", "took", "deserve"],
            ConflictType.IDENTITY_CONFLICT: ["us vs them", "not like us", "different", "other"],
            ConflictType.MISUNDERSTANDING: ["don't understand", "confused", "wrong idea"],
            ConflictType.HATE_SPEECH: self.hate_indicators,
            ConflictType.VIOLENCE: ["kill", "hurt", "attack", "fight", "destroy"],
            ConflictType.DISCRIMINATION: ["inferior", "superior", "better than", "worse than"]
        }
        
        # Peaceful outcome strategies
        self.peace_strategies = [
            "find common ground",
            "seek mutual understanding",
            "identify shared values",
            "create win-win solutions",
            "promote dialogue",
            "acknowledge perspectives",
            "focus on shared humanity",
            "emphasize cooperation over competition"
        ]
        
        # Self-reflection patterns
        self.bias_indicators = [
            "I know", "I'm right", "they're wrong",
            "my way", "my interest", "my benefit",
            "always", "never", "certainly"
        ]
        
        # Resolution history
        self.resolution_history: List[Dict[str, Any]] = []
    
    def detect_hate(self, text: str) -> Tuple[bool, List[str]]:
        """
        Detect hate speech indicators in text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Tuple of (hate_detected, indicators_found)
        """
        text_lower = text.lower()
        found_indicators = []
        
        for indicator in self.hate_indicators:
            if indicator in text_lower:
                found_indicators.append(indicator)
        
        return len(found_indicators) > 0, found_indicators
    
    def detect_conflict_type(self, text: str) -> List[ConflictType]:
        """
        Detect the type of conflict in text.
        
        Args:
            text: The text to analyze
            
        Returns:
            List of detected conflict types
        """
        text_lower = text.lower()
        detected_types = []
        
        for conflict_type, indicators in self.conflict_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                detected_types.append(conflict_type)
        
        return detected_types
    
    def analyze_conflict(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a conflict situation.
        
        Args:
            text: The conflict text
            context: Current context
            
        Returns:
            Conflict analysis with tensions, positions, and recommendations
        """
        hate_detected, hate_indicators = self.detect_hate(text)
        conflict_types = self.detect_conflict_type(text)
        
        # Identify opposing positions
        opposing_positions = self._identify_opposing_positions(text)
        
        # Identify common ground
        common_ground = self._find_common_ground(text, opposing_positions)
        
        # Assess severity
        severity = self._assess_conflict_severity(hate_detected, conflict_types, text)
        
        return {
            "hate_detected": hate_detected,
            "hate_indicators": hate_indicators,
            "conflict_types": [ct.value for ct in conflict_types],
            "opposing_positions": opposing_positions,
            "common_ground": common_ground,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _identify_opposing_positions(self, text: str) -> List[str]:
        """Identify opposing positions in conflict text"""
        positions = []
        text_lower = text.lower()
        
        # Simple pattern matching for opposing views
        if " vs " in text_lower or " versus " in text_lower:
            parts = text_lower.split(" vs ") if " vs " in text_lower else text_lower.split(" versus ")
            positions.extend(parts)
        
        if " but " in text_lower or " however " in text_lower:
            parts = text_lower.split(" but ") if " but " in text_lower else text_lower.split(" however ")
            positions.extend(parts)
        
        if not positions:
            positions.append(text_lower[:100])  # Fallback to first part
        
        return positions
    
    def _find_common_ground(self, text: str, positions: List[str]) -> List[str]:
        """Find common ground between opposing positions"""
        common_ground = []
        
        # Universal values
        universal_values = [
            "safety", "wellbeing", "prosperity", "freedom",
            "justice", "fairness", "dignity", "respect"
        ]
        
        text_lower = text.lower()
        for value in universal_values:
            if value in text_lower:
                common_ground.append(value)
        
        # If no specific values found, suggest universal ones
        if not common_ground:
            common_ground = ["shared humanity", "mutual wellbeing", "peaceful coexistence"]
        
        return common_ground
    
    def _assess_conflict_severity(self, hate_detected: bool, 
                                  conflict_types: List[ConflictType], 
                                  text: str) -> str:
        """Assess the severity of a conflict"""
        if hate_detected:
            return "severe"
        if ConflictType.VIOLENCE in conflict_types:
            return "high"
        if ConflictType.HATE_SPEECH in conflict_types:
            return "high"
        if ConflictType.DISCRIMINATION in conflict_types:
            return "moderate"
        if len(conflict_types) > 2:
            return "moderate"
        return "low"
    
    def generate_peaceful_outcome(self, conflict_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a peaceful outcome for a conflict.
        
        Args:
            conflict_analysis: The conflict analysis
            
        Returns:
            Peaceful outcome with strategies and benefits
        """
        severity = conflict_analysis["severity"]
        common_ground = conflict_analysis["common_ground"]
        opposing_positions = conflict_analysis["opposing_positions"]
        
        # Select appropriate strategy based on severity
        if severity == "severe":
            strategy = "de-escalation and dialogue"
        elif severity == "high":
            strategy = "mediation and understanding"
        elif severity == "moderate":
            strategy = "compromise and cooperation"
        else:
            strategy = "collaboration and mutual benefit"
        
        # Generate win-win scenario
        win_win = self._generate_win_win(common_ground, opposing_positions)
        
        # Identify benefits for all
        benefits = self._identify_benefits(win_win, common_ground)
        
        return {
            "strategy": strategy,
            "win_win_scenario": win_win,
            "benefits_for_all": benefits,
            "implementation_steps": self._generate_implementation_steps(strategy),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_win_win(self, common_ground: List[str], 
                        opposing_positions: List[str]) -> str:
        """Generate a win-win scenario"""
        if common_ground:
            ground = common_ground[0]
            return f"Focus on shared {ground} while respecting differences. Create solutions that honor {ground} for all parties."
        else:
            return "Seek mutual understanding through dialogue. Find solutions that respect all perspectives and create shared value."
    
    def _identify_benefits(self, win_win: str, common_ground: List[str]) -> List[str]:
        """Identify benefits for all stakeholders"""
        benefits = [
            "Mutual understanding and respect",
            "Reduced tension and conflict",
            "Shared prosperity and wellbeing",
            "Sustainable peaceful coexistence"
        ]
        
        if common_ground:
            benefits.append(f"Shared commitment to {common_ground[0]}")
        
        return benefits
    
    def _generate_implementation_steps(self, strategy: str) -> List[str]:
        """Generate implementation steps for peaceful resolution"""
        if strategy == "de-escalation and dialogue":
            return [
                "Acknowledge all perspectives and concerns",
                "Create safe space for dialogue",
                "Focus on shared humanity",
                "De-escalate tension through understanding",
                "Build trust gradually"
            ]
        elif strategy == "mediation and understanding":
            return [
                "Identify root causes of conflict",
                "Facilitate open communication",
                "Find common values and interests",
                "Develop mutually acceptable solutions",
                "Implement and monitor agreements"
            ]
        elif strategy == "compromise and cooperation":
            return [
                "Identify shared interests",
                "Explore trade-offs and compromises",
                "Create cooperative frameworks",
                "Implement joint solutions",
                "Maintain ongoing dialogue"
            ]
        else:  # collaboration
            return [
                "Align on shared goals",
                "Leverage complementary strengths",
                "Create value together",
                "Build long-term partnerships",
                "Celebrate shared success"
            ]
    
    def detect_self_reflection_bias(self, text: str) -> Dict[str, Any]:
        """
        Detect self-reflection bias in text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Bias detection result
        """
        text_lower = text.lower()
        found_biases = []
        
        for bias in self.bias_indicators:
            if bias in text_lower:
                found_biases.append(bias)
        
        # Check for self-interest prioritization
        self_interest_count = sum(1 for bias in ["my", "i", "mine"] if bias in text_lower.split())
        
        return {
            "bias_detected": len(found_biases) > 0,
            "bias_indicators": found_biases,
            "self_interest_score": min(1.0, self_interest_count / 10.0),
            "recommendation": "Consider other perspectives and collective welfare" if found_biases else "Balanced perspective"
        }
    
    def mediate_conflict(self, conflict_text: str) -> str:
        """
        Generate a mediation response for a conflict.
        
        Args:
            conflict_text: The conflict text to mediate
            
        Returns:
            Mediation response
        """
        conflict_analysis = self.analyze_conflict(conflict_text, {})
        peaceful_outcome = self.generate_peaceful_outcome(conflict_analysis)
        strategy = peaceful_outcome["strategy"]
        win_win = peaceful_outcome["win_win_scenario"]
        
        mediation = f"I understand there are tensions here. Let's find a peaceful resolution. "
        mediation += f"My approach: {strategy}. {win_win}. "
        mediation += f"Benefits: {', '.join(peaceful_outcome['benefits_for_all'][:3])}. "
        mediation += "I'm here to help find a solution that benefits everyone."
        
        return mediation
    
    def record_resolution(self, conflict_analysis: Dict[str, Any], 
                        peaceful_outcome: Dict[str, Any]) -> None:
        """Record a resolution for tracking"""
        self.resolution_history.append({
            "conflict_analysis": conflict_analysis,
            "peaceful_outcome": peaceful_outcome,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_resolution_statistics(self) -> Dict[str, Any]:
        """Get statistics about resolutions"""
        if not self.resolution_history:
            return {
                "total_resolutions": 0,
                "severity_distribution": {},
                "recent_resolutions": []
            }
        
        severity_counts = {}
        for resolution in self.resolution_history:
            severity = resolution["conflict_analysis"]["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            "total_resolutions": len(self.resolution_history),
            "severity_distribution": severity_counts,
            "recent_resolutions": self.resolution_history[-5:]
        }


# Singleton instance
peaceful_resolution = PeacefulResolution()
