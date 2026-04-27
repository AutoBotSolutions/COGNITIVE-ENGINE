"""
Comprehensive Test Suite for Reasoning Trace System

Tests all aspects of the reasoning trace system including:
- Trace event recording
- Thought evaluation tracking
- Thought evolution tracking
- Query capabilities (top thoughts, explain rejection, compare versions)
- Reasoning chain reconstruction
- Trace export and persistence
"""

import pytest
import os
import tempfile
from datetime import datetime
from core.reasoning_trace import (
    ReasoningTrace, ReasoningTraceManager, TraceEventType,
    TraceEvent, ThoughtEvaluation, ThoughtEvolution
)


class TestTraceEvent:
    """Test TraceEvent class"""
    
    def test_event_creation(self):
        """Test creating a trace event"""
        event = TraceEvent(
            id="test_event",
            timestamp=datetime.utcnow(),
            event_type=TraceEventType.THOUGHT_GENERATED,
            layer="generator",
            data={"thought": "test"},
            thought_id="thought_1"
        )
        assert event.id == "test_event"
        assert event.event_type == TraceEventType.THOUGHT_GENERATED
        assert event.layer == "generator"
        assert event.thought_id == "thought_1"
    
    def test_event_to_dict(self):
        """Test converting event to dictionary"""
        event = TraceEvent(
            id="test_event",
            timestamp=datetime.utcnow(),
            event_type=TraceEventType.THOUGHT_GENERATED,
            layer="generator",
            data={"test": "data"}
        )
        event_dict = event.to_dict()
        assert event_dict["id"] == "test_event"
        assert event_dict["event_type"] == "thought_generated"
        assert event_dict["layer"] == "generator"


class TestThoughtEvaluation:
    """Test ThoughtEvaluation class"""
    
    def test_evaluation_creation(self):
        """Test creating a thought evaluation"""
        evaluation = ThoughtEvaluation(
            thought_id="thought_1",
            evaluator="deliberator",
            score=0.85,
            confidence=0.9,
            criteria={"coherence": 0.8, "relevance": 0.9},
            reasoning="Well-structured thought"
        )
        assert evaluation.thought_id == "thought_1"
        assert evaluation.score == 0.85
        assert evaluation.confidence == 0.9
        assert evaluation.evaluator == "deliberator"
    
    def test_evaluation_to_dict(self):
        """Test converting evaluation to dictionary"""
        evaluation = ThoughtEvaluation(
            thought_id="thought_1",
            evaluator="deliberator",
            score=0.85,
            confidence=0.9,
            criteria={"coherence": 0.8},
            reasoning="Test"
        )
        eval_dict = evaluation.to_dict()
        assert eval_dict["thought_id"] == "thought_1"
        assert eval_dict["score"] == 0.85
        assert eval_dict["evaluator"] == "deliberator"


class TestThoughtEvolution:
    """Test ThoughtEvolution class"""
    
    def test_evolution_creation(self):
        """Test creating a thought evolution"""
        evolution = ThoughtEvolution(original_thought_id="thought_1")
        assert evolution.original_thought_id == "thought_1"
        assert len(evolution.evolution_steps) == 0
    
    def test_add_evolution_step(self):
        """Test adding an evolution step"""
        evolution = ThoughtEvolution(original_thought_id="thought_1")
        evolution.add_step(
            step_type="revision",
            from_id="thought_1",
            to_id="thought_2",
            reason="Improved clarity"
        )
        assert len(evolution.evolution_steps) == 1
        assert evolution.evolution_steps[0]["step_type"] == "revision"
    
    def test_evolution_to_dict(self):
        """Test converting evolution to dictionary"""
        evolution = ThoughtEvolution(original_thought_id="thought_1")
        evolution.add_step("revision", "thought_1", "thought_2", "test")
        evolution_dict = evolution.to_dict()
        assert evolution_dict["original_thought_id"] == "thought_1"
        assert len(evolution_dict["evolution_steps"]) == 1


class TestReasoningTrace:
    """Test ReasoningTrace class"""
    
    def setup_method(self):
        """Setup fresh trace for each test"""
        self.trace = ReasoningTrace()
    
    def test_trace_creation(self):
        """Test creating a reasoning trace"""
        assert self.trace.session_id is not None
        assert self.trace.start_time is not None
        assert len(self.trace.events) == 0
    
    def test_record_event(self):
        """Test recording an event"""
        event_id = self.trace.record_event(
            event_type=TraceEventType.INPUT_RECEIVED,
            layer="engine",
            data={"input": "test"}
        )
        assert event_id is not None
        assert len(self.trace.events) == 1
        assert event_id in self.trace.event_index
    
    def test_record_evaluation(self):
        """Test recording a thought evaluation"""
        self.trace.record_evaluation(
            thought_id="thought_1",
            evaluator="deliberator",
            score=0.8,
            confidence=0.85,
            criteria={"coherence": 0.8},
            reasoning="Good thought"
        )
        assert "thought_1" in self.trace.evaluations
        assert len(self.trace.evaluations["thought_1"]) == 1
    
    def test_record_evolution(self):
        """Test recording a thought evolution"""
        self.trace.record_evolution(
            step_type="revision",
            from_id="thought_1",
            to_id="thought_2",
            reason="Improved"
        )
        assert "thought_1" in self.trace.evolutions
    
    def test_get_events_by_type(self):
        """Test filtering events by type"""
        self.trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {})
        self.trace.record_event(TraceEventType.THOUGHT_EVALUATED, "deliberator", {})
        self.trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {})
        
        generated_events = self.trace.get_events_by_type(TraceEventType.THOUGHT_GENERATED)
        assert len(generated_events) == 2
    
    def test_get_events_by_layer(self):
        """Test filtering events by layer"""
        self.trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {})
        self.trace.record_event(TraceEventType.THOUGHT_EVALUATED, "deliberator", {})
        self.trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {})
        
        generator_events = self.trace.get_events_by_layer("generator")
        assert len(generator_events) == 2
    
    def test_get_events_for_thought(self):
        """Test getting events for a specific thought"""
        event_id1 = self.trace.record_event(
            TraceEventType.THOUGHT_GENERATED,
            "generator",
            {},
            thought_id="thought_1"
        )
        event_id2 = self.trace.record_event(
            TraceEventType.THOUGHT_EVALUATED,
            "deliberator",
            {},
            thought_id="thought_1"
        )
        
        thought_events = self.trace.get_events_for_thought("thought_1")
        assert len(thought_events) == 2
    
    def test_get_top_thoughts(self):
        """Test getting top thoughts by score"""
        self.trace.record_evaluation("thought_1", "deliberator", 0.9, 0.9, {}, "Good")
        self.trace.record_evaluation("thought_2", "deliberator", 0.7, 0.8, {}, "Okay")
        self.trace.record_evaluation("thought_3", "deliberator", 0.85, 0.85, {}, "Good")
        
        top_thoughts = self.trace.get_top_thoughts(n=2)
        assert len(top_thoughts) == 2
        assert top_thoughts[0]["final_score"] == 0.9
    
    def test_explain_rejection(self):
        """Test explaining why a thought was rejected"""
        self.trace.record_event(
            TraceEventType.THOUGHT_REJECTED,
            "deliberator",
            {"reason": "low confidence"},
            thought_id="thought_1"
        )
        self.trace.record_evaluation(
            "thought_1",
            "deliberator",
            0.3,
            0.4,
            {"coherence": 0.3},
            "Not coherent enough"
        )
        
        explanation = self.trace.explain_rejection("thought_1")
        assert explanation is not None
        assert "thought_1" in explanation
        assert "rejected" in explanation.lower()
    
    def test_compare_thought_versions(self):
        """Test comparing different versions of a thought"""
        self.trace.record_evolution("revision", "thought_1", "thought_2", "Improved clarity")
        self.trace.record_evolution("revision", "thought_2", "thought_3", "Added detail")
        
        comparison = self.trace.compare_thought_versions("thought_1")
        assert comparison is not None
        assert "thought_1" in comparison
        assert "evolution" in comparison.lower()
    
    def test_get_reasoning_chain(self):
        """Test getting reasoning chain for a thought"""
        # Create a chain: event1 -> event2 -> event3
        event_id1 = self.trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {})
        event_id2 = self.trace.record_event(
            TraceEventType.THOUGHT_EVALUATED,
            "deliberator",
            {},
            parent_event_id=event_id1
        )
        event_id3 = self.trace.record_event(
            TraceEventType.THOUGHT_ACCEPTED,
            "committer",
            {},
            parent_event_id=event_id2
        )
        
        chain = self.trace.get_reasoning_chain(event_id3)
        assert len(chain) >= 1
    
    def test_set_final_decision(self):
        """Test setting final decision"""
        self.trace.set_final_decision({
            "output": "test output",
            "confidence": 0.9
        })
        
        assert self.trace.final_decision is not None
        assert self.trace.final_decision["output"] == "test output"
        assert self.trace.end_time is not None
    
    def test_get_summary(self):
        """Test getting trace summary"""
        self.trace.record_event(TraceEventType.INPUT_RECEIVED, "engine", {})
        self.trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {})
        
        summary = self.trace.get_summary()
        assert summary["session_id"] is not None
        assert summary["total_events"] == 2
        assert "event_counts" in summary
    
    def test_export_trace(self):
        """Test exporting trace to file"""
        self.trace.record_event(TraceEventType.INPUT_RECEIVED, "engine", {})
        self.trace.set_final_decision({"output": "test"})
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            self.trace.export_trace(temp_file.name)
            assert os.path.exists(temp_file.name)
        finally:
            os.unlink(temp_file.name)


class TestReasoningTraceManager:
    """Test ReasoningTraceManager class"""
    
    def setup_method(self):
        """Setup fresh manager for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = ReasoningTraceManager(storage_dir=self.temp_dir)
    
    def teardown_method(self):
        """Clean up temp directory"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_create_trace(self):
        """Test creating a new trace"""
        trace = self.manager.create_trace()
        assert trace is not None
        assert trace.session_id in self.manager.traces
    
    def test_get_trace(self):
        """Test retrieving a trace by session ID"""
        trace = self.manager.create_trace()
        session_id = trace.session_id
        
        retrieved = self.manager.get_trace(session_id)
        assert retrieved is not None
        assert retrieved.session_id == session_id
    
    def test_get_all_traces(self):
        """Test getting all traces"""
        self.manager.create_trace()
        self.manager.create_trace()
        self.manager.create_trace()
        
        all_traces = self.manager.get_all_traces()
        assert len(all_traces) == 3
    
    def test_save_trace(self):
        """Test saving a trace to disk"""
        trace = self.manager.create_trace()
        trace.record_event(TraceEventType.INPUT_RECEIVED, "engine", {})
        
        self.manager.save_trace(trace.session_id)
        
        file_path = os.path.join(self.temp_dir, f"{trace.session_id}.json")
        assert os.path.exists(file_path)
    
    def test_load_trace(self):
        """Test loading a trace from disk"""
        trace = self.manager.create_trace()
        trace.record_event(TraceEventType.INPUT_RECEIVED, "engine", {"input": "test"})
        trace.set_final_decision({"output": "result"})
        
        self.manager.save_trace(trace.session_id)
        
        # Create new manager and load
        new_manager = ReasoningTraceManager(storage_dir=self.temp_dir)
        loaded_trace = new_manager.load_trace(trace.session_id)
        
        assert loaded_trace is not None
        assert loaded_trace.session_id == trace.session_id
        assert len(loaded_trace.events) == 1


class TestReasoningTraceIntegration:
    """Integration tests for reasoning trace"""
    
    def setup_method(self):
        """Setup for integration tests"""
        self.trace = ReasoningTrace()
    
    def test_complete_cognitive_session_trace(self):
        """Test tracing a complete cognitive session"""
        # Input
        self.trace.record_event(TraceEventType.INPUT_RECEIVED, "engine", {"input": "test question"})
        
        # Interpretation
        self.trace.record_event(TraceEventType.INTERPRETATION, "interpreter", {"goals": ["answer question"]})
        
        # Generation
        thought_id1 = "thought_1"
        self.trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {}, thought_id=thought_id1)
        self.trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {}, thought_id="thought_2")
        
        # Evaluation
        self.trace.record_evaluation(thought_id1, "deliberator", 0.8, 0.85, {"coherence": 0.8}, "Good")
        self.trace.record_event(TraceEventType.THOUGHT_EVALUATED, "deliberator", {}, thought_id=thought_id1)
        
        # Acceptance
        self.trace.record_event(TraceEventType.THOUGHT_ACCEPTED, "committer", {}, thought_id=thought_id1)
        
        # Commitment
        self.trace.record_event(TraceEventType.DECISION_COMMITTED, "committer", {"output": "answer"})
        self.trace.set_final_decision({"output": "answer", "thought_id": thought_id1})
        
        # Verify
        summary = self.trace.get_summary()
        assert summary["total_events"] >= 5
        assert self.trace.final_decision is not None
    
    def test_evolution_tracking(self):
        """Test tracking thought evolution through multiple revisions"""
        # Initial thought
        thought_id1 = "thought_1"
        self.trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {}, thought_id=thought_id1)
        
        # Revision
        thought_id2 = "thought_2"
        self.trace.record_evolution("revision", thought_id1, thought_id2, "Improved clarity")
        self.trace.record_event(TraceEventType.THOUGHT_REVISED, "deliberator", {}, thought_id=thought_id2)
        
        # Another revision
        thought_id3 = "thought_3"
        self.trace.record_evolution("revision", thought_id2, thought_id3, "Added detail")
        self.trace.record_event(TraceEventType.THOUGHT_REVISED, "deliberator", {}, thought_id=thought_id3)
        
        # Verify evolution
        evolution = self.trace.get_thought_evolution(thought_id1)
        assert evolution is not None
        assert len(evolution.evolution_steps) == 2
    
    def test_query_capabilities(self):
        """Test various query capabilities"""
        # Create some thoughts with different scores
        self.trace.record_evaluation("thought_1", "deliberator", 0.9, 0.9, {}, "Excellent")
        self.trace.record_evaluation("thought_2", "deliberator", 0.7, 0.8, {}, "Good")
        self.trace.record_evaluation("thought_3", "deliberator", 0.5, 0.6, {}, "Poor")
        
        # Query top thoughts
        top_thoughts = self.trace.get_top_thoughts(n=2)
        assert len(top_thoughts) == 2
        assert top_thoughts[0]["final_score"] >= top_thoughts[1]["final_score"]
        
        # Query rejection explanation
        self.trace.record_event(TraceEventType.THOUGHT_REJECTED, "deliberator", {}, thought_id="thought_3")
        explanation = self.trace.explain_rejection("thought_3")
        assert explanation is not None


class TestReasoningTraceEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_trace(self):
        """Test operations on empty trace"""
        trace = ReasoningTrace()
        
        top_thoughts = trace.get_top_thoughts()
        assert len(top_thoughts) == 0
        
        summary = trace.get_summary()
        assert summary["total_events"] == 0
    
    def test_nonexistent_thought_queries(self):
        """Test querying for nonexistent thoughts"""
        trace = ReasoningTrace()
        
        explanation = trace.explain_rejection("nonexistent")
        assert "not evaluated" in explanation.lower() or "not" in explanation.lower()
        
        comparison = trace.compare_thought_versions("nonexistent")
        assert "no evolution" in comparison.lower()
    
    def test_invalid_parent_event(self):
        """Test recording event with invalid parent"""
        trace = ReasoningTrace()
        
        # Should handle gracefully
        event_id = trace.record_event(
            TraceEventType.THOUGHT_GENERATED,
            "generator",
            {},
            parent_event_id="nonexistent"
        )
        assert event_id is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
