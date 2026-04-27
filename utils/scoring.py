"""
Scoring functions for evaluating thoughts

Provides various scoring mechanisms for thought evaluation in the deliberation layer.
"""

from typing import Dict, Any, List
from models.thought import Thought
from models.state import ProblemState


class ThoughtScorer:
    """
    Scores thoughts based on multiple criteria.
    """
    
    def __init__(self):
        self.weights = {
            "coherence": 0.3,
            "relevance": 0.25,
            "novelty": 0.15,
            "feasibility": 0.2,
            "completeness": 0.1
        }
    
    def score(self, thought: Thought, state: ProblemState) -> float:
        """
        Calculate overall score for a thought.
        
        Args:
            thought: The thought to score
            state: The current problem state
            
        Returns:
            Overall score (0.0 to 1.0)
        """
        scores = {
            "coherence": self.score_coherence(thought),
            "relevance": self.score_relevance(thought, state),
            "novelty": self.score_novelty(thought, state),
            "feasibility": self.score_feasibility(thought, state),
            "completeness": self.score_completeness(thought, state)
        }
        
        # Weighted sum
        total = sum(scores[key] * self.weights[key] for key in scores)
        
        # Store scores in thought metadata
        thought.metadata["scores"] = scores
        thought.metadata["overall_score"] = total
        
        return total
    
    def score_coherence(self, thought: Thought) -> float:
        """Score based on internal logical consistency"""
        # Check if premise is well-formed
        if not thought.premise or len(thought.premise) < 10:
            return 0.0
        
        # Check for contradictions in weaknesses
        if len(thought.weaknesses) > 5:
            return 0.3
        
        # Base score for having a clear premise
        base_score = 0.7
        
        # Bonus for having history
        if thought.history:
            base_score += 0.1
        
        # Penalty for too many weaknesses
        base_score -= min(0.3, len(thought.weaknesses) * 0.05)
        
        return max(0.0, min(1.0, base_score))
    
    def score_relevance(self, thought: Thought, state: ProblemState) -> float:
        """Score based on relevance to problem goals"""
        if not state.goals:
            return 0.5
        
        # Check if thought addresses any goals
        premise_lower = thought.premise.lower()
        relevance_count = 0
        
        for goal in state.goals:
            if any(word in premise_lower for word in goal.lower().split()):
                relevance_count += 1
        
        # Normalize
        return min(1.0, relevance_count / max(1, len(state.goals)))
    
    def score_novelty(self, thought: Thought, state: ProblemState) -> float:
        """Score based on novelty compared to knowns"""
        if not state.knowns:
            return 0.8  # High novelty if no knowns
        
        premise_lower = thought.premise.lower()
        
        # Check if thought introduces new information
        novelty_count = 0
        for key, value in state.knowns.items():
            if str(value).lower() not in premise_lower:
                novelty_count += 1
        
        return min(1.0, novelty_count / max(1, len(state.knowns)))
    
    def score_feasibility(self, thought: Thought, state: ProblemState) -> float:
        """Score based on feasibility given constraints"""
        if not state.constraints:
            return 0.8  # High feasibility if no constraints
        
        premise_lower = thought.premise.lower()
        
        # Check if thought respects constraints
        violations = 0
        for constraint in state.constraints:
            if "not" in constraint.lower():
                # Negative constraint - check if thought violates it
                if any(word in premise_lower for word in constraint.lower().split()):
                    violations += 1
        
        if violations > 0:
            return max(0.0, 1.0 - (violations * 0.3))
        
        return 0.8
    
    def score_completeness(self, thought: Thought, state: ProblemState) -> float:
        """Score based on addressing unknowns"""
        if not state.unknowns:
            return 1.0  # Complete if no unknowns
        
        premise_lower = thought.premise.lower()
        
        # Check if thought addresses unknowns
        addressed_count = 0
        for unknown in state.unknowns:
            if any(word in premise_lower for word in unknown.lower().split()):
                addressed_count += 1
        
        return min(1.0, addressed_count / max(1, len(state.unknowns)))
    
    def compare_thoughts(self, thought1: Thought, thought2: Thought) -> int:
        """
        Compare two thoughts by score.
        
        Returns:
            -1 if thought1 < thought2, 1 if thought1 > thought2, 0 if equal
        """
        if thought1.score < thought2.score:
            return -1
        elif thought1.score > thought2.score:
            return 1
        return 0
    
    def rank_thoughts(self, thoughts: List[Thought]) -> List[Thought]:
        """Rank thoughts by score (highest first)"""
        return sorted(thoughts, key=lambda t: t.score, reverse=True)
