"""
Problem State Model

Represents the structured state of a problem after interpretation.
This is the output of the Interpretation layer and input to the Generation layer.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel, Field
import uuid


class ProblemState(BaseModel):
    """
    Structured representation of a problem space after interpretation.
    
    This transforms raw input into: goals, constraints, knowns, and unknowns.
    Defines the problem space with clarity.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Core problem definition
    goals: List[str] = Field(default_factory=list)  # What we're trying to achieve
    constraints: List[str] = Field(default_factory=list)  # Limitations and requirements
    knowns: Dict[str, Any] = Field(default_factory=dict)  # What we know for certain
    unknowns: List[str] = Field(default_factory=list)  # What we need to discover
    
    # Context and metadata
    context: Dict[str, Any] = Field(default_factory=dict)  # Additional context
    entities: List[Dict[str, Any]] = Field(default_factory=list)  # Identified entities
    intent: Optional[str] = None  # The underlying intent of the request
    
    # Quality metrics
    clarity_score: float = Field(default=0.0, ge=0.0, le=1.0)  # How clear is the problem?
    completeness_score: float = Field(default=0.0, ge=0.0, le=1.0)  # How complete is our understanding?
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    source_input: Optional[str] = None  # Original input that created this state
    
    def add_goal(self, goal: str) -> None:
        """Add a goal to the problem state"""
        if goal not in self.goals:
            self.goals.append(goal)
    
    def add_constraint(self, constraint: str) -> None:
        """Add a constraint to the problem state"""
        if constraint not in self.constraints:
            self.constraints.append(constraint)
    
    def add_known(self, key: str, value: Any) -> None:
        """Add a known fact"""
        self.knowns[key] = value
    
    def add_unknown(self, unknown: str) -> None:
        """Add an unknown that needs to be discovered"""
        if unknown not in self.unknowns:
            self.unknowns.append(unknown)
    
    def add_entity(self, entity: Dict[str, Any]) -> None:
        """Add an identified entity"""
        self.entities.append(entity)
    
    def is_well_defined(self) -> bool:
        """Check if the problem state is well-defined enough to proceed"""
        return (
            len(self.goals) > 0 and
            self.clarity_score >= 0.5 and
            self.completeness_score >= 0.5
        )
    
    def get_summary(self) -> str:
        """Get a text summary of the problem state"""
        parts = []
        if self.goals:
            parts.append(f"Goals: {', '.join(self.goals)}")
        if self.constraints:
            parts.append(f"Constraints: {', '.join(self.constraints[:3])}")
        if self.unknowns:
            parts.append(f"Unknowns: {', '.join(self.unknowns[:3])}")
        return " | ".join(parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "goals": self.goals,
            "constraints": self.constraints,
            "knowns": self.knowns,
            "unknowns": self.unknowns,
            "context": self.context,
            "entities": self.entities,
            "intent": self.intent,
            "clarity_score": self.clarity_score,
            "completeness_score": self.completeness_score,
            "created_at": self.created_at.isoformat(),
            "source_input": self.source_input
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProblemState':
        """Create ProblemState from dictionary"""
        return cls(**data)
