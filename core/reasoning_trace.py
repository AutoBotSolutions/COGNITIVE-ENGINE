"""
Reasoning Trace System for the Cognitive Engine

This makes thought formation explicit and inspectable by:
- Tracking how thoughts were generated
- Recording evaluation and scoring processes
- Documenting thought evolution and revisions
- Providing complete reasoning traces for inspection

This enables asking "What were your top 3 thoughts?" and "Why did you reject this idea?"
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import json
import os


class TraceEventType(str, Enum):
    """Types of events that can be traced"""
    INPUT_RECEIVED = "input_received"
    INTERPRETATION = "interpretation"
    THOUGHT_GENERATED = "thought_generated"
    THOUGHT_EVALUATED = "thought_evaluated"
    THOUGHT_REVISED = "thought_revised"
    THOUGHT_MERGED = "thought_merged"
    THOUGHT_ACCEPTED = "thought_accepted"
    THOUGHT_REJECTED = "thought_rejected"
    DECISION_COMMITTED = "decision_committed"
    MEMORY_UPDATED = "memory_updated"
    STRATEGY_ADJUSTED = "strategy_adjusted"


@dataclass
class TraceEvent:
    """A single event in the reasoning trace"""
    id: str
    timestamp: datetime
    event_type: TraceEventType
    layer: str  # Which cognitive layer generated this event
    data: Dict[str, Any]
    thought_id: Optional[str] = None  # Associated thought if applicable
    parent_event_id: Optional[str] = None  # Parent event for causality
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type.value,
            "layer": self.layer,
            "data": self.data,
            "thought_id": self.thought_id,
            "parent_event_id": self.parent_event_id
        }


@dataclass
class ThoughtEvaluation:
    """Record of how a thought was evaluated"""
    thought_id: str
    evaluator: str  # What evaluated this thought (e.g., "deliberator", "ethical_alignment")
    score: float
    confidence: float
    criteria: Dict[str, float]  # Individual criteria scores
    reasoning: str  # Explanation of the evaluation
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> dict:
        return {
            "thought_id": self.thought_id,
            "evaluator": self.evaluator,
            "score": self.score,
            "confidence": self.confidence,
            "criteria": self.criteria,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class ThoughtEvolution:
    """Record of how a thought evolved over time"""
    original_thought_id: str
    evolution_steps: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_step(self, step_type: str, from_id: str, to_id: str, reason: str, data: Dict[str, Any] = None):
        """Add an evolution step"""
        step = {
            "step_type": step_type,  # "revision", "merge", "mutation"
            "from_id": from_id,
            "to_id": to_id,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data or {}
        }
        self.evolution_steps.append(step)
    
    def to_dict(self) -> dict:
        return {
            "original_thought_id": self.original_thought_id,
            "evolution_steps": self.evolution_steps
        }


class ReasoningTrace:
    """
    Complete reasoning trace for a single cognitive session.
    
    This provides explicit, inspectable evidence of the thinking process,
    enabling queries like:
    - "What were your top 3 thoughts?"
    - "Why did you reject this idea?"
    - "What changed between version 1 and 3?"
    """
    
    def __init__(self, session_id: str = None):
        self.session_id = session_id or self._generate_session_id()
        self.start_time = datetime.utcnow()
        self.end_time: Optional[datetime] = None
        
        # Trace events
        self.events: List[TraceEvent] = []
        self.event_index: Dict[str, int] = {}  # event_id -> index
        
        # Thought evaluations
        self.evaluations: Dict[str, List[ThoughtEvaluation]] = {}  # thought_id -> evaluations
        
        # Thought evolutions
        self.evolutions: Dict[str, ThoughtEvolution] = {}  # thought_id -> evolution
        
        # Final decision
        self.final_decision: Optional[Dict[str, Any]] = None
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID"""
        import uuid
        return f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
    
    def record_event(self, event_type: TraceEventType, layer: str, data: Dict[str, Any], 
                     thought_id: str = None, parent_event_id: str = None) -> str:
        """
        Record an event in the reasoning trace.
        
        Args:
            event_type: Type of event
            layer: Cognitive layer that generated the event
            data: Event data
            thought_id: Associated thought if applicable
            parent_event_id: Parent event for causality
        
        Returns:
            Event ID
        """
        import uuid
        event_id = str(uuid.uuid4())
        
        event = TraceEvent(
            id=event_id,
            timestamp=datetime.utcnow(),
            event_type=event_type,
            layer=layer,
            data=data,
            thought_id=thought_id,
            parent_event_id=parent_event_id
        )
        
        self.events.append(event)
        self.event_index[event_id] = len(self.events) - 1
        return event_id
    
    def record_evaluation(self, thought_id: str, evaluator: str, score: float, 
                        confidence: float, criteria: Dict[str, float], reasoning: str):
        """Record an evaluation of a thought"""
        evaluation = ThoughtEvaluation(
            thought_id=thought_id,
            evaluator=evaluator,
            score=score,
            confidence=confidence,
            criteria=criteria,
            reasoning=reasoning
        )
        
        if thought_id not in self.evaluations:
            self.evaluations[thought_id] = []
        self.evaluations[thought_id].append(evaluation)
    
    def record_evolution(self, step_type: str, from_id: str, to_id: str, reason: str, data: Dict[str, Any] = None):
        """Record a thought evolution step"""
        # Find or create evolution record
        if from_id not in self.evolutions:
            self.evolutions[from_id] = ThoughtEvolution(original_thought_id=from_id)
        
        self.evolutions[from_id].add_step(step_type, from_id, to_id, reason, data)
    
    def get_events_by_type(self, event_type: TraceEventType) -> List[TraceEvent]:
        """Get all events of a specific type"""
        return [e for e in self.events if e.event_type == event_type]
    
    def get_events_by_layer(self, layer: str) -> List[TraceEvent]:
        """Get all events from a specific layer"""
        return [e for e in self.events if e.layer == layer]
    
    def get_events_for_thought(self, thought_id: str) -> List[TraceEvent]:
        """Get all events related to a specific thought"""
        return [e for e in self.events if e.thought_id == thought_id]
    
    def get_thought_evaluations(self, thought_id: str) -> List[ThoughtEvaluation]:
        """Get all evaluations for a specific thought"""
        return self.evaluations.get(thought_id, [])
    
    def get_thought_evolution(self, thought_id: str) -> Optional[ThoughtEvolution]:
        """Get the evolution history of a thought"""
        return self.evolutions.get(thought_id)
    
    def get_top_thoughts(self, n: int = 3) -> List[Dict[str, Any]]:
        """
        Get the top N thoughts by final score.
        
        This enables the query: "What were your top 3 thoughts?"
        """
        # Get all evaluated thoughts
        thought_scores = {}
        for thought_id, evaluations in self.evaluations.items():
            if evaluations:
                latest_eval = evaluations[-1]
                thought_scores[thought_id] = latest_eval.score
        
        # Sort by score and get top N
        sorted_thoughts = sorted(thought_scores.items(), key=lambda x: x[1], reverse=True)
        top_n = sorted_thoughts[:n]
        
        result = []
        for thought_id, score in top_n:
            evaluations = self.evaluations.get(thought_id, [])
            events = self.get_events_for_thought(thought_id)
            result.append({
                "thought_id": thought_id,
                "final_score": score,
                "evaluations": [e.to_dict() for e in evaluations],
                "events": [e.to_dict() for e in events]
            })
        
        return result
    
    def explain_rejection(self, thought_id: str) -> str:
        """
        Explain why a specific thought was rejected.
        
        This enables the query: "Why did you reject this idea?"
        """
        evaluations = self.get_thought_evaluations(thought_id)
        events = self.get_events_for_thought(thought_id)
        
        if not evaluations:
            return f"Thought {thought_id} was not evaluated."
        
        # Find rejection event
        rejection_events = [e for e in events if e.event_type == TraceEventType.THOUGHT_REJECTED]
        
        if not rejection_events:
            return f"Thought {thought_id} was not explicitly rejected."
        
        rejection_event = rejection_events[0]
        latest_eval = evaluations[-1]
        
        explanation = f"Thought {thought_id} was rejected because:\n"
        explanation += f"- Final score: {latest_eval.score:.3f} (below threshold)\n"
        explanation += f"- Confidence: {latest_eval.confidence:.3f}\n"
        explanation += f"- Reasoning: {latest_eval.reasoning}\n"
        
        if latest_eval.criteria:
            explanation += "- Criteria scores:\n"
            for criterion, score in latest_eval.criteria.items():
                explanation += f"  {criterion}: {score:.3f}\n"
        
        return explanation
    
    def compare_thought_versions(self, thought_id: str) -> str:
        """
        Compare different versions of a thought.
        
        This enables the query: "What changed between version 1 and 3?"
        """
        evolution = self.get_thought_evolution(thought_id)
        
        if not evolution:
            return f"Thought {thought_id} has no evolution history."
        
        explanation = f"Evolution history for thought {thought_id}:\n"
        for i, step in enumerate(evolution.evolution_steps, 1):
            explanation += f"\nStep {i}: {step['step_type']}\n"
            explanation += f"  From: {step['from_id']}\n"
            explanation += f"  To: {step['to_id']}\n"
            explanation += f"  Reason: {step['reason']}\n"
            explanation += f"  Time: {step['timestamp']}\n"
        
        return explanation
    
    def get_reasoning_chain(self, thought_id: str) -> List[TraceEvent]:
        """
        Get the complete reasoning chain for a thought.
        
        This traces back from the final thought through all causal events.
        """
        chain = []
        current_event_id = None
        
        # Find the most recent event for this thought
        thought_events = self.get_events_for_thought(thought_id)
        if thought_events:
            current_event_id = thought_events[-1].id
        
        # Trace back through parent events
        visited = set()
        while current_event_id and current_event_id not in visited:
            if current_event_id in self.event_index:
                idx = self.event_index[current_event_id]
                event = self.events[idx]
                chain.append(event)
                current_event_id = event.parent_event_id
                visited.add(current_event_id)
            else:
                break
        
        return chain
    
    def set_final_decision(self, decision: Dict[str, Any]):
        """Record the final decision of this reasoning session"""
        self.final_decision = decision
        self.end_time = datetime.utcnow()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the entire reasoning trace"""
        duration = 0.0
        if self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
        elif self.start_time:
            duration = (datetime.utcnow() - self.start_time).total_seconds()
        
        event_counts = {}
        for event_type in TraceEventType:
            event_counts[event_type.value] = len(self.get_events_by_type(event_type))
        
        layer_counts = {}
        for event in self.events:
            layer_counts[event.layer] = layer_counts.get(event.layer, 0) + 1
        
        return {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": duration,
            "total_events": len(self.events),
            "event_counts": event_counts,
            "layer_counts": layer_counts,
            "total_thoughts_evaluated": len(self.evaluations),
            "total_evolutions": len(self.evolutions),
            "final_decision": self.final_decision
        }
    
    def export_trace(self, filepath: str):
        """Export the reasoning trace to a file"""
        data = {
            "session_id": self.session_id,
            "summary": self.get_summary(),
            "events": [e.to_dict() for e in self.events],
            "evaluations": {
                tid: [e.to_dict() for e in evals]
                for tid, evals in self.evaluations.items()
            },
            "evolutions": {
                tid: e.to_dict() for tid, e in self.evolutions.items()
            },
            "final_decision": self.final_decision
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


class ReasoningTraceManager:
    """
    Manages multiple reasoning traces and provides query capabilities.
    """
    
    def __init__(self, storage_dir: str = "reasoning_traces"):
        self.storage_dir = storage_dir
        self.traces: Dict[str, ReasoningTrace] = {}  # session_id -> trace
        os.makedirs(storage_dir, exist_ok=True)
    
    def create_trace(self, session_id: str = None) -> ReasoningTrace:
        """Create a new reasoning trace"""
        trace = ReasoningTrace(session_id)
        self.traces[trace.session_id] = trace
        return trace
    
    def get_trace(self, session_id: str) -> Optional[ReasoningTrace]:
        """Get a trace by session ID"""
        return self.traces.get(session_id)
    
    def get_all_traces(self) -> List[ReasoningTrace]:
        """Get all traces"""
        return list(self.traces.values())
    
    def search_traces(self, query: str) -> List[ReasoningTrace]:
        """Search traces by content"""
        query_lower = query.lower()
        results = []
        
        for trace in self.traces.values():
            # Search in events
            for event in trace.events:
                event_str = str(event.data).lower() + str(event.reasoning if hasattr(event, 'reasoning') else '').lower()
                if query_lower in event_str:
                    results.append(trace)
                    break
        
        return results
    
    def save_trace(self, session_id: str):
        """Save a trace to disk"""
        trace = self.traces.get(session_id)
        if trace:
            filepath = os.path.join(self.storage_dir, f"{session_id}.json")
            trace.export_trace(filepath)
    
    def load_trace(self, session_id: str) -> Optional[ReasoningTrace]:
        """Load a trace from disk"""
        filepath = os.path.join(self.storage_dir, f"{session_id}.json")
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        trace = ReasoningTrace(data["session_id"])
        trace.start_time = datetime.fromisoformat(data["summary"]["start_time"])
        trace.end_time = datetime.fromisoformat(data["summary"]["end_time"]) if data["summary"]["end_time"] else None
        trace.final_decision = data["final_decision"]
        
        # Reconstruct events
        for e_data in data["events"]:
            event = TraceEvent(
                id=e_data["id"],
                timestamp=datetime.fromisoformat(e_data["timestamp"]),
                event_type=TraceEventType(e_data["event_type"]),
                layer=e_data["layer"],
                data=e_data["data"],
                thought_id=e_data.get("thought_id"),
                parent_event_id=e_data.get("parent_event_id")
            )
            trace.events.append(event)
            trace.event_index[event.id] = len(trace.events) - 1
        
        # Reconstruct evaluations
        for tid, evals_data in data["evaluations"].items():
            for e_data in evals_data:
                evaluation = ThoughtEvaluation(
                    thought_id=e_data["thought_id"],
                    evaluator=e_data["evaluator"],
                    score=e_data["score"],
                    confidence=e_data["confidence"],
                    criteria=e_data["criteria"],
                    reasoning=e_data["reasoning"],
                    timestamp=datetime.fromisoformat(e_data["timestamp"])
                )
                if tid not in trace.evaluations:
                    trace.evaluations[tid] = []
                trace.evaluations[tid].append(evaluation)
        
        # Reconstruct evolutions
        for tid, evol_data in data["evolutions"].items():
            evolution = ThoughtEvolution(original_thought_id=evol_data["original_thought_id"])
            evolution.evolution_steps = evol_data["evolution_steps"]
            trace.evolutions[tid] = evolution
        
        self.traces[trace.session_id] = trace
        return trace
