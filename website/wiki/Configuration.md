# Configuration Guide

This guide explains how to configure the Cognitive Engine for different use cases.

## Environment Variables

The Cognitive Engine can be configured using environment variables or a `.env` file.

### Required Variables

#### LLM Provider Configuration

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEFAULT_LLM_PROVIDER=openai
```

**OPENAI_API_KEY**: Your OpenAI API key. Get it from https://platform.openai.com/api-keys

**ANTHROPIC_API_KEY**: Your Anthropic API key. Get it from https://console.anthropic.com/

**DEFAULT_LLM_PROVIDER**: Which LLM provider to use by default. Options: `openai` or `anthropic`

**Note**: You need at least one API key configured. The system will use the available provider.

### Optional Variables

#### Engine Configuration

```env
MIN_ITERATIONS=3
MAX_ITERATIONS=50
EARLY_STOP_CONFIDENCE=0.95
CONFIDENCE_THRESHOLD=0.7
```

**MIN_ITERATIONS**: Minimum number of cognitive iterations before considering early stop. Default: `3`

**MAX_ITERATIONS**: Maximum number of cognitive iterations to prevent infinite loops. Default: `50`

**EARLY_STOP_CONFIDENCE**: Confidence threshold for early stopping. If the best thought exceeds this confidence, the engine stops early. Default: `0.95`

**CONFIDENCE_THRESHOLD**: Minimum confidence required for acceptable output. If no thought meets this threshold after MAX_ITERATIONS, the best available thought is used. Default: `0.7`

#### Dashboard Configuration

```env
ENABLE_DASHBOARD=true
DASHBOARD_PORT=8000
DASHBOARD_HOST=0.0.0.0
```

**ENABLE_DASHBOARD**: Enable or disable the real-time cognitive telemetry dashboard. Default: `true`

**DASHBOARD_PORT**: Port for the dashboard WebSocket server. Default: `8000`

**DASHBOARD_HOST**: Host address for the dashboard server. Default: `0.0.0.0` (all interfaces)

#### Memory Configuration

```env
MEMORY_DB_PATH=cognitive_engine.db
MAX_MEMORY_SIZE=10000
MEMORY_RETENTION_DAYS=365
```

**MEMORY_DB_PATH**: Path to the SQLite database file for memory persistence. Default: `cognitive_engine.db`

**MAX_MEMORY_SIZE**: Maximum number of entries to store in memory. Default: `10000`

**MEMORY_RETENTION_DAYS**: Number of days to retain episodic memory entries. Default: `365`

#### Logging Configuration

```env
LOG_LEVEL=INFO
LOG_FILE=cognitive_engine.log
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_TO_CONSOLE=true
LOG_TO_FILE=true
```

**LOG_LEVEL**: Logging level. Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Default: `INFO`

**LOG_FILE**: Path to the log file. Default: `cognitive_engine.log`

**LOG_FORMAT**: Log message format. Default: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

**LOG_TO_CONSOLE**: Enable console logging. Default: `true`

**LOG_TO_FILE**: Enable file logging. Default: `true`

#### Learning Configuration

```env
ENABLE_LEARNING=true
LEARNING_INTERVAL=100
PATTERN_THRESHOLD=5
RULE_EFFECTIVENESS_THRESHOLD=0.7
```

**ENABLE_LEARNING**: Enable the learning system. Default: `true`

**LEARNING_INTERVAL**: Number of processing cycles between learning operations. Default: `100`

**PATTERN_THRESHOLD**: Minimum frequency for a pattern to be considered significant. Default: `5`

**RULE_EFFECTIVENESS_THRESHOLD**: Minimum effectiveness score for a rule to be retained. Default: `0.7`

#### Prompt Evolution Configuration

```env
ENABLE_PROMPT_EVOLUTION=false
PROMPT_EVOLUTION_INTERVAL=1000
MUTATION_RATE=0.1
PERFORMANCE_BASELINE_LOCK=true
```

**ENABLE_PROMPT_EVOLUTION**: Enable prompt evolution system. Default: `false` (experimental)

**PROMPT_EVOLUTION_INTERVAL**: Number of processing cycles between prompt evolution attempts. Default: `1000`

**MUTATION_RATE**: Maximum rate of prompt change per evolution cycle (0-1). Default: `0.1`

**PERFORMANCE_BASELINE_LOCK**: Prevent performance regression below original baseline. Default: `true`

#### Agent Configuration

```env
ENABLE_AGENT=true
AGENT_STEP_LIMIT=100
AGENT_GOAL_VALIDATION=true
AGENT_MEMORY_CONTROL=true
```

**ENABLE_AGENT**: Enable autonomous agent mode. Default: `true`

**AGENT_STEP_LIMIT**: Maximum number of steps an agent can take. Default: `100`

**AGENT_GOAL_VALIDATION**: Enable goal validation for safety. Default: `true`

**AGENT_MEMORY_CONTROL**: Enable memory control for agents. Default: `true`

## Configuration File

### .env File

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# LLM Provider
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_LLM_PROVIDER=openai

# Engine
MIN_ITERATIONS=3
MAX_ITERATIONS=50
EARLY_STOP_CONFIDENCE=0.95
CONFIDENCE_THRESHOLD=0.7

# Dashboard
ENABLE_DASHBOARD=true
DASHBOARD_PORT=8000

# Memory
MEMORY_DB_PATH=cognitive_engine.db
MAX_MEMORY_SIZE=10000

# Logging
LOG_LEVEL=INFO
LOG_FILE=cognitive_engine.log

# Learning
ENABLE_LEARNING=true
LEARNING_INTERVAL=100

# Prompt Evolution (experimental)
ENABLE_PROMPT_EVOLUTION=false

# Agent
ENABLE_AGENT=true
AGENT_STEP_LIMIT=100
```

### Programmatic Configuration

You can also configure the engine programmatically:

```python
from core.config import Config

config = Config(
    min_iterations=5,
    max_iterations=30,
    early_stop_confidence=0.9,
    confidence_threshold=0.75,
    enable_dashboard=True,
    dashboard_port=8080,
    default_llm_provider="anthropic"
)

from core.engine import CognitiveEngine
engine = CognitiveEngine(config)
```

## Configuration Scenarios

### Fast Response (Low Latency)

For scenarios where speed is more important than depth of reasoning:

```env
MIN_ITERATIONS=1
MAX_ITERATIONS=5
EARLY_STOP_CONFIDENCE=0.8
CONFIDENCE_THRESHOLD=0.6
ENABLE_LEARNING=false
ENABLE_DASHBOARD=false
```

### Deep Reasoning (High Quality)

For scenarios where quality is more important than speed:

```env
MIN_ITERATIONS=5
MAX_ITERATIONS=100
EARLY_STOP_CONFIDENCE=0.98
CONFIDENCE_THRESHOLD=0.8
ENABLE_LEARNING=true
ENABLE_DASHBOARD=true
```

### Development/Debugging

For development and debugging:

```env
LOG_LEVEL=DEBUG
LOG_TO_CONSOLE=true
LOG_TO_FILE=true
ENABLE_DASHBOARD=true
MIN_ITERATIONS=2
MAX_ITERATIONS=10
```

### Production

For production deployment:

```env
LOG_LEVEL=INFO
LOG_TO_CONSOLE=false
LOG_TO_FILE=true
ENABLE_DASHBOARD=false
MIN_ITERATIONS=3
MAX_ITERATIONS=50
ENABLE_PROMPT_EVOLUTION=false
```

### Research/Experimentation

For research and experimentation with prompt evolution:

```env
ENABLE_PROMPT_EVOLUTION=true
PROMPT_EVOLUTION_INTERVAL=500
MUTATION_RATE=0.2
PERFORMANCE_BASELINE_LOCK=true
ENABLE_LEARNING=true
ENABLE_DASHBOARD=true
LOG_LEVEL=DEBUG
```

## Configuration Validation

The system validates configuration at startup. Common validation errors:

### Missing API Keys

**Error**: `No LLM API key configured`

**Solution**: Set either `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`

### Invalid Iteration Settings

**Error**: `MIN_ITERATIONS must be less than MAX_ITERATIONS`

**Solution**: Ensure `MIN_ITERATIONS < MAX_ITERATIONS`

### Invalid Confidence Values

**Error**: `Confidence values must be between 0 and 1`

**Solution**: Ensure all confidence values are in range [0, 1]

### Port Already in Use

**Error**: `Dashboard port already in use`

**Solution**: Change `DASHBOARD_PORT` to a different port

## Advanced Configuration

### Custom LLM Provider

You can add custom LLM providers by extending the LLM client:

```python
from llm.client import LLMClient

class CustomLLMClient(LLMClient):
    def __init__(self):
        super().__init__(provider="custom")
        # Custom initialization
```

### Custom Memory Backend

You can use a different memory backend by implementing the memory interface:

```python
from core.memory import MemoryBackend

class CustomMemoryBackend(MemoryBackend):
    def store(self, event):
        # Custom storage logic
        pass
    
    def retrieve(self, query):
        # Custom retrieval logic
        pass
```

### Custom Scoring Functions

You can implement custom thought scoring:

```python
from utils.scoring import ThoughtScorer

class CustomScorer(ThoughtScorer):
    def score_thought(self, thought):
        # Custom scoring logic
        score = super().score_thought(thought)
        # Add custom factors
        return score
```

## Configuration Best Practices

1. **Security**: Never commit `.env` files with real API keys to version control
2. **Environment-Specific**: Use different configurations for development, staging, and production
3. **Documentation**: Document custom configurations for your team
4. **Validation**: Test configuration changes in a development environment first
5. **Monitoring**: Monitor the impact of configuration changes on system performance
6. **Backups**: Backup configuration files and database before major changes
7. **Version Control**: Keep `.env.example` in version control with placeholder values

## Troubleshooting Configuration Issues

### Configuration Not Loading

If configuration variables aren't being loaded:

1. Check that `.env` file exists in project root
2. Verify variable names are correct (no typos)
3. Ensure no extra spaces around `=`
4. Check file encoding (should be UTF-8)
5. Verify python-dotenv is installed

### Dashboard Not Starting

If the dashboard won't start:

1. Check that `ENABLE_DASHBOARD=true`
2. Verify `DASHBOARD_PORT` is not in use
3. Check firewall settings
4. Verify FastAPI and Uvicorn are installed
5. Check logs for specific error messages

### Memory Database Issues

If memory database has issues:

1. Check `MEMORY_DB_PATH` is writable
2. Verify SQLite is installed
3. Check disk space
4. Try deleting the database file and letting it recreate
5. Check file permissions

### LLM API Errors

If LLM API calls fail:

1. Verify API keys are correct
2. Check API quota/limits
3. Verify internet connectivity
4. Check API service status
5. Try switching to alternate provider

## Configuration Migration

When upgrading versions, configuration may change:

1. Check release notes for configuration changes
2. Backup current `.env` file
3. Update `.env.example` with new variables
4. Test new configuration in development
5. Deploy to production after validation

## Support

For configuration issues:
- Check logs in `cognitive_engine.log` for detailed error information
- Review this documentation for common issues
- Contact: autobotsolution@gmail.com
