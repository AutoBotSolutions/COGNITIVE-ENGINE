"""
Comprehensive Test Suite for Meta-Cognition Layer

Tests all aspects of the meta-cognition system including:
- Starting and stopping thinking sessions
- Should continue thinking decisions
- Stopping conditions
- Strategy adjustments
- Thinking metrics
- Decision history
"""

import pytest
from datetime import datetime
from core.meta_cognition import MetaCognition, ThinkingState, ThinkingMetrics, StoppingCondition


class TestThinkingMetrics:
    """Test ThinkingMetrics class"""
    
    def test_metrics_initialization(self):
        """Test metrics initialize with default values"""
        metrics = ThinkingMetrics()
        assert metrics.iteration == 0
        assert metrics.total_thoughts_generated == 0
        assert metrics.avg_confidence == 0.0
        assert metrics.max_confidence == 0.0
        assert metrics.thought_diversity == 0.0
    
    def test_update_confidence(self):
        """Test confidence tracking"""
        metrics = ThinkingMetrics()
        metrics.update_confidence(0.5)
        metrics.update_confidence(0.7)
        metrics.update_confidence(0.9)
        
        assert metrics.max_confidence == 0.9
        assert len(metrics.confidence_history) == 3
        assert metrics.avg_confidence == 0.7  # (0.5 + 0.7 + 0.9) / 3
    
    def test_calculate_convergence(self):
        """Test convergence calculation"""
        metrics = ThinkingMetrics()
        
        # Add converging values (low variance)
        for _ in range(10):
            metrics.update_confidence(0.8)
        
        convergence = metrics.calculate_convergence()
        assert convergence > 0.5  # Should be high due to low variance
    
    def test_diverse_confidence_values(self):
        """Test with diverse confidence values"""
        metrics = ThinkingMetrics()
        
        # Add diverse values (high variance)
        metrics.update_confidence(0.1)
        metrics.update_confidence(0.9)
        metrics.update_confidence(0.3)
        metrics.update_confidence(0.7)
        
        convergence = metrics.calculate_convergence()
        assert convergence < 0.8  # Should be lower due to high variance


class TestStoppingCondition:
    """Test StoppingCondition class"""
    
    def test_condition_creation(self):
        """Test creating a stopping condition"""
        condition = StoppingCondition(
            name="max_iterations",
            threshold=10,
            current_value=0
        )
        assert condition.name == "max_iterations"
        assert condition.threshold == 10
        assert condition.current_value == 0
        assert condition.triggered == False
    
    def test_condition_check(self):
        """Test condition checking"""
        condition = StoppingCondition(
            name="test",
            threshold=5,
            current_value=3
        )
        
        assert condition.check() == False
        
        condition.current_value = 5
        assert condition.check() == True
        assert condition.triggered == True


class TestMetaCognition:
    """Test MetaCognition class"""
    
    def setup_method(self):
        """Setup fresh meta-cognition for each test"""
        self.config = {
            "min_iterations": 2,
            "max_iterations": 10,
            "early_stop_confidence": 0.95,
            "confidence_threshold": 0.7
        }
        self.meta = MetaCognition(self.config)
    
    def test_initialization(self):
        """Test meta-cognition initializes correctly"""
        assert self.meta.min_iterations == 2
        assert self.meta.max_iterations == 10
        assert self.meta.early_stop_confidence == 0.95
        assert self.meta.confidence_threshold == 0.7
        assert self.meta.state == ThinkingState.INITIALIZING
    
    def test_start_thinking(self):
        """Test starting a thinking session"""
        self.meta.start_thinking()
        assert self.meta.state == ThinkingState.THINKING
        assert self.meta.start_time is not None
        assert len(self.meta.stopping_conditions) > 0
    
    def test_should_continue_at_start(self):
        """Test that thinking continues at the start"""
        self.meta.start_thinking()
        should_continue, reason = self.meta.should_continue_thinking(0.0, 1.0)
        
        assert should_continue == True  # Should continue due to min_iterations
        assert "minimum" in reason.lower()
    
    def test_max_iterations_stopping(self):
        """Test stopping at max iterations"""
        self.meta.start_thinking()
        
        # Simulate reaching max iterations
        for _ in range(self.config["max_iterations"] + 1):
            should_continue, reason = self.meta.should_continue_thinking(0.5, 1.0)
        
        assert should_continue == False
        assert "maximum" in reason.lower()
    
    def test_early_stop_high_confidence(self):
        """Test early stopping with high confidence"""
        self.meta.start_thinking()
        
        # Simulate iterations
        for _ in range(self.config["min_iterations"]):
            self.meta.should_continue_thinking(0.5, 1.0)
        
        # High confidence should trigger early stop
        should_continue, reason = self.meta.should_continue_thinking(
            self.config["early_stop_confidence"] + 0.01,
            1.0
        )
        
        assert should_continue == False
        assert "confidence" in reason.lower()
    
    def test_convergence_stopping(self):
        """Test stopping when converged"""
        self.meta.start_thinking()
        
        # Simulate converging confidence
        for _ in range(self.config["min_iterations"]):
            self.meta.should_continue_thinking(0.8, 1.0)
        
        # Converged with sufficient confidence
        should_continue, reason = self.meta.should_continue_thinking(
            self.config["confidence_threshold"] + 0.1,
            1.0
        )
        
        # Should stop if converged
        assert should_continue == False or "converged" in reason.lower()
    
    def test_stuck_detection(self):
        """Test detection of being stuck"""
        self.meta.start_thinking()
        
        # Simulate high confidence that doesn't improve
        for _ in range(10):
            self.meta.should_continue_thinking(0.9, 1.0)
        
        # Should detect being stuck
        is_stuck = self.meta._is_stuck()
        assert is_stuck == True
    
    def test_strategy_adjustment(self):
        """Test strategy adjustment"""
        self.meta.start_thinking()
        
        self.meta.adjust_strategy(
            situation="low confidence",
            adjustment={"max_iterations": 20}
        )
        
        assert self.meta.max_iterations == 20
        assert len(self.meta.strategy_adjustments) == 1
    
    def test_decision_history(self):
        """Test decision history tracking"""
        self.meta.start_thinking()
        
        # Make some decisions
        for _ in range(3):
            self.meta.should_continue_thinking(0.5, 1.0)
        
        assert len(self.meta.decision_history) >= 3
    
    def test_explain_decision(self):
        """Test explaining a decision"""
        self.meta.start_thinking()
        self.meta.should_continue_thinking(0.5, 1.0)
        
        explanation = self.meta.explain_decision()
        assert explanation is not None
        assert len(explanation) > 0
        assert "Iteration" in explanation
    
    def test_stop_thinking(self):
        """Test manually stopping thinking"""
        self.meta.start_thinking()
        self.meta.stop_thinking(reason="manual stop")
        
        assert self.meta.state == ThinkingState.STOPPED
        assert len(self.meta.decision_history) >= 1
    
    def test_reset(self):
        """Test resetting meta-cognition"""
        self.meta.start_thinking()
        self.meta.should_continue_thinking(0.5, 1.0)
        
        self.meta.reset()
        
        assert self.meta.state == ThinkingState.INITIALIZING
        assert self.meta.metrics.iteration == 0
        assert len(self.meta.decision_history) == 0
    
    def test_get_thinking_summary(self):
        """Test getting thinking summary"""
        self.meta.start_thinking()
        self.meta.should_continue_thinking(0.5, 1.0)
        
        summary = self.meta.get_thinking_summary()
        
        assert "state" in summary
        assert "iteration" in summary
        assert "confidence" in summary
        assert "stopping_conditions" in summary


class TestMetaCognitionEdgeCases:
    """Test edge cases and error handling"""
    
    def test_zero_diversity(self):
        """Test with zero thought diversity"""
        meta = MetaCognition()
        meta.start_thinking()
        
        should_continue, reason = meta.should_continue_thinking(0.5, 0.0)
        assert should_continue is not None
    
    def test_extreme_confidence(self):
        """Test with extreme confidence values"""
        meta = MetaCognition()
        meta.start_thinking()
        
        # Very high confidence
        should_continue, reason = meta.should_continue_thinking(1.0, 1.0)
        assert should_continue is not None
        
        # Very low confidence
        should_continue, reason = meta.should_continue_thinking(0.0, 1.0)
        assert should_continue is not None
    
    def test_without_starting(self):
        """Test operations without starting session"""
        meta = MetaCognition()
        
        # Should handle gracefully
        should_continue, reason = meta.should_continue_thinking(0.5, 1.0)
        # May or may not continue depending on implementation
    
    def test_multiple_sessions(self):
        """Test multiple thinking sessions"""
        meta = MetaCognition()
        
        # First session
        meta.start_thinking()
        meta.should_continue_thinking(0.5, 1.0)
        meta.stop_thinking()
        
        # Second session
        meta.start_thinking()
        meta.should_continue_thinking(0.7, 1.0)
        
        assert meta.metrics.iteration > 0


class TestMetaCognitionIntegration:
    """Integration tests for meta-cognition"""
    
    def setup_method(self):
        """Setup for integration tests"""
        self.meta = MetaCognition({
            "min_iterations": 1,
            "max_iterations": 5,
            "early_stop_confidence": 0.9,
            "confidence_threshold": 0.7
        })
    
    def test_full_thinking_session(self):
        """Test a complete thinking session"""
        self.meta.start_thinking()
        
        iteration_count = 0
        while True:
            should_continue, reason = self.meta.should_continue_thinking(
                0.5 + (iteration_count * 0.1),
                1.0
            )
            iteration_count += 1
            
            if not should_continue:
                break
        
        assert iteration_count >= self.meta.min_iterations
        assert self.meta.state == ThinkingState.STOPPED
    
    def test_adaptive_strategy(self):
        """Test adaptive strategy adjustment"""
        self.meta.start_thinking()
        
        # Simulate poor performance
        for _ in range(3):
            self.meta.should_continue_thinking(0.3, 1.0)
        
        # Adjust strategy
        self.meta.adjust_strategy(
            situation="low confidence",
            adjustment={"confidence_threshold": 0.5}
        )
        
        # Should now be more lenient
        should_continue, reason = self.meta.should_continue_thinking(0.45, 1.0)
        assert should_continue == True
    
    def test_stopping_conditions_tracking(self):
        """Test that all stopping conditions are checked"""
        self.meta.start_thinking()
        
        # Iterate to trigger various conditions
        for i in range(10):
            self.meta.should_continue_thoughts(0.5, 1.0)
        
        # Check that conditions were evaluated
        for condition in self.meta.stopping_conditions:
            assert condition.current_value >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
