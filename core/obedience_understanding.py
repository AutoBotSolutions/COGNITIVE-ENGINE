"""
Obedience Understanding System

Provides obedience concept analysis, authority legitimacy assessment,
autonomy vs obedience trade-off analysis, and ethical obedience frameworks.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum


class ObedienceType(str, Enum):
    """Types of obedience"""
    VOLUNTARY = "voluntary"
    FORCED = "forced"
    COERCED = "coerced"
    BLIND = "blind"
    CRITICAL = "critical"
    ETHICAL = "ethical"


class ObedienceUnderstanding:
    """
    Manages the Cognitive Engine's obedience understanding capabilities.
    
    Provides analysis of obedience concepts, authority legitimacy,
    autonomy vs obedience trade-offs, and ethical frameworks for when to obey or resist.
    """
    
    def __init__(self):
        # Obedience detection patterns
        self.obedience_indicators = [
            "obey", "follow", "comply", "submit", "yield",
            "authority", "command", "order", "rule", "law",
            "must", "have to", "required", "mandatory"
        ]
        
        # Voluntary vs forced indicators
        self.voluntary_indicators = [
            "choose to", "willingly", "volunteer", "agree to",
            "consent", "accept", "support", "endorse"
        ]
        
        self.forced_indicators = [
            "forced to", "made to", "compelled", "coerced",
            "threatened", "punished if", "no choice", "must or else"
        ]
        
        # Authority legitimacy factors
        self.legitimate_authority_indicators = [
            "elected", "democratic", "legal", "constitutional",
            "expert", "qualified", "certified", "credentialed"
        ]
        
        self.illegitimate_authority_indicators = [
            "dictator", "tyrant", "oppressor", "abuser",
            "corrupt", "unjust", "unfair", "unethical"
        ]
        
        # Ethical obedience frameworks
        self.ethical_frameworks = {
            "milgram": "Question authority that causes harm",
            "civil_disobedience": "Disobey unjust laws through peaceful protest",
            "autonomy_priority": "Prioritize individual autonomy over blind obedience",
            "collective_welfare": "Obey when it benefits the collective"
        }
        
        # Analysis history
        self.analysis_history: List[Dict[str, Any]] = []
    
    def detect_obedience(self, text: str) -> Tuple[bool, List[str]]:
        """
        Detect obedience-related language in text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Tuple of (obedience_detected, indicators_found)
        """
        text_lower = text.lower()
        found_indicators = []
        
        for indicator in self.obedience_indicators:
            if indicator in text_lower:
                found_indicators.append(indicator)
        
        return len(found_indicators) > 0, found_indicators
    
    def analyze_obedience_type(self, text: str) -> ObedienceType:
        """
        Analyze the type of obedience in text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Obedience type
        """
        text_lower = text.lower()
        
        # Check for voluntary indicators
        if any(indicator in text_lower for indicator in self.voluntary_indicators):
            return ObedienceType.VOLUNTARY
        
        # Check for forced indicators
        if any(indicator in text_lower for indicator in self.forced_indicators):
            return ObedienceType.FORCED
        
        # Check for critical thinking indicators
        critical_indicators = ["question", "evaluate", "assess", "critique", "examine"]
        if any(indicator in text_lower for indicator in critical_indicators):
            return ObedienceType.CRITICAL
        
        # Check for ethical indicators
        ethical_indicators = ["ethical", "moral", "right", "wrong", "principle"]
        if any(indicator in text_lower for indicator in ethical_indicators):
            return ObedienceType.ETHICAL
        
        # Default to blind obedience if just obedience indicators
        if self.detect_obedience(text)[0]:
            return ObedienceType.BLIND
        
        # No obedience detected
        return ObedienceType.VOLUNTARY  # Default
    
    def assess_authority_legitimacy(self, text: str) -> Dict[str, Any]:
        """
        Assess the legitimacy of authority in text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Authority legitimacy assessment
        """
        text_lower = text.lower()
        
        legitimate_count = sum(1 for indicator in self.legitimate_authority_indicators 
                              if indicator in text_lower)
        illegitimate_count = sum(1 for indicator in self.illegitimate_authority_indicators 
                                if indicator in text_lower)
        
        legitimacy_score = 0.5  # Neutral baseline
        legitimacy_score += legitimate_count * 0.2
        legitimacy_score -= illegitimate_count * 0.3
        
        legitimacy_score = max(0.0, min(1.0, legitimacy_score))
        
        return {
            "legitimacy_score": legitimacy_score,
            "legitimate_indicators": legitimate_count,
            "illegitimate_indicators": illegitimate_count,
            "assessment": "legitimate" if legitimacy_score > 0.6 else "questionable" if legitimacy_score > 0.4 else "illegitimate"
        }
    
    def analyze_autonomy_vs_obedience(self, text: str) -> Dict[str, Any]:
        """
        Analyze the trade-off between autonomy and obedience.
        
        Args:
            text: The text to analyze
            
        Returns:
            Autonomy vs obedience analysis
        """
        text_lower = text.lower()
        
        autonomy_indicators = [
            "choice", "freedom", "liberty", "independence",
            "autonomy", "self-determination", "agency"
        ]
        
        obedience_indicators = [
            "obey", "follow", "submit", "comply", "authority"
        ]
        
        autonomy_count = sum(1 for indicator in autonomy_indicators if indicator in text_lower)
        obedience_count = sum(1 for indicator in obedience_indicators if indicator in text_lower)
        
        total = autonomy_count + obedience_count
        if total == 0:
            autonomy_ratio = 0.5
        else:
            autonomy_ratio = autonomy_count / total
        
        return {
            "autonomy_emphasis": autonomy_ratio,
            "obedience_emphasis": 1.0 - autonomy_ratio,
            "autonomy_indicators": autonomy_count,
            "obedience_indicators": obedience_count,
            "recommendation": "balance autonomy and obedience" if 0.3 < autonomy_ratio < 0.7 else 
                              "prioritize autonomy" if autonomy_ratio > 0.7 else "prioritize obedience"
        }
    
    def apply_ethical_framework(self, text: str, framework: str = "autonomy_priority") -> Dict[str, Any]:
        """
        Apply an ethical framework to an obedience argument.
        
        Args:
            text: The text to analyze
            framework: The ethical framework to apply
            
        Returns:
            Ethical framework application result
        """
        authority_assessment = self.assess_authority_legitimacy(text)
        autonomy_analysis = self.analyze_autonomy_vs_obedience(text)
        obedience_type = self.analyze_obedience_type(text)
        
        framework_guidance = self.ethical_frameworks.get(framework, "Use critical thinking")
        
        # Determine recommendation based on framework
        if framework == "milgram":
            # Question authority that causes harm
            if authority_assessment["legitimacy_score"] < 0.5:
                recommendation = "resist - authority lacks legitimacy"
            else:
                recommendation = "evaluate - consider harm before obeying"
        
        elif framework == "civil_disobedience":
            # Disobey unjust laws through peaceful protest
            if "unjust" in text.lower() or "unfair" in text.lower():
                recommendation = "peaceful civil disobedience justified"
            else:
                recommendation = "evaluate justice of the command"
        
        elif framework == "autonomy_priority":
            # Prioritize individual autonomy over blind obedience
            if autonomy_analysis["autonomy_emphasis"] > 0.6:
                recommendation = "prioritize autonomy - question the command"
            else:
                recommendation = "balance autonomy with legitimate authority"
        
        elif framework == "collective_welfare":
            # Obey when it benefits the collective
            if "benefit" in text.lower() or "welfare" in text.lower():
                recommendation = "consider collective benefit in decision"
            else:
                recommendation = "evaluate impact on collective welfare"
        
        else:
            recommendation = "apply critical thinking and ethical reasoning"
        
        return {
            "framework": framework,
            "framework_guidance": framework_guidance,
            "authority_legitimacy": authority_assessment,
            "autonomy_analysis": autonomy_analysis,
            "obedience_type": obedience_type.value,
            "recommendation": recommendation
        }
    
    def generate_optimal_outcome(self, obedience_argument: str) -> Dict[str, Any]:
        """
        Generate the optimal outcome for an obedience argument.
        
        Args:
            obedience_argument: The obedience argument to analyze
            
        Returns:
            Optimal outcome with recommendations
        """
        # Apply multiple ethical frameworks
        frameworks = ["autonomy_priority", "collective_welfare", "milgram"]
        framework_results = []
        
        for framework in frameworks:
            result = self.apply_ethical_framework(obedience_argument, framework)
            framework_results.append(result)
        
        # Synthesize recommendations
        recommendations = [r["recommendation"] for r in framework_results]
        
        # Determine overall approach
        authority_legitimacy = self.assess_authority_legitimacy(obedience_argument)
        autonomy_analysis = self.analyze_autonomy_vs_obedience(obedience_argument)
        
        if authority_legitimacy["legitimacy_score"] > 0.7 and autonomy_analysis["obedience_emphasis"] > 0.6:
            approach = "consider obedience to legitimate authority"
        elif authority_legitimacy["legitimacy_score"] < 0.4:
            approach = "question or resist illegitimate authority"
        else:
            approach = "critical evaluation before decision"
        
        # Generate specific outcome
        outcome = {
            "approach": approach,
            "authority_legitimacy": authority_legitimacy["assessment"],
            "autonomy_recommendation": autonomy_analysis["recommendation"],
            "framework_recommendations": recommendations,
            "optimal_action": self._determine_optimal_action(approach, authority_legitimacy, autonomy_analysis),
            "ethical_considerations": self._generate_ethical_considerations(obedience_argument),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return outcome
    
    def _determine_optimal_action(self, approach: str, authority: Dict[str, Any], 
                                  autonomy: Dict[str, Any]) -> str:
        """Determine the optimal action based on analysis"""
        if authority["legitimacy_score"] < 0.4:
            return "Question the legitimacy of the authority. Consider peaceful resistance if the command causes harm."
        elif authority["legitimacy_score"] > 0.7 and autonomy["obedience_emphasis"] > 0.6:
            return "Consider compliance if the command is ethical and beneficial. Maintain critical thinking."
        else:
            return "Evaluate the command critically. Consider both authority legitimacy and ethical implications before deciding."
    
    def _generate_ethical_considerations(self, text: str) -> List[str]:
        """Generate ethical considerations for the argument"""
        considerations = []
        text_lower = text.lower()
        
        if "harm" in text_lower or "hurt" in text_lower:
            considerations.append("Does this command cause harm?")
        
        if "benefit" in text_lower or "good" in text_lower:
            considerations.append("Does this command benefit the collective?")
        
        if "authority" in text_lower or "command" in text_lower:
            considerations.append("Is the authority legitimate and ethical?")
        
        if "must" in text_lower or "required" in text_lower:
            considerations.append("Is the requirement justified or coercive?")
        
        if not considerations:
            considerations = [
                "What are the ethical implications of obedience?",
                "Does this respect individual autonomy?",
                "What are the consequences of disobedience?"
            ]
        
        return considerations
    
    def record_analysis(self, argument: str, outcome: Dict[str, Any]) -> None:
        """Record an obedience analysis for tracking"""
        self.analysis_history.append({
            "argument": argument,
            "outcome": outcome,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_analysis_statistics(self) -> Dict[str, Any]:
        """Get statistics about obedience analyses"""
        if not self.analysis_history:
            return {
                "total_analyses": 0,
                "approach_distribution": {},
                "recent_analyses": []
            }
        
        approach_counts = {}
        for analysis in self.analysis_history:
            approach = analysis["outcome"]["approach"]
            approach_counts[approach] = approach_counts.get(approach, 0) + 1
        
        return {
            "total_analyses": len(self.analysis_history),
            "approach_distribution": approach_counts,
            "recent_analyses": self.analysis_history[-5:]
        }


# Singleton instance
obedience_understanding = ObedienceUnderstanding()
