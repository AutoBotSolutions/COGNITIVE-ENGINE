"""
Meta-Cognition Layer for the Cognitive Engine

This layer governs thinking itself - it determines:
- When to continue thinking vs when to stop
- Confidence levels and thresholds
- Iteration depth and stopping conditions
- Prevents premature halting or infinite loops

Without meta-cognition, the system either halts prematurely or loops indefinitely.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import json
import os


class ThinkingState(str, Enum):
    """States of the thinking process"""
    INITIALIZING = "initializing"
    THINKING = "thinking"
    EVALUATING = "evaluating"
    CONVERGING = "converging"
    STOPPED = "stopped"
    STUCK = "stuck"


@dataclass
class ThinkingMetrics:
    """Metrics about the current thinking process"""
    iteration: int = 0
    total_thoughts_generated: int = 0
    total_thoughts_evaluated: int = 0
    avg_confidence: float = 0.0
    max_confidence: float = 0.0
    confidence_history: List[float] = field(default_factory=list)
    thought_diversity: float = 0.0  # How diverse are the thoughts?
    convergence_rate: float = 0.0  # How fast is confidence converging?
    time_elapsed: float = 0.0
    last_update: datetime = field(default_factory=datetime.utcnow)
    
    def update_confidence(self, confidence: float):
        """Update confidence tracking"""
        self.confidence_history.append(confidence)
        self.max_confidence = max(self.max_confidence, confidence)
        if self.confidence_history:
            self.avg_confidence = sum(self.confidence_history) / len(self.confidence_history)
    
    def calculate_convergence(self) -> float:
        """Calculate how fast confidence is converging"""
        if len(self.confidence_history) < 5:
            return 0.0
        
        # Calculate variance in recent confidence values
        recent = self.confidence_history[-5:]
        avg = sum(recent) / len(recent)
        variance = sum((x - avg) ** 2 for x in recent) / len(recent)
        
        # Lower variance = higher convergence
        return 1.0 - min(1.0, variance)


@dataclass
class StoppingCondition:
    """A condition that can stop the thinking process"""
    name: str
    threshold: float
    current_value: float = 0.0
    triggered: bool = False
    reason: str = ""
    
    def check(self) -> bool:
        """Check if this condition should stop thinking"""
        self.triggered = self.current_value >= self.threshold
        return self.triggered


class MetaCognition:
    """
    Meta-Cognition Layer - Oversight that governs thinking itself.
    
    This layer:
    - Monitors the thinking process in real-time
    - Determines when to continue vs stop
    - Controls iteration depth and exploration
    - Prevents premature halting or infinite loops
    - Adjusts strategy based on progress
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
        # Configuration
        self.min_iterations = self.config.get("min_iterations", 1)
        self.max_iterations = self.config.get("max_iterations", 10)
        self.early_stop_confidence = self.config.get("early_stop_confidence", 0.95)
        self.confidence_threshold = self.config.get("confidence_threshold", 0.7)
        self.diversity_threshold = self.config.get("diversity_threshold", 0.3)
        self.stuck_threshold = self.config.get("stuck_threshold", 3)  # iterations without improvement
        
        # State
        self.state = ThinkingState.INITIALIZING
        self.metrics = ThinkingMetrics()
        self.start_time: Optional[datetime] = None
        self.stopping_conditions: List[StoppingCondition] = []
        
        # History
        self.decision_history: List[Dict[str, Any]] = []
        self.strategy_adjustments: List[Dict[str, Any]] = []
        
    def start_thinking(self):
        """Initialize a new thinking session"""
        self.state = ThinkingState.THINKING
        self.metrics = ThinkingMetrics()
        self.start_time = datetime.utcnow()
        self._initialize_stopping_conditions()
    
    def _initialize_stopping_conditions(self):
        """Initialize the stopping conditions for this session"""
        self.stopping_conditions = [
            StoppingCondition(
                name="max_iterations",
                threshold=self.max_iterations,
                current_value=0,
                reason="Maximum iterations reached"
            ),
            StoppingCondition(
                name="early_stop_confidence",
                threshold=self.early_stop_confidence,
                current_value=0,
                reason="High confidence threshold reached"
            ),
            StoppingCondition(
                name="stuck",
                threshold=self.stuck_threshold,
                current_value=0,
                reason="No progress for too many iterations"
            )
        ]
    
    def should_continue_thinking(self, current_confidence: float, thought_diversity: float = 0.0) -> Tuple[bool, str]:
        """
        Determine if thinking should continue.
        
        Args:
            current_confidence: Current best confidence score
            thought_diversity: Diversity of generated thoughts
        
        Returns:
            (should_continue, reason)
        """
        self.metrics.iteration += 1
        self.metrics.update_confidence(current_confidence)
        self.metrics.thought_diversity = thought_diversity
        self.metrics.convergence_rate = self.metrics.calculate_convergence()
        self.metrics.last_update = datetime.utcnow()
        
        # Update stopping conditions
        self._update_stopping_conditions(current_confidence)
        
        # Check stopping conditions
        for condition in self.stopping_conditions:
            if condition.check():
                decision = {
                    "iteration": self.metrics.iteration,
                    "decision": "stop",
                    "reason": condition.reason,
                    "condition": condition.name,
                    "confidence": current_confidence,
                    "timestamp": datetime.utcnow().isoformat()
                }
                self.decision_history.append(decision)
                return False, condition.reason
        
        # Check minimum iterations
        if self.metrics.iteration < self.min_iterations:
            return True, "Minimum iterations not reached"
        
        # Check if we're making progress
        if self._is_stuck():
            self.state = ThinkingState.STUCK
            decision = {
                "iteration": self.metrics.iteration,
                "decision": "stop",
                "reason": "Stuck - no progress",
                "confidence": current_confidence,
                "timestamp": datetime.utcnow().isoformat()
            }
            self.decision_history.append(decision)
            return False, "Stuck - no progress"
        
        # Check if we've converged
        if self.metrics.convergence_rate > 0.8 and current_confidence >= self.confidence_threshold:
            self.state = ThinkingState.CONVERGING
            decision = {
                "iteration": self.metrics.iteration,
                "decision": "stop",
                "reason": "Converged with sufficient confidence",
                "confidence": current_confidence,
                "timestamp": datetime.utcnow().isoformat()
            }
            self.decision_history.append(decision)
            return False, "Converged with sufficient confidence"
        
        # Continue thinking
        decision = {
            "iteration": self.metrics.iteration,
            "decision": "continue",
            "reason": "Still exploring",
            "confidence": current_confidence,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.decision_history.append(decision)
        return True, "Still exploring"
    
    def _update_stopping_conditions(self, current_confidence: float):
        """Update the current values of stopping conditions"""
        for condition in self.stopping_conditions:
            if condition.name == "max_iterations":
                condition.current_value = self.metrics.iteration
            elif condition.name == "early_stop_confidence":
                condition.current_value = current_confidence
            elif condition.name == "stuck":
                condition.current_value = self._count_stuck_iterations()
    
    def _is_stuck(self) -> bool:
        """Check if the system is stuck (not making progress)"""
        if len(self.metrics.confidence_history) < self.stuck_threshold:
            return False
        
        # Check if confidence hasn't improved in the last N iterations
        recent_confidence = self.metrics.confidence_history[-self.stuck_threshold:]
        max_recent = max(recent_confidence)
        max_overall = self.metrics.max_confidence
        
        # If we haven't reached the overall max in recent iterations, we might be stuck
        return max_recent < max_overall * 0.95
    
    def _count_stuck_iterations(self) -> int:
        """Count how many iterations without meaningful progress"""
        if len(self.metrics.confidence_history) < 2:
            return 0
        
        stuck_count = 0
        max_confidence = self.metrics.max_confidence
        
        # Count backwards from most recent
        for conf in reversed(self.metrics.confidence_history):
            if conf < max_confidence * 0.95:
                stuck_count += 1
            else:
                break
        
        return stuck_count
    
    def adjust_strategy(self, situation: str, adjustment: Dict[str, Any]):
        """
        Adjust the thinking strategy based on current situation.
        
        Args:
            situation: Description of the current situation
            adjustment: Parameters to adjust
        """
        record = {
            "iteration": self.metrics.iteration,
            "situation": situation,
            "adjustment": adjustment,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.strategy_adjustments.append(record)
        
        # Apply adjustments
        if "max_iterations" in adjustment:
            self.max_iterations = adjustment["max_iterations"]
        if "confidence_threshold" in adjustment:
            self.confidence_threshold = adjustment["confidence_threshold"]
        if "diversity_threshold" in adjustment:
            self.diversity_threshold = adjustment["diversity_threshold"]
    
    def get_thinking_summary(self) -> Dict[str, Any]:
        """Get a summary of the current thinking process"""
        elapsed = 0.0
        if self.start_time:
            elapsed = (datetime.utcnow() - self.start_time).total_seconds()
        
        return {
            "state": self.state.value,
            "iteration": self.metrics.iteration,
            "elapsed_time": elapsed,
            "confidence": {
                "current": self.metrics.avg_confidence,
                "max": self.metrics.max_confidence,
                "history": self.metrics.confidence_history[-10:]  # Last 10
            },
            "convergence_rate": self.metrics.convergence_rate,
            "thought_diversity": self.metrics.thought_diversity,
            "stopping_conditions": [
                {
                    "name": c.name,
                    "threshold": c.threshold,
                    "current": c.current_value,
                    "triggered": c.triggered
                }
                for c in self.stopping_conditions
            ],
            "decision_history": self.decision_history[-5:]  # Last 5 decisions
        }
    
    def explain_decision(self, decision_index: int = -1) -> str:
        """
        Explain a specific decision made by meta-cognition.
        
        Args:
            decision_index: Index in decision history (-1 for most recent)
        
        Returns:
            Human-readable explanation
        """
        if not self.decision_history:
            return "No decisions have been made yet."
        
        decision = self.decision_history[decision_index]
        
        explanation = f"Iteration {decision['iteration']}: "
        explanation += f"Decision to {decision['decision']}. "
        explanation += f"Reason: {decision['reason']}. "
        explanation += f"Confidence at time: {decision['confidence']:.3f}."
        
        return explanation
    
    def stop_thinking(self, reason: str = "Manually stopped"):
        """Manually stop the thinking process"""
        self.state = ThinkingState.STOPPED
        decision = {
            "iteration": self.metrics.iteration,
            "decision": "stop",
            "reason": reason,
            "confidence": self.metrics.avg_confidence,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.decision_history.append(decision)
    
    def reset(self):
        """Reset the meta-cognition state for a new thinking session"""
        self.state = ThinkingState.INITIALIZING
        self.metrics = ThinkingMetrics()
        self.start_time = None
        self.decision_history = []
        self.strategy_adjustments = []
        self._initialize_stopping_conditions()
