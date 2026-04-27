"""
Event Schema for the Cognitive Dashboard

Standard event types for cognitive telemetry.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
import json


class EventType(str, Enum):
    """Types of cognitive events"""
    THOUGHT_GENERATED = "thought_generated"
    THOUGHT_EVALUATED = "thought_evaluated"
    THOUGHT_ACCEPTED = "thought_accepted"
    THOUGHT_REJECTED = "thought_rejected"
    MEMORY_UPDATE = "memory_update"
    STRATEGY_CHANGE = "strategy_change"
    LAYER_EXECUTION = "layer_execution"
    AGENT_ACTION = "agent_action"
    PROMPT_EVOLUTION = "prompt_evolution"
    LEARNING_CYCLE = "learning_cycle"
    ERROR = "error"


class CognitiveEvent:
    """
    Standard event structure for cognitive telemetry.
    """
    
    def __init__(
        self,
        event_type: EventType,
        data: Dict[str, Any],
        timestamp: Optional[datetime] = None,
        metadata: Dict[str, Any] = None
    ):
        self.event_type = event_type
        self.data = data
        self.timestamp = timestamp or datetime.utcnow()
        self.metadata = metadata or {}
        self.event_id = f"{self.timestamp.isoformat()}_{event_type.value}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CognitiveEvent':
        """Create from dictionary"""
        return cls(
            event_type=EventType(data["event_type"]),
            data=data["data"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {})
        )


class EventStream:
    """
    Manages the stream of cognitive events.
    """
    
    def __init__(self, max_size: int = 1000):
        self.events: list = []
        self.max_size = max_size
        self.subscribers: list = []
    
    def emit(self, event: CognitiveEvent) -> None:
        """Emit an event to the stream"""
        self.events.append(event)
        
        # Trim to max size
        if len(self.events) > self.max_size:
            self.events = self.events[-self.max_size:]
        
        # Notify subscribers
        for subscriber in self.subscribers:
            subscriber(event)
    
    def subscribe(self, callback) -> None:
        """Subscribe to event stream"""
        self.subscribers.append(callback)
    
    def unsubscribe(self, callback) -> None:
        """Unsubscribe from event stream"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)
    
    def get_recent(self, limit: int = 100) -> list:
        """Get recent events"""
        return self.events[-limit:]
    
    def get_by_type(self, event_type: EventType, limit: int = 100) -> list:
        """Get events by type"""
        filtered = [e for e in self.events if e.event_type == event_type]
        return filtered[-limit:]
    
    def clear(self) -> None:
        """Clear all events"""
        self.events.clear()


# Global event stream
event_stream = EventStream()
