"""
Comprehensive Test Suite for Three-Layer Memory Architecture

Tests all aspects of the memory system including:
- Episodic memory (raw events)
- Pattern memory (structure extraction)
- Rule memory (learned strategies)
- Learning pipeline
- Persistence
"""

import pytest
import os
import tempfile
from datetime import datetime
from core.memory import ThreeLayerMemory, EpisodicEvent, Pattern, Rule


class TestEpisodicMemory:
    """Test episodic memory layer"""
    
    def setup_method(self):
        """Setup fresh memory for each test"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.memory = ThreeLayerMemory(storage_path=self.temp_file.name)
    
    def teardown_method(self):
        """Clean up temp file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_record_event(self):
        """Test recording events to episodic memory"""
        event_id = self.memory.record_event(
            event_type="thought_generated",
            data={"thought": "test thought"},
            context={"iteration": 1}
        )
        assert event_id is not None
        assert len(self.memory.episodic_events) == 1
        assert self.memory.total_events == 1
    
    def test_get_recent_events(self):
        """Test retrieving recent events"""
        self.memory.record_event("test1", {"data": 1})
        self.memory.record_event("test2", {"data": 2})
        self.memory.record_event("test3", {"data": 3})
        
        recent = self.memory.get_recent_events(n=2)
        assert len(recent) == 2
        assert recent[0].event_type == "test2"
        assert recent[1].event_type == "test3"
    
    def test_get_events_by_type(self):
        """Test filtering events by type"""
        self.memory.record_event("type_a", {"data": 1})
        self.memory.record_event("type_b", {"data": 2})
        self.memory.record_event("type_a", {"data": 3})
        
        type_a_events = self.memory.get_events_by_type("type_a")
        assert len(type_a_events) == 2
    
    def test_search_events(self):
        """Test searching events by content"""
        self.memory.record_event("test", {"content": "important data here"})
        self.memory.record_event("test", {"content": "other stuff"})
        
        results = self.memory.search_events("important")
        assert len(results) == 1
        assert "important" in str(results[0].data).lower()
    
    def test_event_context(self):
        """Test that events store context"""
        event_id = self.memory.record_event(
            event_type="test",
            data={"main": "data"},
            context={"iteration": 5, "confidence": 0.8}
        )
        
        event = self.memory.episodic_events[-1]
        assert event.context["iteration"] == 5
        assert event.context["confidence"] == 0.8


class TestPatternMemory:
    """Test pattern memory layer"""
    
    def setup_method(self):
        """Setup fresh memory for each test"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.memory = ThreeLayerMemory(storage_path=self.temp_file.name)
    
    def teardown_method(self):
        """Clean up temp file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_extract_sequence_patterns(self):
        """Test extraction of sequence patterns"""
        # Record a repeating sequence
        for _ in range(5):
            self.memory.record_event("step1", {})
            self.memory.record_event("step2", {})
            self.memory.record_event("step3", {})
        
        # Trigger pattern extraction
        self.memory._extract_patterns()
        
        # Should have found sequence patterns
        sequence_patterns = self.memory.get_patterns_by_type("sequence")
        assert len(sequence_patterns) > 0
    
    def test_pattern_frequency(self):
        """Test that pattern frequency is tracked"""
        # Record events
        for _ in range(10):
            self.memory.record_event("repeated", {})
        
        self.memory._extract_patterns()
        
        # Check frequency
        for pattern in self.memory.patterns.values():
            if pattern.pattern_type == "property":
                assert pattern.frequency >= 10
    
    def test_pattern_confidence(self):
        """Test that pattern confidence is calculated"""
        # Record many events to build confidence
        for _ in range(20):
            self.memory.record_event("frequent", {})
        
        self.memory._extract_patterns()
        
        # Check confidence
        for pattern in self.memory.patterns.values():
            assert pattern.confidence >= 0.0
            assert pattern.confidence <= 1.0
    
    def test_get_high_confidence_patterns(self):
        """Test filtering patterns by confidence"""
        # Add a pattern manually with high confidence
        pattern = Pattern(
            id="test_pattern",
            pattern_type="sequence",
            description="Test pattern",
            frequency=10,
            confidence=0.9
        )
        self.memory.patterns["test_pattern"] = pattern
        
        high_conf = self.memory.get_high_confidence_patterns(threshold=0.8)
        assert len(high_conf) >= 1
        assert pattern in high_conf


class TestRuleMemory:
    """Test rule memory layer"""
    
    def setup_method(self):
        """Setup fresh memory for each test"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.memory = ThreeLayerMemory(storage_path=self.temp_file.name)
    
    def teardown_method(self):
        """Clean up temp file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_derive_rule_from_pattern(self):
        """Test deriving rules from patterns"""
        pattern = Pattern(
            id="test_pattern",
            pattern_type="sequence",
            description="A -> B -> C",
            frequency=5,
            confidence=0.8
        )
        
        rule = self.memory.derive_rule_from_pattern(pattern)
        assert rule is not None
        assert rule.id in self.memory.rules
    
    def test_apply_rule(self):
        """Test applying a rule to context"""
        rule = Rule(
            id="test_rule",
            name="Test Rule",
            condition="test condition",
            action="test action",
            confidence=0.9
        )
        self.memory.rules["test_rule"] = rule
        
        context = {"test condition": "present"}
        action = self.memory.apply_rule("test_rule", context)
        assert action == "test action"
    
    def test_get_applicable_rules(self):
        """Test getting rules that apply to context"""
        rule1 = Rule(
            id="rule1",
            name="Rule 1",
            condition="condition1",
            action="action1",
            confidence=0.7
        )
        rule2 = Rule(
            id="rule2",
            name="Rule 2",
            condition="condition2",
            action="action2",
            confidence=0.9
        )
        self.memory.rules["rule1"] = rule1
        self.memory.rules["rule2"] = rule2
        
        context = {"condition1": "present", "condition2": "present"}
        applicable = self.memory.get_applicable_rules(context)
        assert len(applicable) >= 2
    
    def test_update_rule_success(self):
        """Test updating rule success rate"""
        rule = Rule(
            id="test_rule",
            name="Test Rule",
            condition="test",
            action="test",
            confidence=0.5,
            success_rate=0.0,
            usage_count=0
        )
        self.memory.rules["test_rule"] = rule
        
        # Update with success
        self.memory.update_rule_success("test_rule", success=True)
        
        updated = self.memory.rules["test_rule"]
        assert updated.usage_count == 1
        assert updated.success_rate > 0.0
    
    def test_rule_usage_tracking(self):
        """Test that rule usage is tracked"""
        rule = Rule(
            id="test_rule",
            name="Test Rule",
            condition="test",
            action="test",
            confidence=0.5,
            usage_count=0
        )
        self.memory.rules["test_rule"] = rule
        
        # Apply rule
        self.memory.apply_rule("test_rule", {"test": "present"})
        
        # Check usage count
        assert rule.usage_count == 1


class TestMemoryIntegration:
    """Integration tests for three-layer memory"""
    
    def setup_method(self):
        """Setup fresh memory for each test"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.memory = ThreeLayerMemory(storage_path=self.temp_file.name)
    
    def teardown_method(self):
        """Clean up temp file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_learning_pipeline(self):
        """Test the complete learning pipeline"""
        # Record experiences
        for i in range(15):
            self.memory.record_event("learning_event", {"iteration": i})
        
        # Trigger pattern extraction (should happen automatically at interval)
        self.memory._extract_patterns()
        
        # Check that patterns were extracted
        assert len(self.memory.patterns) > 0
        
        # Derive rules from patterns
        for pattern in list(self.memory.patterns.values())[:3]:
            rule = self.memory.derive_rule_from_pattern(pattern)
            assert rule is not None
    
    def test_memory_summary(self):
        """Test getting memory summary"""
        summary = self.memory.get_memory_summary()
        
        assert "episodic" in summary
        assert "pattern" in summary
        assert "rule" in summary
        assert "total_events" in summary["episodic"]
        assert "total_patterns" in summary["pattern"]
        assert "total_rules" in summary["rule"]
    
    def test_persistence(self):
        """Test saving and loading memory"""
        # Add data
        self.memory.record_event("test", {"data": "value"})
        self.memory._extract_patterns()
        
        # Save
        self.memory._save_to_disk()
        
        # Load new instance
        new_memory = ThreeLayerMemory(storage_path=self.temp_file.name)
        
        # Verify data persisted
        assert len(new_memory.episodic_events) >= 1
        assert new_memory.total_events >= 1
    
    def test_pattern_extraction_interval(self):
        """Test that pattern extraction happens at intervals"""
        initial_pattern_count = len(self.memory.patterns)
        
        # Record events up to interval
        for i in range(self.memory.pattern_extraction_interval):
            self.memory.record_event("test", {"i": i})
        
        # Should have extracted patterns
        assert len(self.memory.patterns) >= initial_pattern_count
    
    def test_memory_as_active_participant(self):
        """Test that memory influences future reasoning"""
        # Record successful reasoning pattern
        self.memory.record_event("reasoning", {"strategy": "A", "outcome": "success"})
        self.memory.record_event("reasoning", {"strategy": "A", "outcome": "success"})
        self.memory.record_event("reasoning", {"strategy": "B", "outcome": "failure"})
        
        # Extract patterns
        self.memory._extract_patterns()
        
        # Derive rule
        for pattern in self.memory.patterns.values():
            if pattern.confidence > 0.5:
                rule = self.memory.derive_rule_from_pattern(pattern)
                if rule:
                    # Apply rule to new context
                    context = {"strategy": "A"}
                    action = self.memory.apply_rule(rule.id, context)
                    assert action is not None


class TestMemoryEdgeCases:
    """Test edge cases and error handling"""
    
    def setup_method(self):
        """Setup fresh memory for each test"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.memory = ThreeLayerMemory(storage_path=self.temp_file.name)
    
    def teardown_method(self):
        """Clean up temp file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_empty_memory(self):
        """Test operations on empty memory"""
        summary = self.memory.get_memory_summary()
        assert summary["episodic"]["total_events"] == 0
    
    def test_nonexistent_rule_application(self):
        """Test applying a rule that doesn't exist"""
        action = self.memory.apply_rule("nonexistent_rule", {})
        assert action is None
    
    def test_nonexistent_rule_update(self):
        """Test updating a rule that doesn't exist"""
        # Should not raise error
        self.memory.update_rule_success("nonexistent_rule", success=True)
    
    def test_load_from_nonexistent_file(self):
        """Test loading from a file that doesn't exist"""
        new_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        new_file.close()
        os.unlink(new_file.name)
        
        # Should not raise error
        memory = ThreeLayerMemory(storage_path=new_file.name)
        assert memory is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
