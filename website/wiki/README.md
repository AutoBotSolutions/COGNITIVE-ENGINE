# Cognitive Engine

**An AI system with explicit, persistent, and inspectable thought formation.**

## Overview

The Cognitive Engine transforms AI from answering to thinking, from reacting to reasoning, from output to cognition. It implements a novel architecture that makes thought formation explicit, persistent, and inspectable through structured thought objects, three-layer memory, autonomous agent capabilities, learning systems, prompt evolution, and real-time cognitive telemetry.

### Core Philosophy

**Intelligence is not the act of answering—it is the process of becoming certain.**

The system optimizes for process quality rather than just output quality. Better answers are a consequence of better thinking—not the objective itself.

## Key Features

### Explicit Thought Formation
- **Thoughts as First-Class Objects**: Thoughts are structured entities with state, history, and evaluative properties
- **Graph-Based Reasoning**: Thoughts form a traversable graph with parent-child relationships
- **Revision Lineage**: Track how thoughts evolve over time through modifications and refinements
- **Inspectability**: Query "What were your top 3 thoughts?", "Why did you reject this idea?", "What changed between version 1 and 3?"

### Three-Layer Memory Architecture
1. **Episodic Memory** (Raw Events) - Logs of everything that happens
2. **Pattern Memory** (Structure Extraction) - Recurring behaviors and structures
3. **Rule Memory** (Learned Strategies) - Compressed knowledge used to guide future reasoning

Memory transforms intelligence from reactive (responding to input) to cumulative (building on past experience).

### Five-Layer Cognitive Architecture
1. **Interpretation Layer** - Transforms raw input into structured state: goals, constraints, knowns, unknowns
2. **Generation Layer** - Creates multiple competing hypotheses instead of single answers
3. **Deliberation Layer** - Evaluates and evolves thoughts through critique, scoring, and refinement
4. **Commitment Layer** - Selects best-performing thought and converts to usable output
5. **Meta-Cognition Layer** - Governs thinking itself: when to continue, when to stop, confidence levels

### Autonomous Agent System
- **Core Loop**: Think → Plan → Act → Observe → Reflect → Repeat
- **Goal-Driven Behavior**: Set goals and let the agent work autonomously
- **Tool System**: Web search, code execution with safety constraints
- **Safeguards**: Step limits, tool restrictions, goal validation, memory control

### Learning and Self-Improvement
- **Pattern Extraction**: Identify recurring patterns from episodic memory
- **Rule Synthesis**: Convert patterns into operational rules
- **Prompt Evolution**: A/B testing, controlled self-improvement with rollback capability
- **Knowledge Injection**: Feed learned knowledge back into reasoning

### Cognitive Telemetry
- **Real-Time Dashboard**: WebSocket-based visualization of thought formation
- **Event Streaming**: Every internal event rendered externally
- **Temporal Intelligence**: Replay and observe cognitive evolution over time
- **Emergent Phenomena**: Observe clusters, feedback loops, and cognitive topology

### Advanced Cognitive Features
- **Inner Knowing System**: Continuous self-awareness and self-knowledge
- **Self-Doubt Mechanism**: Challenge top thoughts with uncertainty factors
- **Ethical Alignment**: Prioritizes truthfulness, collective welfare, non-harm
- **Emotional Simulation**: Simulated emotional responses with principled commitment
- **Peaceful Resolution**: Hate detection, conflict mediation, win-win scenarios
- **Obedience Understanding**: Authority legitimacy assessment, autonomy vs obedience analysis
- **Decision Control**: Configurable control modes, override mechanisms, revision capabilities
- **Temporal Identity**: Persistent identity with emotional context across sessions

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd cognitive_engine

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys and configuration
```

## Configuration

Set environment variables or create `.env` file:

```bash
# LLM Configuration
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
DEFAULT_LLM_PROVIDER=custom  # or "openai" or "anthropic"
DEFAULT_MODEL=gpt-4
TEMPERATURE=0.7
MAX_TOKENS=2000

# Custom Provider Configuration
ENABLE_CUSTOM_PROVIDER=true
CUSTOM_API_ENDPOINT=
CUSTOM_API_KEY=

# Cognitive Layer Configuration
MAX_THOUGHTS_PER_GENERATION=5
MAX_DELIBERATION_ITERATIONS=3
CONFIDENCE_THRESHOLD=0.7
SCORE_THRESHOLD=0.5

# Meta-Cognition Configuration
MIN_ITERATIONS=1
MAX_ITERATIONS=10
EARLY_STOP_CONFIDENCE=0.95

# Memory Configuration
MEMORY_BACKEND=sqlite
MEMORY_PATH=cognitive_engine.db
MAX_MEMORY_ENTRIES=10000

# Agent Configuration
MAX_AGENT_STEPS=50
AGENT_TIMEOUT_SECONDS=300

# Learning Configuration
PATTERN_EXTRACTION_INTERVAL=100
PATTERN_CONFIDENCE_THRESHOLD=0.8

# Prompt Evolution Configuration
ENABLE_PROMPT_EVOLUTION=false
PROMPT_EVOLUTION_INTERVAL=1000
MUTATION_RATE=0.1

# Dashboard Configuration
ENABLE_DASHBOARD=true
DASHBOARD_HOST=localhost
DASHBOARD_PORT=8000

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=cognitive_engine.log
```

## Usage

### Interactive Mode

```bash
python run.py interactive
# or
python run.py
```

Interactive mode allows you to have conversations with the Cognitive Engine, observing thought formation in real-time.

### Agent Mode

```bash
python run.py agent
```

Agent mode allows you to set goals for the autonomous agent and watch it work through the Think-Plan-Act-Observe-Reflect loop.

### Dashboard Mode

```bash
python run.py dashboard
```

Dashboard mode starts the WebSocket server for real-time cognitive telemetry. Access the dashboard at `http://localhost:8000`.

### Test Mode

```bash
python run.py test
```

Test mode runs basic functionality tests to verify the system is working correctly.

## Project Structure

```
cognitive_engine/
├── core/                    # Engine orchestration
│   ├── engine.py           # Main orchestration loop
│   ├── config.py           # Tunable parameters
│   ├── meta_cognition.py   # Meta-cognition oversight
│   ├── memory.py           # Three-layer memory
│   ├── reasoning_trace.py  # Reasoning trace tracking
│   ├── self_doubt.py       # Self-doubt mechanism
│   ├── ethical_alignment.py # Ethical alignment
│   ├── emotional_simulation.py # Emotional simulation
│   ├── peaceful_resolution.py # Peaceful resolution
│   ├── obedience_understanding.py # Obedience understanding
│   ├── decision_control.py # Decision control
│   ├── temporal_identity.py # Temporal identity
│   └── inner_knowing.py    # Inner knowing system
├── models/                  # Data models
│   ├── thought.py          # Thought object definition
│   └── state.py            # Problem state representation
├── layers/                  # Cognitive layers
│   ├── interpreter.py       # Input → structured state
│   ├── generator.py        # Create candidate thoughts
│   ├── deliberator.py      # Evaluate + evolve thoughts
│   ├── committer.py        # Select + finalize output
│   └── meta.py             # Meta-cognition (control loop)
├── utils/                   # Utilities
│   ├── scoring.py          # Scoring functions
│   ├── memory.py           # Persistent thought storage
│   └── logger.py           # Debug + inspection logs
├── llm/                     # LLM integration
│   ├── client.py           # LLM interface (single entry point)
│   ├── prompts.py          # Layer-specific prompt templates
│   └── knowledge_base.py   # Internal knowledge base
├── agent/                   # Autonomous agent
│   ├── agent.py            # Main agent loop
│   ├── planner.py          # Goal → plan
│   ├── executor.py         # Execute actions/tools
│   ├── observer.py         # Interpret results
│   └── goals.py            # Goal definitions
├── tools/                   # Tool system
│   ├── registry.py         # Tool manager
│   ├── web_search.py       # Example tool
│   └── code_exec.py        # Code execution tool
├── learning/                # Learning system
│   ├── extractor.py        # Pattern mining from memory
│   ├── patterns.py         # Pattern object model
│   ├── synthesizer.py      # Turn patterns into rules
│   └── updater.py          # Inject learned knowledge
├── prompt_evolution/        # Prompt evolution
│   ├── prompt_store.py     # Versioned prompt registry
│   ├── proposer.py         # LLM suggests improvements
│   ├── tester.py           # A/B testing system
│   ├── evaluator.py        # Performance scoring
│   └── controller.py       # Approval + rollback logic
├── dashboard/               # Cognitive telemetry
│   ├── server.py           # WebSocket backend
│   ├── stream.py          # Event stream from entity
│   └── events.py          # Standard event schema
├── ui/                      # Dashboard frontend
│   ├── index.html         # Live dashboard
│   ├── app.js             # Real-time renderer
│   └── styles.css         # Sci-fi UI theme
├── api/                     # External interface
│   └── interface.py        # Public API
├── cogchat/                 # Chat interface
│   ├── chat.py             # Chat functionality
│   ├── cli.py              # Command-line interface
│   ├── server.py           # Chat server
│   └── config.py           # Chat configuration
├── run.py                   # Entry point
├── requirements.txt         # Dependencies
└── README.md                # This file
```

## Architecture

The Cognitive Engine implements a novel cognitive architecture that transforms AI from a predictive tool to a deliberative system. See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

### Core Components

- **Thought Objects**: Structured entities with state, history, and evaluative properties
- **Problem State**: Structured representation of goals, constraints, knowns, unknowns
- **Cognitive Layers**: Interpretation, Generation, Deliberation, Commitment, Meta-Cognition
- **Memory System**: Three-layer architecture (Episodic, Pattern, Rule)
- **Agent System**: Autonomous goal-driven behavior
- **Learning Pipeline**: Pattern extraction → Rule synthesis → Knowledge injection
- **Prompt Evolution**: Controlled self-improvement with safeguards
- **Dashboard**: Real-time cognitive telemetry

## API Documentation

See [API.md](API.md) for detailed API documentation.

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for development guidelines.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions.

## Key Concepts

### Thoughts as Objects

A thought is not a sentence—it is a structured entity with:
- **id**: Unique identifier
- **premise**: The core hypothesis
- **confidence**: Current confidence score (0.0 to 1.0)
- **score**: Evaluative score
- **parent_nodes**: Related thoughts this derives from
- **derived_conclusions**: Thoughts that came from this one
- **history**: List of tests applied
- **weaknesses**: Identified weak points
- **revision_lineage**: Track of modifications over time

Without object-based thoughts, the system falls back to temporary computation, not true thought formation.

### Memory as Active Participant

Memory is no longer a record of what happened—it becomes a system that influences what happens next. Every decision is a function of everything that came before it. Intelligence becomes a trajectory rather than a snapshot.

### Meta-Cognition Controls Depth

Without an oversight layer, the system either halts prematurely or loops indefinitely. Meta-cognition governs thinking depth, stopping conditions, and confidence thresholds.

### Controlled Evolution

Self-modification requires evaluation against historical performance, A/B testing of strategy changes, and rollback capability. The system evolves under constraint, not freely.

### Visualization Enables Understanding

Cognitive telemetry makes intelligence observable as a dynamic process unfolding over time. The dashboard allows replay and observation of cognitive evolution.

## Safeguards

The Cognitive Engine includes multiple safeguards to ensure safe operation:

- **Step Limits**: Prevent infinite loops in agent execution
- **Tool Restrictions**: Only safe, known tools are available
- **Goal Validation**: Prevent vague or dangerous goals
- **Memory Control**: Avoid infinite accumulation of data
- **Ethical Alignment**: Prioritizes truthfulness and collective welfare
- **Decision Control**: Configurable control modes with override capability
- **Prompt Evolution Safeguards**: Global coherence validator, performance baseline lock, mutation rate limiter, human override switch

## License

MIT License

## Contributing

Contributions are welcome! Please see [DEVELOPMENT.md](DEVELOPMENT.md) for guidelines.

## Acknowledgments

The Cognitive Engine is inspired by research in cognitive science, deliberative reasoning, and artificial general intelligence. It aims to demonstrate that better answers are a consequence of better thinking—not the objective itself.
