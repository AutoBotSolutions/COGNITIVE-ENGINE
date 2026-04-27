# Development Guide

This guide covers development practices, contributing guidelines, and technical details for working on the Cognitive Engine codebase.

## Development Environment Setup

### Prerequisites

- Python 3.9 or higher
- Git
- pip

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd cognitive_engine
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install development dependencies**
```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8 mypy
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your development configuration
```

5. **Run tests**
```bash
python run.py test
```

## Project Structure

```
cognitive_engine/
├── core/                   # Core engine orchestration
│   ├── engine.py          # Main orchestration loop
│   ├── config.py          # Configuration management
│   ├── memory.py          # Three-layer memory system
│   ├── meta_cognition.py  # Meta-cognitive oversight
│   ├── reasoning_trace.py # Reasoning process tracking
│   ├── inner_knowing.py   # Self-awareness system
│   ├── self_doubt.py      # Uncertainty handling
│   ├── ethical_alignment.py # Ethical reasoning
│   ├── emotional_simulation.py # Emotional modeling
│   ├── decision_control.py # Decision management
│   ├── temporal_identity.py # Identity continuity
│   ├── peaceful_resolution.py # Conflict resolution
│   └── obedience_understanding.py # Authority analysis
├── models/                 # Data models
│   ├── thought.py         # Thought object
│   └── state.py           # Problem state
├── layers/                 # Cognitive layers
│   ├── interpreter.py     # Input interpretation
│   ├── generator.py       # Thought generation
│   ├── deliberator.py     # Thought deliberation
│   ├── committer.py       # Output commitment
│   └── meta.py            # Meta-cognition
├── utils/                  # Utilities
│   ├── scoring.py         # Thought scoring
│   ├── memory.py          # Memory utilities
│   └── logger.py          # Logging
├── llm/                    # LLM integration
│   ├── client.py          # LLM client
│   ├── prompts.py         # Prompt templates
│   └── knowledge_base.py  # Context management
├── agent/                  # Autonomous agent
│   ├── agent.py           # Main agent
│   ├── planner.py         # Goal planning
│   ├── executor.py        # Action execution
│   ├── observer.py        # Result observation
│   └── goals.py           # Goal definitions
├── tools/                  # Tool system
│   ├── registry.py        # Tool registry
│   ├── web_search.py      # Web search tool
│   └── code_exec.py       # Code execution tool
├── learning/               # Learning system
│   ├── extractor.py       # Pattern extraction
│   ├── patterns.py        # Pattern model
│   ├── synthesizer.py      # Rule synthesis
│   └── updater.py         # Knowledge update
├── prompt_evolution/       # Prompt evolution
│   ├── prompt_store.py    # Prompt versioning
│   ├── proposer.py        # Improvement suggestions
│   ├── tester.py          # A/B testing
│   ├── evaluator.py       # Performance evaluation
│   └── controller.py      # Change control
├── dashboard/              # Cognitive telemetry
│   ├── server.py          # WebSocket server
│   ├── stream.py          # Event streaming
│   └── events.py          # Event schemas
├── ui/                     # Dashboard UI
│   ├── index.html         # Main dashboard
│   ├── app.js             # Frontend logic
│   └── styles.css         # Styling
├── tests/                  # Test suite
├── docs/                   # Documentation
├── website/                # Website and wiki
│   └── wiki/              # Project wiki
├── run.py                  # Entry point
├── requirements.txt        # Dependencies
└── .env.example            # Environment template
```

## Code Style Guidelines

### Python Style

- Use **Black** for code formatting (120 character line length)
- Use **flake8** for linting
- Include **type hints** for all functions
- Write **Google-style docstrings**
- Follow **PEP 8** naming conventions:
  - PascalCase for classes
  - snake_case for functions and variables
  - UPPER_CASE for constants

### Example Code Style

```python
from typing import Optional, List, Dict, Any
from datetime import datetime


class ExampleClass:
    """
    A brief description of the class.
    
    Longer description if needed.
    
    Attributes:
        attribute1: Description of attribute1
        attribute2: Description of attribute2
    """
    
    def __init__(self, attribute1: str, attribute2: Optional[int] = None):
        """
        Initialize the ExampleClass.
        
        Args:
            attribute1: Description of attribute1
            attribute2: Description of attribute2 (optional)
        """
        self.attribute1 = attribute1
        self.attribute2 = attribute2
    
    def example_method(self, param: str) -> Dict[str, Any]:
        """
        A brief description of the method.
        
        Args:
            param: Description of param
            
        Returns:
            A dictionary containing the result
            
        Raises:
            ValueError: If param is invalid
        """
        if not param:
            raise ValueError("param cannot be empty")
        
        return {
            "result": param,
            "timestamp": datetime.now()
        }
```

### Formatting Commands

```bash
# Format code with Black
black cognitive_engine/

# Check linting with flake8
flake8 cognitive_engine/

# Type checking with mypy
mypy cognitive_engine/
```

## Testing

### Running Tests

```bash
# Run all tests
python run.py test

# Run specific test file
pytest tests/test_engine.py

# Run with coverage
pytest --cov=cognitive_engine tests/

# Run specific test
pytest tests/test_engine.py::test_process
```

### Writing Tests

Create test files in the `tests/` directory following the naming convention `test_<module>.py`.

```python
import pytest
from core.engine import CognitiveEngine


class TestCognitiveEngine:
    """Test suite for CognitiveEngine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = CognitiveEngine()
    
    def test_initialization(self):
        """Test engine initialization."""
        assert self.engine is not None
        assert self.engine.thought_graph is not None
    
    def test_process_basic_query(self):
        """Test processing a basic query."""
        result = self.engine.process("What is AI?")
        assert result is not None
        assert result.final_output is not None
        assert result.iteration_count > 0
```

### Test Coverage

Maintain test coverage above 80%. Check coverage with:

```bash
pytest --cov=cognitive_engine --cov-report=html
```

## Documentation

### Code Documentation

- All public classes and methods must have docstrings
- Use Google-style docstring format
- Include type hints in function signatures
- Document complex algorithms with inline comments

### Wiki Documentation

- Update the wiki in `website/wiki/` when adding features
- Keep API documentation in sync with code changes
- Update architecture documentation for structural changes
- Add examples for new features

### README Updates

- Update README.md for user-facing changes
- Update installation instructions for dependency changes
- Update configuration guide for new configuration options

## Contributing Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Follow code style guidelines
- Write tests for new functionality
- Update documentation
- Ensure all tests pass

### 3. Commit Changes

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

Example:
```
feat(generator): add thought refinement capability

Add ability to refine thoughts based on identified weaknesses.
This improves the quality of generated thoughts over iterations.

Closes #123
```

### 4. Run Tests

```bash
python run.py test
black cognitive_engine/
flake8 cognitive_engine/
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Create a pull request with:
- Clear description of changes
- Link to related issues
- Test results
- Documentation updates

## Architecture Principles

### Modularity

- Each module should have a single, well-defined responsibility
- Minimize dependencies between modules
- Use dependency injection where appropriate
- Define clear interfaces between components

### Testability

- Write code that is easy to test
- Avoid global state
- Use dependency injection for external dependencies
- Mock external services (LLM APIs, databases)

### Performance

- Profile before optimizing
- Consider caching for expensive operations
- Use async I/O for network operations
- Monitor memory usage

### Security

- Never commit API keys or secrets
- Validate all user inputs
- Use parameterized queries for database access
- Sanitize outputs from LLMs

### Maintainability

- Write clear, self-documenting code
- Use descriptive names
- Keep functions focused and small
- Document complex logic

## Common Development Tasks

### Adding a New Cognitive Layer

1. Create new file in `layers/` directory
2. Inherit from base layer pattern
3. Implement required methods
4. Add layer to engine initialization
5. Write tests
6. Update documentation

Example:
```python
# layers/new_layer.py
from typing import List
from models.thought import Thought


class NewLayer:
    """Description of new layer."""
    
    def process(self, thoughts: List[Thought]) -> List[Thought]:
        """Process thoughts."""
        # Implementation
        return thoughts
```

### Adding a New Tool

1. Create new file in `tools/` directory
2. Implement tool interface
3. Register tool in registry
4. Write tests
5. Update documentation

Example:
```python
# tools/new_tool.py
from typing import Dict, Any


class NewTool:
    """Description of new tool."""
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool."""
        # Implementation
        return {"result": "..."}
```

### Adding a New Memory Layer

1. Extend memory interface in `core/memory.py`
2. Implement storage and retrieval methods
3. Add to ThreeLayerMemory
4. Write tests
5. Update documentation

### Modifying Prompt Templates

1. Edit `llm/prompts.py`
2. Test with various inputs
3. Monitor performance impact
4. Update prompt evolution if enabled
5. Document changes

## Debugging

### Enabling Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Or set environment variable:
```env
LOG_LEVEL=DEBUG
```

### Using the Dashboard

Start the dashboard to visualize cognitive processes:

```bash
python run.py dashboard
```

Access at `http://localhost:8000`

### Inspecting Thought Graphs

```python
from core.engine import CognitiveEngine

engine = CognitiveEngine()
result = engine.process("Your query")

# Inspect thought graph
for thought_id, thought in engine.thought_graph.thoughts.items():
    print(f"ID: {thought_id}")
    print(f"Premise: {thought.premise}")
    print(f"Confidence: {thought.confidence}")
    print(f"Score: {thought.score}")
    print(f"Weaknesses: {thought.weaknesses}")
    print(f"History: {thought.history}")
    print("---")
```

### Memory Inspection

```python
from core.engine import CognitiveEngine

engine = CognitiveEngine()
result = engine.process("Your query")

# Inspect memory
memory = engine.get_memory()
episodic = memory.get_episodic_memory()
patterns = memory.get_pattern_memory()
rules = memory.get_rule_memory()

print(f"Episodic entries: {len(episodic)}")
print(f"Patterns: {len(patterns)}")
print(f"Rules: {len(rules)}")
```

## Performance Optimization

### Profiling

```python
import cProfile
import pstats

from core.engine import CognitiveEngine

engine = CognitiveEngine()

profiler = cProfile.Profile()
profiler.enable()

result = engine.process("Your query")

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

### Common Bottlenecks

1. **LLM API calls**: Cache responses where appropriate
2. **Memory operations**: Use indexing for faster queries
3. **Thought graph traversal**: Implement memoization
4. **Dashboard streaming**: Use batching for events

### Optimization Strategies

- Use async/await for I/O operations
- Implement caching for expensive computations
- Use connection pooling for database operations
- Batch operations where possible
- Consider using compiled extensions for performance-critical code

## Deployment

### Production Checklist

- [ ] Update configuration for production
- [ ] Set appropriate log levels
- [ ] Disable debug features
- [ ] Secure API keys
- [ ] Set up monitoring
- [ ] Configure backup for database
- [ ] Test in staging environment
- [ ] Document deployment process

### Docker Deployment

Example Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV LOG_LEVEL=INFO
ENV ENABLE_DASHBOARD=false

CMD ["python", "run.py"]
```

### Environment-Specific Configurations

Use different `.env` files for different environments:

- `.env.development` - Development settings
- `.env.staging` - Staging settings
- `.env.production` - Production settings

Load with:
```bash
export $(cat .env.production | xargs)
```

## Troubleshooting Development Issues

### Import Errors

**Problem**: `ModuleNotFoundError`

**Solutions**:
- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`
- Check PYTHONPATH includes project root

### Test Failures

**Problem**: Tests failing intermittently

**Solutions**:
- Check for external dependencies (API keys, network)
- Use mocking for external services
- Add retry logic for flaky tests
- Check for race conditions in async code

### Memory Leaks

**Problem**: Memory usage growing over time

**Solutions**:
- Profile memory usage
- Check for circular references
- Ensure proper cleanup in objects
- Limit memory size in configuration

### LLM API Rate Limits

**Problem**: Hitting API rate limits

**Solutions**:
- Implement exponential backoff
- Cache responses
- Use multiple API keys
- Reduce request frequency

## Resources

### Internal Documentation

- [Architecture Documentation](Architecture.md)
- [API Reference](API-Reference.md)
- [Core Modules](Core-Modules.md)
- [Configuration Guide](Configuration.md)

### External Resources

- Python Documentation: https://docs.python.org/
- Pydantic Documentation: https://docs.pydantic.dev/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- OpenAI API Documentation: https://platform.openai.com/docs
- Anthropic API Documentation: https://docs.anthropic.com/

## Support

For development questions:
- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- Check existing issues and documentation first
