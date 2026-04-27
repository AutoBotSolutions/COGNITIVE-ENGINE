"""
Three-Layer Memory Architecture for the Cognitive Engine

This implements the memory system that transforms intelligence from reactive to cumulative:

1. Episodic Memory (Raw Events) - Logs of everything that happens
2. Pattern Memory (Structure Extraction) - Recurring behaviors and structures
3. Rule Memory (Learned Strategies) - Compressed knowledge used to guide future reasoning

Memory becomes an active participant that influences what happens next, not just a record.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
from collections import defaultdict
import json
import os


@dataclass
class EpisodicEvent:
    """A single event in episodic memory"""
    id: str
    timestamp: datetime
    event_type: str
    data: Dict[str, Any]
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "data": self.data,
            "context": self.context
        }


@dataclass
class Pattern:
    """A recurring pattern extracted from episodic memory"""
    id: str
    pattern_type: str
    description: str
    frequency: int = 0
    confidence: float = 0.0
    examples: List[str] = field(default_factory=list)
    last_seen: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pattern_type": self.pattern_type,
            "description": self.description,
            "frequency": self.frequency,
            "confidence": self.confidence,
            "examples": self.examples,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None
        }


@dataclass
class Rule:
    """A learned rule derived from patterns"""
    id: str
    name: str
    condition: str
    action: str
    confidence: float = 0.0
    success_rate: float = 0.0
    usage_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "condition": self.condition,
            "action": self.action,
            "confidence": self.confidence,
            "success_rate": self.success_rate,
            "usage_count": self.usage_count,
            "created_at": self.created_at.isoformat()
        }


class ThreeLayerMemory:
    """
    Three-Layer Memory Architecture
    
    Layer 1: Episodic Memory - Raw events and interactions
    Layer 2: Pattern Memory - Recurring structures and behaviors
    Layer 3: Rule Memory - Learned strategies that guide future reasoning
    
    This transforms intelligence from reactive (responding to input) to cumulative 
    (building on past experience).
    """
    
    def __init__(self, storage_path: str = "cognitive_memory.json"):
        self.storage_path = storage_path
        
        # Layer 1: Episodic Memory
        self.episodic_events: List[EpisodicEvent] = []
        self.episodic_index: Dict[str, int] = {}  # event_id -> index
        
        # Layer 2: Pattern Memory
        self.patterns: Dict[str, Pattern] = {}
        
        # Layer 3: Rule Memory
        self.rules: Dict[str, Rule] = {}
        
        # Statistics
        self.total_events = 0
        self.pattern_extraction_interval = 100  # Extract patterns every N events
        
        self._load_from_disk()
    
    # ============ LAYER 1: EPISODIC MEMORY ============
    
    def record_event(self, event_type: str, data: Dict[str, Any], context: Dict[str, Any] = None) -> str:
        """
        Record an event in episodic memory.
        
        Args:
            event_type: Type of event (e.g., "thought_generated", "user_input", "reasoning_step")
            data: Event data
            context: Additional context (e.g., current state, goals)
        
        Returns:
            Event ID
        """
        import uuid
        event_id = str(uuid.uuid4())
        
        event = EpisodicEvent(
            id=event_id,
            timestamp=datetime.utcnow(),
            event_type=event_type,
            data=data,
            context=context or {}
        )
        
        self.episodic_events.append(event)
        self.episodic_index[event_id] = len(self.episodic_events) - 1
        self.total_events += 1
        
        # Trigger pattern extraction if interval reached
        if self.total_events % self.pattern_extraction_interval == 0:
            self._extract_patterns()
        
        self._save_to_disk()
        return event_id
    
    def get_recent_events(self, n: int = 10, event_type: str = None) -> List[EpisodicEvent]:
        """Get the most recent events, optionally filtered by type"""
        events = self.episodic_events
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return events[-n:]
    
    def get_events_by_type(self, event_type: str) -> List[EpisodicEvent]:
        """Get all events of a specific type"""
        return [e for e in self.episodic_events if e.event_type == event_type]
    
    def search_events(self, query: str) -> List[EpisodicEvent]:
        """Search events by content"""
        query_lower = query.lower()
        results = []
        for event in self.episodic_events:
            # Search in data and context
            event_str = str(event.data).lower() + str(event.context).lower()
            if query_lower in event_str:
                results.append(event)
        return results
    
    # ============ LAYER 2: PATTERN MEMORY ============
    
    def _extract_patterns(self):
        """
        Extract recurring patterns from episodic memory.
        
        This identifies:
        - Repeated reasoning failures
        - Common thought structures
        - Recurring interaction patterns
        """
        print(f"Extracting patterns from {len(self.episodic_events)} events...")
        
        # Pattern: Repeated event sequences
        self._extract_sequence_patterns()
        
        # Pattern: Common properties in similar events
        self._extract_property_patterns()
        
        # Pattern: Temporal patterns
        self._extract_temporal_patterns()
        
        self._save_to_disk()
    
    def _extract_sequence_patterns(self):
        """Extract patterns in event sequences"""
        # Look for repeated sequences of event types
        sequence_length = 3
        if len(self.episodic_events) < sequence_length:
            return
        
        sequence_counts = defaultdict(int)
        sequence_examples = defaultdict(list)
        
        for i in range(len(self.episodic_events) - sequence_length + 1):
            sequence = tuple(e.event_type for e in self.episodic_events[i:i+sequence_length])
            sequence_counts[sequence] += 1
            if len(sequence_examples[sequence]) < 3:
                sequence_examples[sequence].append(i)
        
        # Create pattern objects for frequent sequences
        for sequence, count in sequence_counts.items():
            if count >= 3:  # Minimum frequency threshold
                import uuid
                pattern_id = f"seq_{str(uuid.uuid4())[:8]}"
                
                pattern = Pattern(
                    id=pattern_id,
                    pattern_type="sequence",
                    description=f"Sequence: {' → '.join(sequence)}",
                    frequency=count,
                    confidence=min(1.0, count / 10.0),
                    examples=[str(idx) for idx in sequence_examples[sequence]],
                    last_seen=datetime.utcnow()
                )
                self.patterns[pattern_id] = pattern
    
    def _extract_property_patterns(self):
        """Extract patterns in event properties"""
        # Group events by type and find common properties
        type_to_events = defaultdict(list)
        for event in self.episodic_events:
            type_to_events[event.event_type].append(event)
        
        for event_type, events in type_to_events.items():
            if len(events) < 3:
                continue
            
            # Find common keys in data
            common_keys = None
            for event in events:
                keys = set(event.data.keys())
                if common_keys is None:
                    common_keys = keys
                else:
                    common_keys = common_keys.intersection(keys)
            
            if common_keys and len(common_keys) > 1:
                import uuid
                pattern_id = f"prop_{str(uuid.uuid4())[:8]}"
                
                pattern = Pattern(
                    id=pattern_id,
                    pattern_type="property",
                    description=f"Common properties in {event_type}: {', '.join(common_keys)}",
                    frequency=len(events),
                    confidence=0.7,
                    examples=[e.id for e in events[:3]],
                    last_seen=datetime.utcnow()
                )
                self.patterns[pattern_id] = pattern
    
    def _extract_temporal_patterns(self):
        """Extract temporal patterns in events"""
        # Look for events that occur at regular intervals
        if len(self.episodic_events) < 5:
            return
        
        # Group by event type and check timing
        type_to_timestamps = defaultdict(list)
        for event in self.episodic_events:
            type_to_timestamps[event.event_type].append(event.timestamp)
        
        for event_type, timestamps in type_to_timestamps.items():
            if len(timestamps) < 3:
                continue
            
            # Check for regular intervals
            intervals = []
            for i in range(1, len(timestamps)):
                interval = (timestamps[i] - timestamps[i-1]).total_seconds()
                intervals.append(interval)
            
            if intervals:
                avg_interval = sum(intervals) / len(intervals)
                variance = sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)
                
                # If variance is low, it's a regular pattern
                if variance < (avg_interval ** 2) * 0.5:  # Coefficient of variation < 0.7
                    import uuid
                    pattern_id = f"temp_{str(uuid.uuid4())[:8]}"
                    
                    pattern = Pattern(
                        id=pattern_id,
                        pattern_type="temporal",
                        description=f"{event_type} occurs approximately every {avg_interval:.1f} seconds",
                        frequency=len(timestamps),
                        confidence=0.8,
                        examples=[str(ts) for ts in timestamps[:3]],
                        last_seen=datetime.utcnow()
                    )
                    self.patterns[pattern_id] = pattern
    
    def get_patterns_by_type(self, pattern_type: str) -> List[Pattern]:
        """Get all patterns of a specific type"""
        return [p for p in self.patterns.values() if p.pattern_type == pattern_type]
    
    def get_high_confidence_patterns(self, threshold: float = 0.7) -> List[Pattern]:
        """Get patterns with confidence above threshold"""
        return [p for p in self.patterns.values() if p.confidence >= threshold]
    
    # ============ LAYER 3: RULE MEMORY ============
    
    def derive_rule_from_pattern(self, pattern: Pattern) -> Optional[Rule]:
        """
        Derive a rule from a pattern.
        
        This transforms patterns into actionable rules that guide future reasoning.
        """
        import uuid
        
        if pattern.pattern_type == "sequence":
            # Rule: If we see this sequence, expect the next event
            rule = Rule(
                id=f"rule_{str(uuid.uuid4())[:8]}",
                name=f"Sequence Rule: {pattern.description}",
                condition=f"Events match sequence: {pattern.description}",
                action="Anticipate continuation of sequence",
                confidence=pattern.confidence * 0.9,
                success_rate=0.0,
                usage_count=0
            )
            self.rules[rule.id] = rule
            return rule
        
        elif pattern.pattern_type == "property":
            # Rule: When this event type occurs, expect these properties
            rule = Rule(
                id=f"rule_{str(uuid.uuid4())[:8]}",
                name=f"Property Rule: {pattern.description}",
                condition=f"Event type matches pattern: {pattern.description}",
                action="Check for expected properties",
                confidence=pattern.confidence * 0.8,
                success_rate=0.0,
                usage_count=0
            )
            self.rules[rule.id] = rule
            return rule
        
        return None
    
    def apply_rule(self, rule_id: str, context: Dict[str, Any]) -> Optional[str]:
        """
        Apply a rule to the current context.
        
        Returns:
            Action to take if rule applies, None otherwise
        """
        rule = self.rules.get(rule_id)
        if not rule:
            return None
        
        # Simple rule matching - check if condition matches context
        # This is a basic implementation; could be more sophisticated
        context_str = str(context).lower()
        condition_str = rule.condition.lower()
        
        if condition_str in context_str:
            rule.usage_count += 1
            return rule.action
        
        return None
    
    def update_rule_success(self, rule_id: str, success: bool):
        """Update the success rate of a rule"""
        rule = self.rules.get(rule_id)
        if not rule:
            return
        
        # Update success rate using moving average
        rule.usage_count += 1
        if success:
            rule.success_rate = (rule.success_rate * (rule.usage_count - 1) + 1.0) / rule.usage_count
        else:
            rule.success_rate = (rule.success_rate * (rule.usage_count - 1) + 0.0) / rule.usage_count
        
        self._save_to_disk()
    
    def get_applicable_rules(self, context: Dict[str, Any]) -> List[Rule]:
        """Get all rules that apply to the current context"""
        applicable = []
        for rule in self.rules.values():
            context_str = str(context).lower()
            condition_str = rule.condition.lower()
            if condition_str in context_str:
                applicable.append(rule)
        return sorted(applicable, key=lambda r: r.confidence, reverse=True)
    
    # ============ MEMORY INTEGRATION ============
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of all three memory layers"""
        return {
            "episodic": {
                "total_events": len(self.episodic_events),
                "event_types": list(set(e.event_type for e in self.episodic_events))
            },
            "pattern": {
                "total_patterns": len(self.patterns),
                "pattern_types": list(set(p.pattern_type for p in self.patterns.values())),
                "high_confidence": len(self.get_high_confidence_patterns(0.7))
            },
            "rule": {
                "total_rules": len(self.rules),
                "avg_confidence": sum(r.confidence for r in self.rules.values()) / len(self.rules) if self.rules else 0,
                "avg_success_rate": sum(r.success_rate for r in self.rules.values()) / len(self.rules) if self.rules else 0
            }
        }
    
    def _save_to_disk(self):
        """Save memory to disk"""
        try:
            data = {
                "episodic_events": [e.to_dict() for e in self.episodic_events[-1000:]],  # Keep last 1000
                "patterns": {pid: p.to_dict() for pid, p in self.patterns.items()},
                "rules": {rid: r.to_dict() for rid, r in self.rules.items()},
                "total_events": self.total_events
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def _load_from_disk(self):
        """Load memory from disk"""
        if not os.path.exists(self.storage_path):
            return
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            
            # Load episodic events
            for e_data in data.get("episodic_events", []):
                event = EpisodicEvent(
                    id=e_data["id"],
                    timestamp=datetime.fromisoformat(e_data["timestamp"]),
                    event_type=e_data["event_type"],
                    data=e_data["data"],
                    context=e_data.get("context", {})
                )
                self.episodic_events.append(event)
                self.episodic_index[event.id] = len(self.episodic_events) - 1
            
            # Load patterns
            for pid, p_data in data.get("patterns", {}).items():
                pattern = Pattern(
                    id=p_data["id"],
                    pattern_type=p_data["pattern_type"],
                    description=p_data["description"],
                    frequency=p_data.get("frequency", 0),
                    confidence=p_data.get("confidence", 0.0),
                    examples=p_data.get("examples", []),
                    last_seen=datetime.fromisoformat(p_data["last_seen"]) if p_data.get("last_seen") else None
                )
                self.patterns[pid] = pattern
            
            # Load rules
            for rid, r_data in data.get("rules", {}).items():
                rule = Rule(
                    id=r_data["id"],
                    name=r_data["name"],
                    condition=r_data["condition"],
                    action=r_data["action"],
                    confidence=r_data.get("confidence", 0.0),
                    success_rate=r_data.get("success_rate", 0.0),
                    usage_count=r_data.get("usage_count", 0),
                    created_at=datetime.fromisoformat(r_data["created_at"]) if r_data.get("created_at") else datetime.utcnow()
                )
                self.rules[rid] = rule
            
            self.total_events = data.get("total_events", 0)
            print(f"Loaded memory: {len(self.episodic_events)} events, {len(self.patterns)} patterns, {len(self.rules)} rules")
        except Exception as e:
            print(f"Error loading memory: {e}")
