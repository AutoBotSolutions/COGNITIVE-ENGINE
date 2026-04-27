"""
Pattern Object Model for the Learning System

Represents patterns extracted from experiences.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid


class Pattern(BaseModel):
    """
    Represents a recurring pattern identified in experiences.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pattern_text: str
    pattern_type: str  # e.g., "reasoning_strategy", "failure_mode", "success_pattern"
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    frequency: int = Field(default=1)
    
    # Context
    source_experiences: List[str] = Field(default_factory=list)  # IDs of source experiences
    domain: Optional[str] = None  # Domain this pattern applies to
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_seen: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def increment_frequency(self) -> None:
        """Increment the frequency counter"""
        self.frequency += 1
        self.last_seen = datetime.utcnow()
    
    def update_confidence(self, new_confidence: float) -> None:
        """Update the confidence score"""
        self.confidence = max(0.0, min(1.0, new_confidence))
        self.last_seen = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "pattern_text": self.pattern_text,
            "pattern_type": self.pattern_type,
            "confidence": self.confidence,
            "frequency": self.frequency,
            "source_experiences": self.source_experiences,
            "domain": self.domain,
            "created_at": self.created_at.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Pattern':
        """Create from dictionary"""
        return cls(**data)


class Rule(BaseModel):
    """
    Represents a learned rule derived from patterns.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    rule_text: str
    rule_type: str  # e.g., "strategy", "heuristic", "constraint"
    source_pattern_id: Optional[str] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Application
    usage_count: int = Field(default=0)
    success_count: int = Field(default=0)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def record_usage(self, success: bool = True) -> None:
        """Record a usage of this rule"""
        self.usage_count += 1
        if success:
            self.success_count += 1
        self.last_used = datetime.utcnow()
    
    def get_success_rate(self) -> float:
        """Calculate success rate"""
        if self.usage_count == 0:
            return 0.0
        return self.success_count / self.usage_count
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "rule_text": self.rule_text,
            "rule_type": self.rule_type,
            "source_pattern_id": self.source_pattern_id,
            "confidence": self.confidence,
            "usage_count": self.usage_count,
            "success_count": self.success_count,
            "success_rate": self.get_success_rate(),
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rule':
        """Create from dictionary"""
        return cls(**data)
