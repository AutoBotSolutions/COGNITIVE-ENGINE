# Cognitive Engine

An AI system with explicit, persistent, and inspectable thought formation.

## Overview

The Cognitive Engine transforms AI from answering to thinking, from reacting to reasoning, from output to cognition. It implements a 4-part cognitive architecture with thought objects, three-layer memory, autonomous agent capabilities, learning systems, prompt evolution, and real-time cognitive telemetry.

## Architecture

### Core Components

- **Models**: Thought and ProblemState objects for structured cognition
- **Layers**: Interpreter, Generator, Deliberator, Committer, Meta-Cognition
- **Utilities**: Scoring, Memory (SQLite), Logging
- **LLM Integration**: OpenAI/Anthropic client with layer-specific prompts

### Advanced Features

- **Autonomous Agent**: Think → Plan → Act → Observe → Reflect loop
- **Tools**: Web search, code execution with safety constraints
- **Learning**: Pattern extraction, rule synthesis, knowledge injection
- **Prompt Evolution**: A/B testing, controlled self-improvement with rollback
- **Dashboard**: Real-time WebSocket cognitive telemetry

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Interactive Mode

```bash
python run.py
# or
python run.py interactive
```

### Agent Mode

```bash
python run.py agent
```

### Dashboard Mode

```bash
python run.py dashboard
```

### Test Mode

```bash
python run.py test
```

## Configuration

Set environment variables or create `.env` file:

```
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
DEFAULT_LLM_PROVIDER=openai
ENABLE_DASHBOARD=true
```

## Project Structure

```
cognitive_engine/
├── core/           # Engine orchestration
├── models/         # Thought and state objects
├── layers/         # Cognitive layers
├── utils/          # Scoring, memory, logging
├── llm/            # LLM client and prompts
├── agent/          # Autonomous agent
├── tools/          # Tool registry
├── learning/       # Pattern extraction and learning
├── prompt_evolution/  # Prompt optimization
├── dashboard/      # WebSocket telemetry
├── ui/             # Dashboard frontend
└── run.py          # Entry point
```

## Key Features

- **Explicit Thought Formation**: Thoughts are structured objects with state, history, and evaluative properties
- **Three-Layer Memory**: Episodic (raw events), Pattern (structure extraction), Rule (learned strategies)
- **Meta-Cognition**: Oversight layer governing thinking depth and stopping conditions
- **Controlled Evolution**: Self-modification with A/B testing, evaluation, and rollback capability
- **Cognitive Telemetry**: Real-time dashboard observing thought formation
- **Safeguards**: Step limits, tool restrictions, goal validation, memory control

## License

MIT License
