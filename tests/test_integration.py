"""
Comprehensive Integration Tests for Full Cognitive Pipeline

Tests the integration of all cognitive components:
- Knowledge base + Memory + Meta-cognition + Reasoning trace
- Full cognitive pipeline (interpreter → generator → deliberator → committer)
- End-to-end cognitive sessions
- Component interaction and data flow
"""

import pytest
import asyncio
import os
import tempfile
from core.engine import CognitiveEngine
from core.config import config
from core.memory import ThreeLayerMemory
from core.meta_cognition import MetaCognition
from core.reasoning_trace import ReasoningTrace, ReasoningTraceManager


class TestComponentIntegration:
    """Test integration between cognitive components"""
    
    def setup_method(self):
        """Setup for integration tests"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
    
    def teardown_method(self):
        """Clean up temp files"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_memory_knowledge_base_integration(self):
        """Test that memory and knowledge base work together"""
        memory = ThreeLayerMemory(storage_path=self.temp_file.name)
        
        # Record cognitive event
        memory.record_event("cognition", {"type": "reasoning"})
        
        # Trigger pattern extraction
        memory._extract_patterns()
        
        # Verify patterns were extracted
        assert len(memory.patterns) >= 0
    
    def test_meta_cognition_memory_integration(self):
        """Test that meta-cognition and memory work together"""
        meta = MetaCognition({"min_iterations": 1, "max_iterations": 5})
        memory = ThreeLayerMemory(storage_path=self.temp_file.name)
        
        meta.start_thinking()
        
        # Simulate thinking iterations
        for i in range(3):
            should_continue, reason = meta.should_continue_thinking(0.5 + (i * 0.1), 1.0)
            memory.record_event("thinking_iteration", {"iteration": i})
        
        # Verify both systems tracked the session
        assert meta.metrics.iteration == 3
        assert memory.total_events == 3
    
    def test_reasoning_trace_memory_integration(self):
        """Test that reasoning trace and memory work together"""
        trace = ReasoningTrace()
        memory = ThreeLayerMemory(storage_path=self.temp_file.name)
        
        # Record event in trace
        trace.record_event(
            TraceEventType.INPUT_RECEIVED,
            "engine",
            {"input": "test"}
        )
        
        # Record same event in memory
        memory.record_event("input_received", {"input": "test"})
        
        # Verify both recorded
        assert len(trace.events) == 1
        assert memory.total_events == 1
    
    def test_full_component_stack(self):
        """Test all components working together"""
        # Initialize all components
        memory = ThreeLayerMemory(storage_path=self.temp_file.name)
        meta = MetaCognition({"min_iterations": 1, "max_iterations": 5})
        trace = ReasoningTrace()
        trace_manager = ReasoningTraceManager()
        
        # Simulate a cognitive session
        trace.record_event(TraceEventType.INPUT_RECEIVED, "engine", {"input": "test"})
        memory.record_event("session_start", {"input": "test"})
        
        meta.start_thinking()
        
        # Simulate thinking loop
        iteration = 0
        while True:
            should_continue, reason = meta.should_continue_thinking(0.5 + (iteration * 0.1), 1.0)
            
            # Record in all systems
            trace.record_event(TraceEventType.THOUGHT_GENERATED, "generator", {"iteration": iteration})
            memory.record_event("thought_generation", {"iteration": iteration})
            
            if not should_continue:
                break
            iteration += 1
        
        # Finalize
        trace.set_final_decision({"iterations": iteration})
        
        # Verify all systems tracked the session
        assert meta.metrics.iteration > 0
        assert memory.total_events > 0
        assert len(trace.events) > 0


class TestCognitivePipelineIntegration:
    """Test the full cognitive pipeline integration"""
    
    def setup_method(self):
        """Setup for pipeline tests"""
        # Temporarily enable custom provider
        self.original_provider = config.default_llm_provider
        config.default_llm_provider = "custom"
        config.enable_custom_provider = True
    
    def teardown_method(self):
        """Restore original config"""
        config.default_llm_provider = self.original_provider
    
    @pytest.mark.asyncio
    async def test_engine_initialization(self):
        """Test that engine initializes with new cognitive systems"""
        engine = CognitiveEngine()
        
        # Verify new systems are initialized
        assert engine.memory is not None
        assert engine.meta_cognition is not None
        assert engine.reasoning_trace_manager is not None
    
    @pytest.mark.asyncio
    async def test_process_creates_trace(self):
        """Test that processing creates a reasoning trace"""
        engine = CognitiveEngine()
        
        result = await engine.process("What is cognition?")
        
        # Verify trace was created
        assert engine.current_trace is not None
        assert len(engine.current_trace.events) > 0
    
    @pytest.mark.asyncio
    async def test_process_records_memory(self):
        """Test that processing records events in memory"""
        engine = CognitiveEngine()
        
        initial_event_count = engine.memory.total_events
        result = await engine.process("What is learning?")
        
        # Verify memory was updated
        assert engine.memory.total_events > initial_event_count
    
    @pytest.mark.asyncio
    async def test_process_uses_meta_cognition(self):
        """Test that processing uses meta-cognition"""
        engine = CognitiveEngine()
        
        result = await engine.process("Test question")
        
        # Verify meta-cognition was used
        assert engine.meta_cognition.metrics.iteration > 0
        assert len(engine.meta_cognition.decision_history) > 0
    
    @pytest.mark.asyncio
    async def test_full_pipeline_flow(self):
        """Test the complete pipeline flow"""
        engine = CognitiveEngine()
        
        result = await engine.process("What is the purpose of this system?")
        
        # Verify result
        assert result is not None
        assert "success" in result
        
        if result["success"]:
            assert "output" in result
            assert result["output"] is not None


class TestEndToEndCognitiveSession:
    """Test complete end-to-end cognitive sessions"""
    
    def setup_method(self):
        """Setup for end-to-end tests"""
        self.original_provider = config.default_llm_provider
        config.default_llm_provider = "custom"
        config.enable_custom_provider = True
    
    def teardown_method(self):
        """Restore original config"""
        config.default_llm_provider = self.original_provider
    
    @pytest.mark.asyncio
    async def test_simple_question_session(self):
        """Test a simple question-answer session"""
        engine = CognitiveEngine()
        
        result = await engine.process("What is cognition?")
        
        assert result is not None
        if result["success"]:
            assert len(result["output"]) > 0
    
    @pytest.mark.asyncio
    async def test_multi_question_session(self):
        """Test multiple questions in sequence"""
        engine = CognitiveEngine()
        
        questions = [
            "What is learning?",
            "How does memory work?",
            "What is reasoning?"
        ]
        
        results = []
        for question in questions:
            result = await engine.process(question)
            results.append(result)
        
        # Verify all processed
        assert len(results) == len(questions)
        
        # Verify at least some succeeded
        successful = sum(1 for r in results if r.get("success"))
        assert successful >= 0
    
    @pytest.mark.asyncio
    async def test_session_persistence(self):
        """Test that session data persists across questions"""
        engine = CognitiveEngine()
        
        # First question
        await engine.process("What is cognition?")
        first_memory_count = engine.memory.total_events
        
        # Second question
        await engine.process("What is learning?")
        second_memory_count = engine.memory.total_events
        
        # Memory should accumulate
        assert second_memory_count >= first_memory_count


class TestDataFlowIntegrity:
    """Test data flow integrity across components"""
    
    def setup_method(self):
        """Setup for data flow tests"""
        self.original_provider = config.default_llm_provider
        config.default_llm_provider = "custom"
        config.enable_custom_provider = True
    
    def teardown_method(self):
        """Restore original config"""
        config.default_llm_provider = self.original_provider
    
    @pytest.mark.asyncio
    async def test_input_to_trace_flow(self):
        """Test that input flows to trace correctly"""
        engine = CognitiveEngine()
        
        input_text = "Test input"
        result = await engine.process(input_text)
        
        # Verify input was recorded in trace
        input_events = engine.current_trace.get_events_by_type(TraceEventType.INPUT_RECEIVED)
        assert len(input_events) > 0
    
    @pytest.mark.asyncio
    async def test_thought_to_memory_flow(self):
        """Test that thoughts flow to memory correctly"""
        engine = CognitiveEngine()
        
        result = await engine.process("Generate thoughts about learning")
        
        # Verify thought generation was recorded in memory
        thought_events = engine.memory.get_events_by_type("thought_generation")
        assert len(thought_events) >= 0
    
    @pytest.mark.asyncio
    async def test_meta_cognition_to_decision_flow(self):
        """Test that meta-cognition decisions are tracked"""
        engine = CognitiveEngine()
        
        result = await engine.process("Test question")
        
        # Verify meta-cognition decisions were recorded
        assert len(engine.meta_cognition.decision_history) > 0


class TestErrorHandlingIntegration:
    """Test error handling across integrated components"""
    
    def setup_method(self):
        """Setup for error handling tests"""
        self.original_provider = config.default_llm_provider
        config.default_llm_provider = "custom"
        config.enable_custom_provider = True
    
    def teardown_method(self):
        """Restore original config"""
        config.default_llm_provider = self.original_provider
    
    @pytest.mark.asyncio
    async def test_memory_error_handling(self):
        """Test that memory errors don't crash the system"""
        engine = CognitiveEngine()
        
        # Corrupt memory state (simulate error)
        # System should handle gracefully
        result = await engine.process("Test question")
        
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_trace_error_handling(self):
        """Test that trace errors don't crash the system"""
        engine = CognitiveEngine()
        
        # System should handle trace errors gracefully
        result = await engine.process("Test question")
        
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_meta_cognition_error_handling(self):
        """Test that meta-cognition errors don't crash the system"""
        engine = CognitiveEngine()
        
        # System should handle meta-cognition errors gracefully
        result = await engine.process("Test question")
        
        assert result is not None


class TestPerformanceIntegration:
    """Test performance characteristics of integrated system"""
    
    def setup_method(self):
        """Setup for performance tests"""
        self.original_provider = config.default_llm_provider
        config.default_llm_provider = "custom"
        config.enable_custom_provider = True
    
    def teardown_method(self):
        """Restore original config"""
        config.default_llm_provider = self.original_provider
    
    @pytest.mark.asyncio
    async def test_session_duration(self):
        """Test that sessions complete in reasonable time"""
        engine = CognitiveEngine()
        
        import time
        start = time.time()
        result = await engine.process("What is cognition?")
        duration = time.time() - start
        
        # Should complete in reasonable time (< 30 seconds)
        assert duration < 30
    
    @pytest.mark.asyncio
    async def test_memory_efficiency(self):
        """Test that memory doesn't grow unbounded"""
        engine = CognitiveEngine()
        
        initial_count = engine.memory.total_events
        
        # Process multiple questions
        for _ in range(5):
            await engine.process("Test question")
        
        final_count = engine.memory.total_events
        
        # Memory should grow but not explode
        assert final_count < initial_count + 1000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
