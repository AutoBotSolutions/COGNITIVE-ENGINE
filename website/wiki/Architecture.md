# Cognitive Engine Architecture

This document describes the overall architecture of the Cognitive Engine system.

## High-Level Architecture

The Cognitive Engine implements a 5-layer cognitive architecture with supporting systems for memory, learning, autonomy, and visualization.

```
┌─────────────────────────────────────────────────────────────┐
│                     Meta-Cognition Layer                     │
│  (Oversight, iteration control, confidence management)      │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌────────▼────────┐
│  Interpreter   │  │    Generator    │  │  Deliberator    │
│  (Input →      │  │  (Create        │  │  (Evaluate &    │
│   Structured)   │  │   Thoughts)     │  │   Evolve)       │
└────────────────┘  └─────────────────┘  └─────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                     ┌────────▼────────┐
                     │   Committer     │
                     │  (Finalize &    │
                     │   Express)      │
                     └─────────────────┘
```

## Core Cognitive Layers

### 1. Interpreter Layer

**Purpose**: Transform raw input into structured problem state

**Responsibilities**:
- Parse and understand user input
- Extract goals, constraints, knowns, and unknowns
- Define the problem space clearly
- Create structured ProblemState object

**File**: `layers/interpreter.py`

**Output**: Structured ProblemState with:
- Goals: What needs to be achieved
- Constraints: Limitations and requirements
- Knowns: Facts and information provided
- Unknowns: Gaps in knowledge
- Context: Relevant background information

### 2. Generator Layer

**Purpose**: Create multiple competing thought candidates

**Responsibilities**:
- Generate diverse hypotheses
- Break the "single-shot answer" limitation
- Create thought objects with initial confidence
- Ensure variety in thought generation

**File**: `layers/generator.py`

**Output**: Multiple Thought objects with:
- Unique premise
- Initial confidence score
- Parent relationships
- Metadata for tracking

### 3. Deliberator Layer

**Purpose**: Evaluate, test, and evolve thoughts

**Responsibilities**:
- Internal simulation of thought outcomes
- Stress testing of hypotheses
- Comparative scoring between thoughts
- Mutation and refinement of weak thoughts
- Identification of weaknesses

**File**: `layers/deliberator.py`

**Processes**:
- Internal Simulation: Test thought validity
- Stress Testing: Challenge assumptions
- Comparative Scoring: Rank thoughts by quality
- Mutation: Improve weak thoughts
- Convergence: Merge similar thoughts

### 4. Committer Layer

**Purpose**: Select best thought and express output

**Responsibilities**:
- Select highest-scoring thought
- Convert to natural language output
- Optionally expose reasoning trace
- Store result in memory

**File**: `layers/committer.py`

**Output**:
- Final answer/expression
- Reasoning trace (if enabled)
- Memory storage of result

### 5. Meta-Cognition Layer

**Purpose**: Govern the thinking process itself

**Responsibilities**:
- Determine when to continue thinking
- Decide when to stop (confidence thresholds)
- Control iteration depth
- Prevent premature halting or infinite loops
- Monitor overall cognitive health

**File**: `layers/meta.py`

**Controls**:
- Minimum iterations (prevent early exit)
- Maximum iterations (prevent infinite loops)
- Early stop confidence (stop when confident)
- Confidence threshold (quality gate)

## Supporting Systems

### Memory System

**Architecture**: Three-layer memory hierarchy

#### Episodic Memory
- Stores raw events and interactions
- Complete logs of everything that happens
- Foundation for higher-level extraction
- File: `core/memory.py`

#### Pattern Memory
- Recurring behaviors and structures
- Compressed representations of patterns
- Enables functional self-awareness
- File: `learning/extractor.py`, `learning/patterns.py`

#### Rule Memory
- Learned strategies and operational rules
- Directly modifies reasoning behavior
- Patterns transformed into actionable rules
- File: `learning/synthesizer.py`, `learning/updater.py`

### Thought Object Model

**Structure**:
```python
Thought:
  - id: Unique identifier
  - premise: Core hypothesis
  - confidence: Current confidence score
  - parent_nodes: Related thoughts
  - derived_conclusions: Child thoughts
  - score: Evaluative score
  - history: Tests applied
  - weaknesses: Identified weak points
  - revision_lineage: Modification tracking
```

**File**: `models/thought.py`

**Key Properties**:
- Persistence: Survives beyond single processing
- Inspectability: Can query history and evolution
- Revisability: Can be modified or discarded
- Object-based: Enables graph traversal

### Autonomous Agent System

**Core Loop**: Think → Plan → Act → Observe → Reflect

**Components**:
- **Agent**: Main orchestration loop (`agent/agent.py`)
- **Planner**: Goal → plan conversion (`agent/planner.py`)
- **Executor**: Execute actions/tools (`agent/executor.py`)
- **Observer**: Interpret results (`agent/observer.py`)
- **Goals**: Goal definitions (`agent/goals.py`)

**Tool System**:
- Registry: Tool manager (`tools/registry.py`)
- Web Search: Information retrieval (`tools/web_search.py`)
- Code Execution: Safe code running (`tools/code_exec.py`)

**Safeguards**:
- Step limits (prevent infinite loops)
- Tool restrictions (only safe tools)
- Goal validation (prevent dangerous goals)
- Memory control (prevent accumulation)

### Learning System

**Pipeline**: Record → Extract → Synthesize → Inject

**Components**:
- **Extractor**: Pattern mining from memory (`learning/extractor.py`)
- **Patterns**: Pattern object model (`learning/patterns.py`)
- **Synthesizer**: Turn patterns into rules (`learning/synthesizer.py`)
- **Updater**: Inject learned knowledge (`learning/updater.py`)

**Process**:
1. Record experiences in episodic memory
2. Extract recurring patterns
3. Convert patterns into reusable rules
4. Feed rules back into reasoning

### Prompt Evolution System

**Purpose**: Controlled self-improvement through prompt optimization

**Components**:
- **Prompt Store**: Versioned prompt registry (`prompt_evolution/prompt_store.py`)
- **Proposer**: LLM suggests improvements (`prompt_evolution/proposer.py`)
- **Tester**: A/B testing system (`prompt_evolution/tester.py`)
- **Evaluator**: Performance scoring (`prompt_evolution/evaluator.py`)
- **Controller**: Approval and rollback (`prompt_evolution/controller.py`)

**Safeguards**:
- Evaluation against historical performance
- Controlled A/B testing
- Rollback capability
- Global coherence validation
- Performance baseline lock
- Mutation rate limiter
- Human override switch

### Dashboard / Cognitive Telemetry

**Purpose**: Real-time observation of thought formation

**Components**:
- **Server**: WebSocket backend (`dashboard/server.py`)
- **Stream**: Event stream from entity (`dashboard/stream.py`)
- **Events**: Standard event schema (`dashboard/events.py`)
- **UI**: Frontend visualization (`ui/`)

**Visualized**:
- Thought generation (visible nodes)
- Memory updates (evolving archives)
- Strategy shifts (parameter drift)
- Deliberation scoring
- Memory growth
- Prompt evolution
- Agent actions over time

**Emergent Phenomena**:
- Thought clusters forming over time
- Dominant reasoning paths
- Dense vs sparse reasoning regions
- Feedback loops
- Cognitive topology

### LLM Integration

**Architecture**: Single entry point with layer-specific prompts

**Components**:
- **Client**: LLM interface (`llm/client.py`)
- **Prompts**: Layer-specific templates (`llm/prompts.py`)
- **Knowledge Base**: Context management (`llm/knowledge_base.py`)

**Specialization**:
- Generator: Creative thought generation
- Deliberator: Critical evaluation
- Simulation: Outcome prediction
- Meta: Process oversight

## Data Flow

```
User Input
    ↓
Interpreter → ProblemState
    ↓
Generator → Multiple Thoughts
    ↓
Deliberator → Evolved/Scored Thoughts
    ↓
Meta-Cognition → Continue/Stop Decision
    ↓ (if continue)
Deliberator → Further Evolution
    ↓ (if stop)
Committer → Final Output
    ↓
Memory Storage (All Three Layers)
    ↓
Learning System → Pattern Extraction
    ↓
Rule Memory → Strategy Updates
```

## Component Interactions

### Engine Orchestration

**File**: `core/engine.py`

The CognitiveEngine class coordinates all layers and systems:
- Initializes all components
- Manages the main processing loop
- Handles iteration control
- Integrates with dashboard
- Manages temporal snapshots

### Configuration Management

**File**: `core/config.py`

Centralized configuration for:
- LLM provider settings
- Iteration limits
- Confidence thresholds
- Dashboard settings
- Memory configuration
- Logging configuration

### Reasoning Traces

**File**: `core/reasoning_trace.py`

Tracks the complete reasoning process:
- Event logging
- Thought evolution
- Decision points
- Temporal replay capability

## Advanced Cognitive Features

### Inner Knowing System

**File**: `core/inner_knowing.py`

Continuous self-awareness and self-modeling:
- Capability tracking
- Self-knowledge base
- Identity formation
- Continuous self-reflection

### Self-Doubt System

**File**: `core/self_doubt.py**

Meta-cognitive uncertainty handling:
- Doubt level assessment
- Confidence calibration
- Error detection
- Self-questioning

### Ethical Alignment

**File**: `core/ethical_alignment.py`

Moral reasoning and value alignment:
- Ethical constraint checking
- Value conflict detection
- Welfare optimization
- Truthfulness enforcement

### Emotional Simulation

**File**: `core/emotional_simulation.py`

Emotional context and attachment:
- Emotional state modeling
- Stakeholder attachment
- Empathy simulation
- Affective memory

### Decision Control

**File**: `core/decision_control.py`

Autonomy and authority management:
- Decision override capability
- Authority legitimacy assessment
- Autonomy vs obedience analysis
- Peaceful conflict resolution

### Temporal Identity

**File**: `core/temporal_identity.py`

Long-term identity continuity:
- Identity persistence over time
- State continuity
- Memory with emotional context
- Identity evolution

## Technology Stack

### Core
- Python 3.9+
- asyncio for async operations
- Pydantic for data validation

### LLM Integration
- OpenAI API
- Anthropic API
- Custom prompt templates

### Data Storage
- SQLite for memory
- JSON for configuration
- NPZ for neural weights

### Web/Dashboard
- FastAPI for server
- WebSockets for real-time updates
- Jinja2 for templating

### Utilities
- python-dateutil for datetime
- pytz for timezone handling
- colorlog for logging
- orjson for JSON handling

## Design Principles

1. **Explicit Thought**: Thoughts are first-class objects
2. **Persistence**: All cognitive state persists beyond single operations
3. **Inspectability**: Every cognitive process is observable
4. **Revisability**: Thoughts and strategies can be revised
5. **Safeguards**: Multiple layers of protection against failure
6. **Evolution**: System improves over time through learning
7. **Transparency**: Dashboard provides real-time visibility
8. **Modularity**: Clean separation of concerns between components
