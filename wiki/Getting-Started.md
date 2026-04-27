# Getting Started with Cognitive Engine

This guide will help you install, configure, and run the Cognitive Engine.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (for cloning the repository)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd cognitive_engine
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# LLM Provider Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEFAULT_LLM_PROVIDER=openai  # or 'anthropic'

# Engine Configuration
MIN_ITERATIONS=3
MAX_ITERATIONS=50
EARLY_STOP_CONFIDENCE=0.95
CONFIDENCE_THRESHOLD=0.7

# Dashboard Configuration
ENABLE_DASHBOARD=true
DASHBOARD_PORT=8000

# Memory Configuration
MEMORY_DB_PATH=cognitive_engine.db
MAX_MEMORY_SIZE=10000

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=cognitive_engine.log
```

### Required API Keys

You need at least one LLM provider API key:

- **OpenAI**: Get your API key from https://platform.openai.com/api-keys
- **Anthropic**: Get your API key from https://console.anthropic.com/

## Running the Engine

### Interactive Mode

Run the engine in interactive mode for single queries:

```bash
python run.py
# or
python run.py interactive
```

Example session:
```
Cognitive Engine v1.0.0
Enter your query (or 'quit' to exit): What is the meaning of life?

[Processing thoughts...]
[Iteration 1/10] Generated 3 candidate thoughts
[Iteration 2/10] Deliberating on thoughts...
[Iteration 3/10] Confidence threshold reached

Answer: The meaning of life is a philosophical question...
```

### Agent Mode

Run the autonomous agent with goal-directed behavior:

```bash
python run.py agent
```

The agent will:
1. Accept a goal
2. Create a plan
3. Execute actions using tools
4. Observe results
5. Reflect and adapt

### Dashboard Mode

Start the real-time cognitive telemetry dashboard:

```bash
python run.py dashboard
```

Access the dashboard at: `http://localhost:8000`

The dashboard shows:
- Real-time thought generation
- Memory updates
- Strategy shifts
- Deliberation scoring
- Cognitive topology

### Test Mode

Run test suites:

```bash
python run.py test
```

## Usage Examples

### Basic Query

```python
from core.engine import CognitiveEngine

engine = CognitiveEngine()
result = engine.process("What is cognitive science?")
print(result.final_output)
```

### With Custom Configuration

```python
from core.engine import CognitiveEngine
from core.config import Config

config = Config(
    min_iterations=5,
    max_iterations=20,
    confidence_threshold=0.8
)

engine = CognitiveEngine(config)
result = engine.process("Explain quantum computing")
```

### Accessing Thought Graph

```python
from core.engine import CognitiveEngine

engine = CognitiveEngine()
result = engine.process("Compare Python and JavaScript")

# Access thought graph
for thought in engine.thought_graph.thoughts.values():
    print(f"Thought: {thought.premise}")
    print(f"Confidence: {thought.confidence}")
    print(f"Score: {thought.score}")
```

### Using Memory

```python
from core.engine import CognitiveEngine

engine = CognitiveEngine()

# Process multiple queries
engine.process("What is machine learning?")
engine.process("How do neural networks work?")

# Access memory
episodic = engine.memory.get_episodic_memory()
patterns = engine.memory.get_pattern_memory()
rules = engine.memory.get_rule_memory()

print(f"Episodic entries: {len(episodic)}")
print(f"Patterns found: {len(patterns)}")
print(f"Rules learned: {len(rules)}")
```

## Troubleshooting

### Common Issues

#### API Key Errors

**Error**: `API key not found`

**Solution**: Ensure your `.env` file contains the correct API key for your chosen LLM provider.

#### Memory Database Errors

**Error**: `SQLite database locked`

**Solution**: Ensure only one instance of the engine is running at a time, or configure a different database path.

#### Dashboard Connection Issues

**Error**: `WebSocket connection failed`

**Solution**: Check that the dashboard port is not in use and that `ENABLE_DASHBOARD=true` in your `.env` file.

#### Import Errors

**Error**: `ModuleNotFoundError: No module named 'xxx'`

**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Next Steps

- Read the [Architecture documentation](Architecture.md) to understand the system design
- Explore [Core Modules](Core-Modules.md) for detailed component documentation
- Check the [API documentation](API.md) for reference information
- Review the [Configuration Guide](Configuration.md) for advanced setup options

## Support

For issues or questions:
- **Email**: autobotsolution@gmail.com
- Check the logs in `cognitive_engine.log` for detailed error information
