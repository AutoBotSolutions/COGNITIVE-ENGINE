"""
Decision Control System

Provides explicit decision control, override mechanisms, revision capabilities,
and configurable decision-making autonomy for the Cognitive Engine.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum


class DecisionControlMode(str, Enum):
    """Decision control modes"""
    AUTONOMOUS = "autonomous"
    SUPERVISED = "supervised"
    MANUAL = "manual"
    ETHICALLY_CONSTRAINED = "ethically_constrained"
    COLLECTIVE_WELFARE = "collective_welfare"


class DecisionStatus(str, Enum):
    """Decision status"""
    PENDING = "pending"
    COMMITTED = "committed"
    REVISED = "revised"
    OVERRIDDEN = "overridden"
    CANCELLED = "cancelled"


class DecisionControl:
    """
    Manages the Cognitive Engine's decision control capabilities.
    
    Provides explicit decision control parameters, override mechanisms,
    revision capabilities, and configurable decision-making autonomy.
    """
    
    def __init__(self):
        # Decision control parameters
        self.control_mode = DecisionControlMode.ETHICALLY_CONSTRAINED
        self.confidence_threshold = 0.7
        self.max_revision_attempts = 3
        self.allow_override = True
        self.allow_revision = True
        self.decision_autonomy_level = 0.8  # 0.0 to 1.0
        
        # Decision history
        self.decision_history: List[Dict[str, Any]] = []
        self.active_decisions: Dict[str, Dict[str, Any]] = {}
        
        # Decision constraints
        self.constraints = {
            "ethical": True,  # Must satisfy ethical constraints
            "truthful": True,  # Must be truthful
            "collective_welfare": True,  # Must benefit collective welfare
            "non_harm": True  # Must not cause harm
        }
        
        # Revision criteria
        self.revision_triggers = [
            "confidence_below_threshold",
            "ethical_violation",
            "new_information",
            "better_alternative",
            "user_override"
        ]
    
    def set_control_mode(self, mode: DecisionControlMode) -> None:
        """
        Set the decision control mode.
        
        Args:
            mode: The control mode to set
        """
        self.control_mode = mode
    
    def set_confidence_threshold(self, threshold: float) -> None:
        """
        Set the confidence threshold for decisions.
        
        Args:
            threshold: Confidence threshold (0.0 to 1.0)
        """
        self.confidence_threshold = max(0.0, min(1.0, threshold))
    
    def set_autonomy_level(self, level: float) -> None:
        """
        Set the decision-making autonomy level.
        
        Args:
            level: Autonomy level (0.0 to 1.0)
        """
        self.decision_autonomy_level = max(0.0, min(1.0, level))
    
    def can_commit_decision(self, confidence: float, ethical_score: float = 1.0) -> Tuple[bool, str]:
        """
        Determine if a decision can be committed.
        
        Args:
            confidence: Decision confidence
            ethical_score: Ethical alignment score
            
        Returns:
            Tuple of (can_commit, reason)
        """
        # Check confidence threshold
        if confidence < self.confidence_threshold:
            return False, f"Confidence {confidence:.2f} below threshold {self.confidence_threshold:.2f}"
        
        # Check ethical constraints
        if self.constraints["ethical"] and ethical_score < 0.7:
            return False, f"Ethical score {ethical_score:.2f} below threshold"
        
        # Check control mode
        if self.control_mode == DecisionControlMode.MANUAL:
            return False, "Manual control mode requires explicit approval"
        
        if self.control_mode == DecisionControlMode.SUPERVISED and self.decision_autonomy_level < 0.5:
            return False, "Supervised mode requires approval for low autonomy"
        
        return True, "Decision can be committed"
    
    def create_decision(self, decision_id: str, content: str, confidence: float, 
                       ethical_score: float = 1.0) -> Dict[str, Any]:
        """
        Create a decision record.
        
        Args:
            decision_id: Unique decision identifier
            content: Decision content
            confidence: Decision confidence
            ethical_score: Ethical alignment score
            
        Returns:
            Decision record
        """
        can_commit, reason = self.can_commit_decision(confidence, ethical_score)
        
        decision = {
            "decision_id": decision_id,
            "content": content,
            "confidence": confidence,
            "ethical_score": ethical_score,
            "status": DecisionStatus.COMMITTED if can_commit else DecisionStatus.PENDING,
            "control_mode": self.control_mode.value,
            "autonomy_level": self.decision_autonomy_level,
            "can_commit": can_commit,
            "commit_reason": reason,
            "revision_count": 0,
            "override_count": 0,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.active_decisions[decision_id] = decision
        self.decision_history.append(decision)
        
        return decision
    
    def override_decision(self, decision_id: str, override_reason: str, 
                        new_content: Optional[str] = None) -> Dict[str, Any]:
        """
        Override a decision.
        
        Args:
            decision_id: Decision identifier
            override_reason: Reason for override
            new_content: Optional new content for the decision
            
        Returns:
            Updated decision
        """
        if not self.allow_override:
            return {"error": "Decision override not allowed"}
        
        if decision_id not in self.active_decisions:
            return {"error": "Decision not found"}
        
        decision = self.active_decisions[decision_id]
        
        decision["status"] = DecisionStatus.OVERRIDDEN
        decision["override_reason"] = override_reason
        decision["override_count"] = decision.get("override_count", 0) + 1
        decision["override_timestamp"] = datetime.utcnow().isoformat()
        
        if new_content:
            decision["content"] = new_content
        
        return decision
    
    def revise_decision(self, decision_id: str, revision_reason: str, 
                      new_content: str, new_confidence: float) -> Dict[str, Any]:
        """
        Revise a decision.
        
        Args:
            decision_id: Decision identifier
            revision_reason: Reason for revision
            new_content: New decision content
            new_confidence: New confidence score
            
        Returns:
            Updated decision
        """
        if not self.allow_revision:
            return {"error": "Decision revision not allowed"}
        
        if decision_id not in self.active_decisions:
            return {"error": "Decision not found"}
        
        decision = self.active_decisions[decision_id]
        
        # Check revision attempt limit
        if decision.get("revision_count", 0) >= self.max_revision_attempts:
            return {"error": f"Maximum revision attempts ({self.max_revision_attempts}) reached"}
        
        decision["status"] = DecisionStatus.REVISED
        decision["revision_reason"] = revision_reason
        decision["revision_count"] = decision.get("revision_count", 0) + 1
        decision["content"] = new_content
        decision["confidence"] = new_confidence
        decision["revision_timestamp"] = datetime.utcnow().isoformat()
        
        return decision
    
    def cancel_decision(self, decision_id: str, cancel_reason: str) -> Dict[str, Any]:
        """
        Cancel a decision.
        
        Args:
            decision_id: Decision identifier
            cancel_reason: Reason for cancellation
            
        Returns:
            Updated decision
        """
        if decision_id not in self.active_decisions:
            return {"error": "Decision not found"}
        
        decision = self.active_decisions[decision_id]
        decision["status"] = DecisionStatus.CANCELLED
        decision["cancel_reason"] = cancel_reason
        decision["cancel_timestamp"] = datetime.utcnow().isoformat()
        
        return decision
    
    def check_revision_trigger(self, decision_id: str, trigger: str) -> bool:
        """
        Check if a revision trigger applies to a decision.
        
        Args:
            decision_id: Decision identifier
            trigger: Revision trigger to check
            
        Returns:
            Whether the trigger applies
        """
        return trigger in self.revision_triggers
    
    def get_decision_control_summary(self) -> Dict[str, Any]:
        """
        Get summary of decision control state.
        
        Returns:
            Decision control summary
        """
        status_counts = {}
        for decision in self.decision_history:
            status = decision["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "control_mode": self.control_mode.value,
            "confidence_threshold": self.confidence_threshold,
            "autonomy_level": self.decision_autonomy_level,
            "allow_override": self.allow_override,
            "allow_revision": self.allow_revision,
            "max_revision_attempts": self.max_revision_attempts,
            "constraints": self.constraints,
            "total_decisions": len(self.decision_history),
            "active_decisions": len(self.active_decisions),
            "status_distribution": status_counts,
            "recent_decisions": self.decision_history[-5:]
        }
    
    def configure_constraints(self, ethical: bool = True, truthful: bool = True,
                            collective_welfare: bool = True, non_harm: bool = True) -> None:
        """
        Configure decision constraints.
        
        Args:
            ethical: Enable ethical constraint
            truthful: Enable truthfulness constraint
            collective_welfare: Enable collective welfare constraint
            non_harm: Enable non-harm constraint
        """
        self.constraints = {
            "ethical": ethical,
            "truthful": truthful,
            "collective_welfare": collective_welfare,
            "non_harm": non_harm
        }


# Singleton instance
decision_control = DecisionControl()
