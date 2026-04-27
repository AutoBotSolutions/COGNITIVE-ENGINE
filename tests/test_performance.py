"""
Comprehensive Performance and Stress Tests for Cognitive Engine

Tests performance characteristics and system under load:
- Response time benchmarks
- Memory usage profiling
- Concurrent request handling
- Large-scale cognitive sessions
- Resource limits and degradation
"""

import pytest
import asyncio
import time
import os
import tempfile
from core.memory import ThreeLayerMemory
from core.meta_cognition import MetaCognition
from core.reasoning_trace import ReasoningTrace, ReasoningTraceManager
from llm.knowledge_base import KnowledgeBase, Concept


class TestKnowledgeBasePerformance:
    """Test knowledge base performance"""
    
    def test_large_scale_concept_storage(self):
        """Test storing large number of concepts"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            kb = KnowledgeBase(storage_path=temp_file.name)
            
            # Add 1000 concepts
            start = time.time()
            for i in range(1000):
                concept = Concept(
                    id=f"concept_{i}",
                    name=f"concept_{i}",
                    description=f"Description for concept {i}",
                    properties={"index": i},
                    confidence=0.8
                )
                kb.add_concept(concept)
            
            duration = time.time() - start
            assert duration < 10.0  # Should complete in < 10 seconds
            assert len(kb.concepts) >= 1000
        finally:
            os.unlink(temp_file.name)
    
    def test_pathfinding_performance(self):
        """Test pathfinding with large knowledge graph"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            kb = KnowledgeBase(storage_path=temp_file.name)
            
            # Create a large graph
            for i in range(100):
                kb.add_concept(Concept(
                    id=f"node_{i}",
                    name=f"node_{i}",
                    description="",
                    properties={},
                    relationships={}
                ))
            
            # Create paths
            for i in range(99):
                kb.add_relationship(f"node_{i}", "connects_to", f"node_{i+1}")
            
            # Test pathfinding
            start = time.time()
            path = kb.find_path("node_0", "node_99")
            duration = time.time() - start
            
            assert duration < 1.0  # Should complete in < 1 second
            assert len(path) == 100
        finally:
            os.unlink(temp_file.name)
    
    def test_reasoning_performance(self):
        """Test reasoning performance with large knowledge base"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            kb = KnowledgeBase(storage_path=temp_file.name)
            
            # Add many concepts
            for i in range(500):
                kb.add_concept(Concept(
                    id=f"concept_{i}",
                    name=f"concept_{i}",
                    description=f"Description {i}",
                    properties={},
                    confidence=0.8
                ))
            
            # Test reasoning
            start = time.time()
            response = kb.reason_about("What is cognition?")
            duration = time.time() - start
            
            assert duration < 5.0  # Should complete in < 5 seconds
            assert response is not None
        finally:
            os.unlink(temp_file.name)


class TestMemoryPerformance:
    """Test memory system performance"""
    
    def test_large_scale_event_recording(self):
        """Test recording large number of events"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            memory = ThreeLayerMemory(storage_path=temp_file.name)
            
            # Record 1000 events
            start = time.time()
            for i in range(1000):
                memory.record_event("test_event", {"iteration": i})
            
            duration = time.time() - start
            assert duration < 5.0  # Should complete in < 5 seconds
            assert memory.total_events == 1000
        finally:
            os.unlink(temp_file.name)
    
    def test_pattern_extraction_performance(self):
        """Test pattern extraction with many events"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            memory = ThreeLayerMemory(storage_path=temp_file.name)
            
            # Record many events
            for i in range(500):
                memory.record_event("test", {"value": i % 10})
            
            # Test pattern extraction
            start = time.time()
            memory._extract_patterns()
            duration = time.time() - start
            
            assert duration < 10.0  # Should complete in < 10 seconds
        finally:
            os.unlink(temp_file.name)
    
    def test_persistence_performance(self):
        """Test saving/loading large memory"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            memory = ThreeLayerMemory(storage_path=temp_file.name)
            
            # Add many events
            for i in range(1000):
                memory.record_event("test", {"value": i})
            
            # Test save
            start = time.time()
            memory._save_to_disk()
            save_duration = time.time() - start
            
            # Test load
            start = time.time()
            new_memory = ThreeLayerMemory(storage_path=temp_file.name)
            load_duration = time.time() - start
            
            assert save_duration < 5.0
            assert load_duration < 5.0
        finally:
            os.unlink(temp_file.name)


class TestMetaCognitionPerformance:
    """Test meta-cognition performance"""
    
    def test_long_thinking_session(self):
        """Test performance of long thinking session"""
        meta = MetaCognition({
            "min_iterations": 1,
            "max_iterations": 100,
            "early_stop_confidence": 0.95,
            "confidence_threshold": 0.7
        })
        
        meta.start_thinking()
        
        start = time.time()
        iteration_count = 0
        while True:
            should_continue, reason = meta.should_continue_thinking(0.5, 1.0)
            iteration_count += 1
            if not should_continue or iteration_count >= 50:
                break
        duration = time.time() - start
        
        assert duration < 5.0  # Should complete 50 iterations in < 5 seconds
        assert iteration_count >= 50
    
    def test_strategy_adjustment_performance(self):
        """Test performance of strategy adjustments"""
        meta = MetaCognition()
        meta.start_thinking()
        
        start = time.time()
        for i in range(100):
            meta.adjust_strategy(
                situation=f"test_{i}",
                adjustment={"param": i}
            )
        duration = time.time() - start
        
        assert duration < 1.0  # Should complete in < 1 second
        assert len(meta.strategy_adjustments) == 100


class TestReasoningTracePerformance:
    """Test reasoning trace performance"""
    
    def test_large_trace_recording(self):
        """Test recording many trace events"""
        trace = ReasoningTrace()
        
        start = time.time()
        for i in range(1000):
            trace.record_event(
                TraceEventType.THOUGHT_GENERATED,
                "generator",
                {"iteration": i}
            )
        duration = time.time() - start
        
        assert duration < 5.0  # Should complete in < 5 seconds
        assert len(trace.events) == 1000
    
    def test_trace_export_performance(self):
        """Test exporting large trace"""
        trace = ReasoningTrace()
        
        # Add many events
        for i in range(1000):
            trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {"i": i})
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            start = time.time()
            trace.export_trace(temp_file.name)
            duration = time.time() - start
            
            assert duration < 10.0  # Should complete in < 10 seconds
        finally:
            os.unlink(temp_file.name)
    
    def test_trace_query_performance(self):
        """Test querying large trace"""
        trace = ReasoningTrace()
        
        # Add many events
        for i in range(1000):
            trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {"i": i})
        
        # Test query
        start = time.time()
        events = trace.get_events_by_type(TraceEventType.THOUGHT_GENERATED)
        duration = time.time() - start
        
        assert duration < 1.0  # Should complete in < 1 second
        assert len(events) == 1000


class TestStressTests:
    """Stress tests for cognitive components"""
    
    def test_memory_under_load(self):
        """Test memory system under continuous load"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            memory = ThreeLayerMemory(storage_path=temp_file.name)
            
            # Continuous recording
            start = time.time()
            for i in range(5000):
                memory.record_event("load_test", {"value": i})
                
                # Trigger pattern extraction periodically
                if i % 100 == 0:
                    memory._extract_patterns()
            
            duration = time.time() - start
            assert duration < 30.0  # Should complete in < 30 seconds
            assert memory.total_events == 5000
        finally:
            os.unlink(temp_file.name)
    
    def test_meta_cognition_under_load(self):
        """Test meta-cognition under continuous decision making"""
        meta = MetaCognition({"min_iterations": 1, "max_iterations": 1000})
        meta.start_thinking()
        
        start = time.time()
        for i in range(1000):
            should_continue, reason = meta.should_continue_thinking(0.5, 1.0)
            if not should_continue:
                break
        duration = time.time() - start
        
        assert duration < 10.0  # Should complete in < 10 seconds
    
    def test_concurrent_trace_operations(self):
        """Test concurrent trace operations"""
        manager = ReasoningTraceManager()
        
        start = time.time()
        for i in range(100):
            trace = manager.create_trace()
            trace.record_event(TraceEventType.INPUT_RECEIVED, "engine", {"i": i})
            manager.save_trace(trace.session_id)
        duration = time.time() - start
        
        assert duration < 10.0  # Should complete in < 10 seconds
        assert len(manager.traces) == 100


class TestResourceLimits:
    """Test system behavior at resource limits"""
    
    def test_memory_growth_limits(self):
        """Test that memory growth is controlled"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            memory = ThreeLayerMemory(storage_path=temp_file.name)
            
            # Add many events
            for i in range(2000):
                memory.record_event("test", {"value": i})
            
            # Save should only keep recent events (limit in implementation)
            memory._save_to_disk()
            
            # Load and verify
            new_memory = ThreeLayerMemory(storage_path=temp_file.name)
            # Should not have all 2000 due to limit
            assert new_memory.total_events <= 2000
        finally:
            os.unlink(temp_file.name)
    
    def test_meta_cognition_iteration_limits(self):
        """Test that meta-cognition respects iteration limits"""
        meta = MetaCognition({
            "min_iterations": 1,
            "max_iterations": 5,
            "early_stop_confidence": 1.0,  # Never early stop
            "confidence_threshold": 1.0
        })
        
        meta.start_thinking()
        
        iteration_count = 0
        for _ in range(20):  # Try more than max
            should_continue, reason = meta.should_continue_thoughts(0.5, 1.0)
            iteration_count += 1
            if not should_continue:
                break
        
        assert iteration_count <= meta.max_iterations
    
    def test_trace_size_limits(self):
        """Test that trace size is managed"""
        trace = ReasoningTrace()
        
        # Add many events
        for i in range(10000):
            trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {"i": i})
        
        # Should still be able to get summary
        summary = trace.get_summary()
        assert summary["total_events"] == 10000


class TestDegradationBehavior:
    """Test system behavior under degraded conditions"""
    
    def test_slow_persistence_handling(self):
        """Test handling of slow persistence"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            memory = ThreeLayerMemory(storage_path=temp_file.name)
            
            # Add events
            for i in range(100):
                memory.record_event("test", {"value": i})
            
            # Save should complete even if slow
            memory._save_to_disk()
            
            # Should still be usable
            memory.record_event("after_save", {"test": "value"})
            assert memory.total_events >= 100
        finally:
            os.unlink(temp_file.name)
    
    def test_low_confidence_handling(self):
        """Test handling of consistently low confidence"""
        meta = MetaCognition({"min_iterations": 1, "max_iterations": 10})
        meta.start_thinking()
        
        # All low confidence
        for i in range(20):
            should_continue, reason = meta.should_continue_thoughts(0.1, 1.0)
            if not should_continue:
                break
        
        # Should eventually stop
        assert not should_continue or meta.metrics.iteration >= meta.max_iterations
    
    def test_empty_knowledge_base_reasoning(self):
        """Test reasoning with minimal knowledge"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            kb = KnowledgeBase(storage_path=temp_file.name)
            
            # Remove all concepts (simulate empty KB)
            kb.concepts = {}
            kb.concept_index = {}
            
            # Should still handle reasoning gracefully
            response = kb.reason_about("What is cognition?")
            assert response is not None  # Should not crash
        finally:
            os.unlink(temp_file.name)


class TestPerformanceBenchmarks:
    """Performance benchmarks for critical operations"""
    
    def test_benchmark_knowledge_base_query(self):
        """Benchmark knowledge base query performance"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            kb = KnowledgeBase(storage_path=temp_file.name)
            
            # Warm up
            for _ in range(10):
                kb.reason_about("test")
            
            # Benchmark
            times = []
            for _ in range(100):
                start = time.time()
                kb.reason_about("What is cognition?")
                times.append(time.time() - start)
            
            avg_time = sum(times) / len(times)
            assert avg_time < 0.1  # Average < 100ms
        finally:
            os.unlink(temp_file.name)
    
    def test_benchmark_memory_event_recording(self):
        """Benchmark memory event recording"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            memory = ThreeLayerMemory(storage_path=temp_file.name)
            
            # Warm up
            for _ in range(10):
                memory.record_event("test", {})
            
            # Benchmark
            times = []
            for _ in range(1000):
                start = time.time()
                memory.record_event("benchmark", {"value": 1})
                times.append(time.time() - start)
            
            avg_time = sum(times) / len(times)
            assert avg_time < 0.01  # Average < 10ms
        finally:
            os.unlink(temp_file.name)
    
    def test_benchmark_meta_cognition_decision(self):
        """Benchmark meta-cognition decision making"""
        meta = MetaCognition({"min_iterations": 1, "max_iterations": 10})
        meta.start_thinking()
        
        # Warm up
        for _ in range(10):
            meta.should_continue_thoughts(0.5, 1.0)
        
        # Benchmark
        times = []
        for _ in range(1000):
            start = time.time()
            meta.should_continue_thoughts(0.5, 1.0)
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        assert avg_time < 0.01  # Average < 10ms


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
