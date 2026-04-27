# Cognitive Engine Test Suite

Comprehensive testing system for all cognitive components.

## Test Files

### Component Tests
- **test_knowledge_base.py** - Tests for knowledge base system
  - Concept creation and storage
  - Relationship management
  - Pathfinding and reasoning
  - Learning from interactions
  - Persistence

- **test_memory.py** - Tests for three-layer memory architecture
  - Episodic memory (raw events)
  - Pattern memory (structure extraction)
  - Rule memory (learned strategies)
  - Learning pipeline
  - Persistence

- **test_meta_cognition.py** - Tests for meta-cognition layer
  - Starting and stopping thinking sessions
  - Should continue thinking decisions
  - Stopping conditions
  - Strategy adjustments
  - Thinking metrics

- **test_reasoning_trace.py** - Tests for reasoning trace system
  - Trace event recording
  - Thought evaluation tracking
  - Thought evolution tracking
  - Query capabilities
  - Reasoning chain reconstruction

### Integration Tests
- **test_integration.py** - Integration tests for full cognitive pipeline
  - Component interaction
  - Data flow integrity
  - End-to-end cognitive sessions
  - Error handling across components

### Performance Tests
- **test_performance.py** - Performance and stress tests
  - Response time benchmarks
  - Memory usage profiling
  - Large-scale operations
  - Resource limits
  - Degradation behavior

## Running Tests

### Run All Tests
```bash
cd /home/robbie/Desktop/cognitive_engine
python3 -m pytest tests/ -v
```

### Run Specific Test File
```bash
python3 -m pytest tests/test_knowledge_base.py -v
```

### Run Specific Test Class
```bash
python3 -m pytest tests/test_memory.py::TestEpisodicMemory -v
```

### Run Specific Test
```bash
python3 -m pytest tests/test_meta_cognition.py::TestMetaCognition::test_start_thinking -v
```

### Run Performance Tests Only
```bash
python3 -m pytest tests/test_performance.py -v
```

### Run with Coverage
```bash
python3 -m pytest tests/ --cov=. --cov-report=html
```

## Test Structure

Each test file follows this structure:
- **Unit tests** - Test individual components in isolation
- **Integration tests** - Test component interactions
- **Edge case tests** - Test error handling and boundary conditions
- **Performance tests** - Test performance characteristics

## Test Coverage

The test suite covers:
- ✅ Knowledge base system (concepts, relationships, reasoning, learning)
- ✅ Three-layer memory (episodic, pattern, rule)
- ✅ Meta-cognition (oversight, decision making, strategy adjustment)
- ✅ Reasoning trace (event recording, query capabilities, persistence)
- ✅ Full cognitive pipeline integration
- ✅ Performance and stress testing

## Continuous Integration

To run tests in CI:
```bash
python3 -m pytest tests/ -v --tb=short --maxfail=5
```

## Test Data

Tests use temporary files that are automatically cleaned up. No test data is committed to the repository.

## Adding New Tests

When adding new cognitive components:
1. Create a new test file following the naming convention `test_<component>.py`
2. Include unit tests, integration tests, edge cases, and performance tests
3. Use pytest fixtures for setup/teardown
4. Clean up temporary resources in teardown methods
5. Update this README with the new test file description
