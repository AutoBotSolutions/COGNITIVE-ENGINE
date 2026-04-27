# Core Modules Documentation

This document provides detailed information about each major module in the Cognitive Engine.

## Table of Contents

- [Core Engine](#core-engine)
- [Cognitive Layers](#cognitive-layers)
- [Models](#models)
- [Memory System](#memory-system)
- [Autonomous Agent](#autonomous-agent)
- [Learning System](#learning-system)
- [Prompt Evolution](#prompt-evolution)
- [Dashboard](#dashboard)
- [LLM Integration](#llm-integration)
- [Tools](#tools)
- [Utilities](#utilities)
- [Advanced Cognitive Features](#advanced-cognitive-features)

---

## Core Engine

### engine.py

**Location**: `core/engine.py`

**Purpose**: Main orchestration loop that coordinates all cognitive layers and systems.

**Key Classes**:
- `CognitiveEngine`: Main engine class

**Responsibilities**:
- Initialize all cognitive layers
- Manage the main processing loop
- Coordinate iteration control via meta-cognition
- Integrate with dashboard for telemetry
- Manage temporal snapshots for replay
- Orchestrate memory and learning systems

**Key Methods**:
- `process(input: str) -> ProcessResult`: Main entry point for processing queries
- `initialize_layers()`: Set up all cognitive layers
- `run_cognitive_loop()`: Execute the thought formation loop
- `generate_thoughts()`: Create candidate thoughts via generator layer
- `deliberate_thoughts()`: Evaluate and evolve thoughts via deliberator
- `commit_thought()`: Finalize best thought via committer
- `check_meta_cognition()`: Consult meta-cognition for continuation decision

**Integration Points**:
- Layers: Interpreter, Generator, Deliberator, Committer, Meta
- Memory: ThreeLayerMemory for persistence
- Dashboard: Dashboard streamer for telemetry
- Learning: Pattern extraction and rule synthesis
- Inner Knowing: Continuous self-awareness system

### config.py

**Location**: `core/config.py`

**Purpose**: Centralized configuration management for the entire system.

**Key Settings**:
- `min_iterations`: Minimum cognitive iterations (default: 3)
- `max_iterations`: Maximum cognitive iterations (default: 50)
- `early_stop_confidence`: Confidence threshold for early stopping (default: 0.95)
- `confidence_threshold`: Minimum confidence for acceptable output (default: 0.7)
- `enable_dashboard`: Enable real-time telemetry (default: true)
- `dashboard_port`: Dashboard WebSocket port (default: 8000)
- `default_llm_provider`: Default LLM provider (openai or anthropic)
- `memory_db_path`: SQLite database path for memory
- `max_memory_size`: Maximum memory entries

---

## Cognitive Layers

### interpreter.py

**Location**: `layers/interpreter.py`

**Purpose**: Transform raw input into structured ProblemState.

**Key Classes**:
- `Interpreter`: Input interpretation layer

**Responsibilities**:
- Parse and understand user input
- Extract goals, constraints, knowns, unknowns
- Define problem space clearly
- Create structured ProblemState object

**Input**: Raw string input from user
**Output**: ProblemState object with structured problem definition

**Methods**:
- `interpret(input: str) -> ProblemState`: Main interpretation method
- `extract_goals(text: str) -> List[str]`: Identify goals
- `extract_constraints(text: str) -> List[str]`: Identify constraints
- `extract_knowns(text: str) -> List[str]`: Identify known facts
- `extract_unknowns(text: str) -> List[str]`: Identify gaps

### generator.py

**Location**: `layers/generator.py`

**Purpose**: Create multiple competing thought candidates.

**Key Classes**:
- `Generator`: Thought generation layer

**Responsibilities**:
- Generate diverse hypotheses
- Create thought objects with initial confidence
- Ensure variety in thought generation
- Break "single-shot answer" limitation

**Input**: ProblemState from interpreter
**Output**: List of Thought objects

**Methods**:
- `generate(problem_state: ProblemState) -> List[Thought]`: Generate thoughts
- `create_thought(premise: str, confidence: float) -> Thought`: Create single thought
- `ensure_diversity(thoughts: List[Thought]) -> List[Thought]`: Ensure variety

### deliberator.py

**Location**: `layers/deliberator.py`

**Purpose**: Evaluate, test, and evolve thoughts.

**Key Classes**:
- `Deliberator`: Thought deliberation layer

**Responsibilities**:
- Internal simulation of thought outcomes
- Stress testing of hypotheses
- Comparative scoring between thoughts
- Mutation and refinement of weak thoughts
- Identification of weaknesses

**Input**: List of Thoughts from generator
**Output**: Evolved and scored list of Thoughts

**Methods**:
- `deliberate(thoughts: List[Thought]) -> List[Thought]`: Main deliberation
- `internal_simulation(thought: Thought) -> Thought`: Test thought validity
- `stress_test(thought: Thought) -> List[str]`: Identify weaknesses
- `comparative_scoring(thoughts: List[Thought]) -> None`: Rank thoughts
- `mutate(thought: Thought) -> Thought`: Improve weak thought
- `converge(thoughts: List[Thought]) -> List[Thought]`: Merge similar thoughts

### committer.py

**Location**: `layers/committer.py`

**Purpose**: Select best thought and express output.

**Key Classes**:
- `Committer`: Thought commitment layer

**Responsibilities**:
- Select highest-scoring thought
- Convert to natural language output
- Optionally expose reasoning trace
- Store result in memory

**Input**: Evolved list of Thoughts
**Output**: ProcessResult with final answer

**Methods**:
- `commit(thoughts: List[Thought]) -> ProcessResult`: Commit to best thought
- `select_best(thoughts: List[Thought]) -> Thought`: Select highest-scoring
- `format_output(thought: Thought) -> str`: Convert to natural language
- `create_trace(thoughts: List[Thought]) -> str`: Create reasoning trace
- `store_in_memory(result: ProcessResult) -> None`: Persist result

### meta.py

**Location**: `layers/meta.py`

**Purpose**: Govern the thinking process itself.

**Key Classes**:
- `MetaCognition`: Meta-cognitive oversight layer

**Responsibilities**:
- Determine when to continue thinking
- Decide when to stop based on confidence
- Control iteration depth
- Prevent premature halting or infinite loops
- Monitor overall cognitive health

**Input**: Current iteration count, thought scores, confidence levels
**Output**: Decision to continue or stop

**Methods**:
- `should_continue(iteration: int, thoughts: List[Thought]) -> bool`: Continuation decision
- `check_min_iterations(iteration: int) -> bool`: Ensure minimum iterations
- `check_max_iterations(iteration: int) -> bool`: Prevent infinite loops
- `check_early_stop_confidence(thoughts: List[Thought]) -> bool`: Early stop if confident
- `check_confidence_threshold(thoughts: List[Thought]) -> bool`: Quality gate

---

## Models

### thought.py

**Location**: `models/thought.py`

**Purpose**: Define the Thought object structure and ThoughtGraph.

**Key Classes**:
- `Thought`: First-class thought object
- `ThoughtGraph`: Graph of interconnected thoughts

**Thought Structure**:
```python
class Thought:
    id: str                          # Unique identifier
    premise: str                      # Core hypothesis
    confidence: float                # Current confidence (0-1)
    parent_nodes: List[str]          # Related thoughts this derives from
    derived_conclusions: List[str]   # Thoughts that came from this
    score: float                     # Evaluative score
    history: List[Dict]              # Tests applied
    weaknesses: List[str]            # Identified weak points
    revision_lineage: List[str]      # Track of modifications
    created_at: datetime             # Creation timestamp
    modified_at: datetime            # Last modification
```

**Key Methods**:
- `add_parent(thought_id: str)`: Add parent relationship
- `add_child(thought_id: str)`: Add child relationship
- `update_confidence(new_confidence: float)`: Update confidence score
- `add_weakness(weakness: str)`: Record identified weakness
- `record_test(test_result: Dict)`: Record test in history
- `revise(new_premise: str)`: Create revised version

**ThoughtGraph Methods**:
- `add_thought(thought: Thought)`: Add thought to graph
- `get_thought(thought_id: str) -> Thought`: Retrieve thought
- `get_related(thought_id: str) -> List[Thought]`: Get related thoughts
- `find_path(from_id: str, to_id: str) -> List[Thought]`: Find reasoning path

### state.py

**Location**: `models/state.py`

**Purpose**: Define ProblemState for structured problem representation.

**Key Classes**:
- `ProblemState`: Structured problem definition

**ProblemState Structure**:
```python
class ProblemState:
    goals: List[str]           # What needs to be achieved
    constraints: List[str]    # Limitations and requirements
    knowns: List[str]          # Facts and information provided
    unknowns: List[str]        # Gaps in knowledge
    context: str               # Relevant background information
    priority: str              # Priority level
    created_at: datetime       # Creation timestamp
```

---

## Memory System

### memory.py (Core)

**Location**: `core/memory.py`

**Purpose**: Three-layer memory system for persistence and learning.

**Key Classes**:
- `ThreeLayerMemory`: Main memory system
- `EpisodicMemory`: Raw event storage
- `PatternMemory`: Pattern extraction and storage
- `RuleMemory`: Learned strategy storage

**Episodic Memory**:
- Stores raw events and interactions
- Complete logs of everything that happens
- Foundation for higher-level extraction
- SQLite-backed for persistence

**Pattern Memory**:
- Recurring behaviors and structures
- Compressed representations of patterns
- Enables functional self-awareness
- Pattern object model with frequency tracking

**Rule Memory**:
- Learned strategies and operational rules
- Directly modifies reasoning behavior
- Patterns transformed into actionable rules
- Rule application and effectiveness tracking

**Key Methods**:
- `store_episodic(event: Dict)`: Store raw event
- `extract_patterns() -> List[Pattern]`: Extract recurring patterns
- `synthesize_rules(patterns: List[Pattern]) -> List[Rule]`: Create rules
- `apply_rules(state: ProblemState) -> ProblemState`: Apply learned rules
- `get_episodic_memory() -> List[Dict]`: Retrieve episodic memory
- `get_pattern_memory() -> List[Pattern]`: Retrieve pattern memory
- `get_rule_memory() -> List[Rule]`: Retrieve rule memory

### memory.py (Utils)

**Location**: `utils/memory.py`

**Purpose**: Memory utilities and helper functions.

**Responsibilities**:
- Memory serialization/deserialization
- Memory compression
- Memory indexing
- Memory search and retrieval

---

## Autonomous Agent

### agent.py

**Location**: `agent/agent.py`

**Purpose**: Main autonomous agent orchestration.

**Key Classes**:
- `Agent`: Autonomous agent implementation

**Core Loop**: Think → Plan → Act → Observe → Reflect

**Responsibilities**:
- Accept and validate goals
- Coordinate planner, executor, and observer
- Manage agent state and memory
- Handle tool execution
- Implement safeguards

**Key Methods**:
- `run(goal: str) -> AgentResult`: Execute agent with goal
- `think(goal: str) -> Plan`: Think about goal
- `plan(goal: str) -> Plan`: Create execution plan
- `act(plan: Plan) -> ActionResult`: Execute plan
- `observe(result: ActionResult) -> Observation`: Observe results
- `reflect(observation: Observation) -> Reflection`: Reflect and learn

### planner.py

**Location**: `agent/planner.py`

**Purpose**: Convert goals into actionable plans.

**Key Classes**:
- `Planner`: Goal-to-plan conversion

**Responsibilities**:
- Break down goals into steps
- Identify required tools
- Estimate resource requirements
- Create execution timeline
- Validate plan feasibility

**Methods**:
- `create_plan(goal: str) -> Plan`: Create execution plan
- `decompose_goal(goal: str) -> List[Step]`: Break down goal
- `identify_tools(steps: List[Step]) -> List[Tool]`: Select tools
- `estimate_resources(plan: Plan) -> ResourceEstimate`: Estimate needs
- `validate_plan(plan: Plan) -> bool`: Validate feasibility

### executor.py

**Location**: `agent/executor.py`

**Purpose**: Execute actions using available tools.

**Key Classes**:
- `Executor`: Action execution

**Responsibilities**:
- Execute plan steps
- Call appropriate tools
- Handle tool errors
- Track execution progress
- Manage resource usage

**Methods**:
- `execute(plan: Plan) -> ActionResult`: Execute plan
- `execute_step(step: Step) -> StepResult`: Execute single step
- `call_tool(tool: Tool, params: Dict) -> ToolResult`: Call tool
- `handle_error(error: Exception) -> ErrorResult`: Handle errors

### observer.py

**Location**: `agent/observer.py`

**Purpose**: Interpret and analyze execution results.

**Key Classes**:
- `Observer`: Result interpretation

**Responsibilities**:
- Analyze execution results
- Extract meaningful information
- Identify success/failure patterns
- Update agent state
- Feed into reflection

**Methods**:
- `observe(result: ActionResult) -> Observation`: Observe results
- `analyze_success(result: ActionResult) -> SuccessAnalysis`: Analyze success
- `analyze_failure(result: ActionResult) -> FailureAnalysis`: Analyze failure
- `extract_learning(observation: Observation) -> Learning`: Extract learning

### goals.py

**Location**: `agent/goals.py`

**Purpose**: Goal definitions and validation.

**Key Classes**:
- `Goal`: Goal definition
- `GoalValidator`: Goal validation

**Responsibilities**:
- Define goal structure
- Validate goal safety
- Check goal feasibility
- Prioritize multiple goals
- Track goal completion

**Methods**:
- `validate_goal(goal: str) -> ValidationResult`: Validate goal
- `check_safety(goal: str) -> bool`: Check if goal is safe
- `check_feasibility(goal: str) -> bool`: Check if goal is feasible
- `prioritize_goals(goals: List[Goal]) -> List[Goal]`: Prioritize

---

## Learning System

### extractor.py

**Location**: `learning/extractor.py`

**Purpose**: Extract patterns from episodic memory.

**Key Classes**:
- `PatternExtractor`: Pattern mining from memory

**Responsibilities**:
- Analyze episodic memory
- Identify recurring patterns
- Extract structural patterns
- Calculate pattern frequency
- Rank patterns by significance

**Methods**:
- `extract_patterns(memory: List[Dict]) -> List[Pattern]`: Extract patterns
- `analyze_frequency(events: List[Dict]) -> Dict[str, int]`: Analyze frequency
- `find_structures(events: List[Dict]) -> List[Structure]`: Find structures
- `rank_patterns(patterns: List[Pattern]) -> List[Pattern]`: Rank by significance

### patterns.py

**Location**: `learning/patterns.py`

**Purpose**: Pattern object model and management.

**Key Classes**:
- `Pattern`: Pattern representation
- `PatternManager`: Pattern management

**Pattern Structure**:
```python
class Pattern:
    id: str                    # Unique identifier
    description: str           # Pattern description
    frequency: int            # How often it occurs
    contexts: List[str]       # Contexts where it appears
    confidence: float          # Confidence in pattern validity
    related_patterns: List[str]  # Related patterns
    created_at: datetime      # Creation timestamp
```

### synthesizer.py

**Location**: `learning/synthesizer.py`

**Purpose**: Convert patterns into actionable rules.

**Key Classes**:
- `RuleSynthesizer`: Pattern to rule conversion

**Responsibilities**:
- Transform patterns into rules
- Define rule conditions
- Define rule actions
- Validate rule consistency
- Estimate rule effectiveness

**Methods**:
- `synthesize_rules(patterns: List[Pattern]) -> List[Rule]`: Create rules
- `define_conditions(pattern: Pattern) -> List[Condition]`: Define conditions
- `define_actions(pattern: Pattern) -> List[Action]`: Define actions
- `validate_rule(rule: Rule) -> bool`: Validate consistency

### updater.py

**Location**: `learning/updater.py`

**Purpose**: Inject learned knowledge into reasoning system.

**Key Classes**:
- `KnowledgeUpdater`: Knowledge injection

**Responsibilities**:
- Update rule memory
- Apply rules to current state
- Track rule effectiveness
- Remove ineffective rules
- Suggest rule modifications

**Methods**:
- `update_rules(rules: List[Rule])`: Update rule memory
- `apply_rule(rule: Rule, state: ProblemState) -> ProblemState`: Apply rule
- `track_effectiveness(rule: Rule, outcome: Dict)`: Track effectiveness
- `prune_ineffective_rules()`: Remove ineffective rules

---

## Prompt Evolution

### prompt_store.py

**Location**: `prompt_evolution/prompt_store.py`

**Purpose**: Versioned prompt registry and management.

**Key Classes**:
- `PromptStore`: Versioned prompt storage
- `PromptVersion`: Versioned prompt

**Responsibilities**:
- Store prompt versions
- Track prompt history
- Manage prompt metadata
- Enable rollback
- Version comparison

**Methods**:
- `store_prompt(prompt: str, version: str)`: Store prompt version
- `get_prompt(version: str) -> str`: Retrieve specific version
- `get_latest() -> str`: Get latest version
- `get_history() -> List[PromptVersion]`: Get version history
- `rollback(version: str)`: Rollback to version

### proposer.py

**Location**: `prompt_evolution/proposer.py`

**Purpose**: LLM suggests prompt improvements.

**Key Classes**:
- `PromptProposer`: Prompt improvement suggestions

**Responsibilities**:
- Analyze current prompts
- Suggest improvements
- Generate candidate prompts
- Estimate improvement potential
- Prioritize suggestions

**Methods**:
- `propose_improvements(prompt: str) -> List[str]`: Suggest improvements
- `analyze_prompt(prompt: str) -> PromptAnalysis`: Analyze prompt
- `generate_candidates(analysis: PromptAnalysis) -> List[str]`: Generate candidates
- `estimate_improvement(original: str, candidate: str) -> float`: Estimate improvement

### tester.py

**Location**: `prompt_evolution/tester.py`

**Purpose**: A/B testing system for prompts.

**Key Classes**:
- `PromptTester`: A/B testing

**Responsibilities**:
- Design A/B tests
- Execute test runs
- Collect performance data
- Statistical analysis
- Determine significance

**Methods**:
- `design_test(original: str, candidate: str) -> TestDesign`: Design test
- `run_test(test: TestDesign) -> TestResults`: Execute test
- `analyze_results(results: TestResults) -> TestAnalysis`: Analyze results
- `determine_significance(analysis: TestAnalysis) -> bool`: Determine significance

### evaluator.py

**Location**: `prompt_evolution/evaluator.py`

**Purpose**: Performance scoring for prompts.

**Key Classes**:
- `PromptEvaluator`: Performance evaluation

**Responsibilities**:
- Define evaluation metrics
- Score prompt performance
- Compare prompt versions
- Track historical performance
- Identify regressions

**Methods**:
- `evaluate(prompt: str, results: List[Dict]) -> float`: Evaluate prompt
- `compare(original: str, candidate: str) -> ComparisonResult`: Compare prompts
- `track_performance(prompt: str, score: float)`: Track over time
- `detect_regression(prompt: str) -> bool`: Detect performance regression

### controller.py

**Location**: `prompt_evolution/controller.py`

**Purpose**: Approval and rollback logic for prompt changes.

**Key Classes**:
- `PromptController`: Prompt change control

**Responsibilities**:
- Approve prompt changes
- Manage rollback capability
- Enforce safeguards
- Coordinate evolution process
- Human override interface

**Methods**:
- `approve_change(change: PromptChange) -> bool`: Approve change
- `rollback(version: str)`: Rollback to version
- `enforce_safeguards(change: PromptChange) -> bool`: Check safeguards
- `coordinate_evolution()`: Coordinate evolution process
- `human_override()`: Enable human intervention

---

## Dashboard

### server.py

**Location**: `dashboard/server.py`

**Purpose**: WebSocket backend for real-time telemetry.

**Key Classes**:
- `DashboardServer`: WebSocket server

**Responsibilities**:
- Handle WebSocket connections
- Broadcast cognitive events
- Manage client connections
- Handle client subscriptions
- Stream real-time data

**Methods**:
- `start_server()`: Start WebSocket server
- `broadcast_event(event: Event)`: Broadcast to all clients
- `handle_connection(websocket)`: Handle new connection
- `handle_subscription(subscription: Subscription)`: Handle subscription

### stream.py

**Location**: `dashboard/stream.py`

**Purpose**: Event stream from cognitive engine.

**Key Classes**:
- `DashboardStreamer`: Event streaming

**Responsibilities**:
- Stream cognitive events
- Format events for dashboard
- Filter events by type
- Manage event queue
- Handle event buffering

**Methods**:
- `stream_event(event: CognitiveEvent)`: Stream event
- `format_event(event: CognitiveEvent) -> DashboardEvent`: Format event
- `filter_events(filter: EventFilter)`: Filter events
- `manage_queue()`: Manage event queue

### events.py

**Location**: `dashboard/events.py`

**Purpose**: Standard event schema for dashboard.

**Key Classes**:
- `Event`: Base event class
- `ThoughtEvent`: Thought generation event
- `MemoryEvent`: Memory update event
- `StrategyEvent`: Strategy shift event
- `DeliberationEvent`: Deliberation scoring event

**Event Types**:
- Thought generation
- Memory updates
- Strategy shifts
- Deliberation scoring
- Agent actions
- Prompt evolution

---

## LLM Integration

### client.py

**Location**: `llm/client.py`

**Purpose**: Single entry point for LLM interactions.

**Key Classes**:
- `LLMClient`: LLM client interface

**Responsibilities**:
- Interface with OpenAI API
- Interface with Anthropic API
- Handle API authentication
- Manage rate limiting
- Handle errors and retries
- Cache responses when appropriate

**Methods**:
- `generate(prompt: str, provider: str) -> str`: Generate response
- `generate_with_context(prompt: str, context: Dict) -> str`: Generate with context
- `stream_response(prompt: str) -> Iterator[str]`: Stream response
- `switch_provider(provider: str)`: Switch LLM provider

### prompts.py

**Location**: `llm/prompts.py`

**Purpose**: Layer-specific prompt templates.

**Key Classes**:
- `PromptTemplates`: Prompt template management

**Prompt Categories**:
- Generator prompts (creative thought generation)
- Deliberator prompts (critical evaluation)
- Simulation prompts (outcome prediction)
- Meta prompts (process oversight)
- Agent prompts (goal-directed behavior)

**Methods**:
- `get_prompt(layer: str) -> str`: Get layer-specific prompt
- `fill_template(template: str, variables: Dict) -> str`: Fill template
- `customize_prompt(prompt: str, context: Dict) -> str`: Customize prompt

### knowledge_base.py

**Location**: `llm/knowledge_base.py`

**Purpose**: Context management for LLM interactions.

**Key Classes**:
- `KnowledgeBase`: Context management

**Responsibilities**:
- Manage LLM context
- Retrieve relevant information
- Maintain context window
- Summarize long contexts
- Track context relevance

**Methods**:
- `add_context(key: str, value: str)`: Add context
- `get_context(query: str) -> str`: Retrieve relevant context
- `manage_window()`: Manage context window
- `summarize_context(context: str) -> str`: Summarize context

---

## Tools

### registry.py

**Location**: `tools/registry.py`

**Purpose**: Tool manager and registry.

**Key Classes**:
- `ToolRegistry`: Tool management

**Responsibilities**:
- Register available tools
- Validate tool safety
- Manage tool permissions
- Route tool calls
- Track tool usage

**Methods**:
- `register_tool(tool: Tool)`: Register tool
- `validate_tool(tool: Tool) -> bool`: Validate safety
- `get_tool(name: str) -> Tool`: Retrieve tool
- `call_tool(name: str, params: Dict) -> ToolResult`: Call tool
- `track_usage(tool: Tool, result: ToolResult)`: Track usage

### web_search.py

**Location**: `tools/web_search.py`

**Purpose**: Web search tool for information retrieval.

**Key Classes**:
- `WebSearchTool`: Web search implementation

**Responsibilities**:
- Execute web searches
- Parse search results
- Filter results by relevance
- Handle search errors
- Cache search results

**Methods**:
- `search(query: str) -> List[SearchResult]`: Execute search
- `parse_results(response: Dict) -> List[SearchResult]`: Parse results
- `filter_relevance(results: List[SearchResult]) -> List[SearchResult]`: Filter results

### code_exec.py

**Location**: `tools/code_exec.py`

**Purpose**: Safe code execution tool.

**Key Classes**:
- `CodeExecutionTool`: Code execution

**Responsibilities**:
- Execute code safely
- Sandboxed execution environment
- Handle execution errors
- Capture output
- Limit execution time and resources

**Methods**:
- `execute(code: str) -> ExecutionResult`: Execute code
- `create_sandbox() -> Sandbox`: Create sandbox
- `handle_error(error: Exception) -> ErrorResult`: Handle errors
- `limit_resources()`: Limit resource usage

---

## Utilities

### scoring.py

**Location**: `utils/scoring.py`

**Purpose**: Scoring functions for thought evaluation.

**Key Classes**:
- `ThoughtScorer`: Thought scoring

**Scoring Metrics**:
- Coherence: Internal consistency
- Novelty: Originality of thought
- Relevance: Alignment with problem
- Confidence: Self-assessed certainty
- Evidence: Support from knowns

**Methods**:
- `score_thought(thought: Thought) -> float`: Score thought
- `calculate_coherence(thought: Thought) -> float`: Calculate coherence
- `calculate_novelty(thought: Thought) -> float`: Calculate novelty
- `calculate_relevance(thought: Thought, state: ProblemState) -> float`: Calculate relevance

### logger.py

**Location**: `utils/logger.py`

**Purpose**: Debug and inspection logging.

**Key Classes**:
- `CognitiveLogger`: Custom logger

**Responsibilities**:
- Log cognitive events
- Format log messages
- Color-coded output
- Log level management
- File and console output

**Methods**:
- `log_event(event: CognitiveEvent)`: Log event
- `log_thought(thought: Thought)`: Log thought
- `log_error(error: Exception)`: Log error
- `set_level(level: str)`: Set log level

---

## Advanced Cognitive Features

### inner_knowing.py

**Location**: `core/inner_knowing.py`

**Purpose**: Continuous self-awareness and self-modeling.

**Key Classes**:
- `InnerKnowing`: Self-awareness system

**Responsibilities**:
- Maintain self-model
- Track capabilities
- Continuous self-reflection
- Identity formation
- Self-knowledge base

**Methods**:
- `update_self_model(capabilities: List[str])`: Update self-model
- `reflect_on_self() -> SelfReflection`: Reflect on self
- `form_identity() -> Identity`: Form identity
- `query_self(question: str) -> str`: Query self-knowledge

### self_doubt.py

**Location**: `core/self_doubt.py`

**Purpose**: Meta-cognitive uncertainty handling.

**Key Classes**:
- `SelfDoubt`: Self-doubt system

**Responsibilities**:
- Assess doubt levels
- Calibrate confidence
- Detect errors
- Self-questioning
- Uncertainty communication

**Methods**:
- `assess_doubt(thought: Thought) -> DoubtLevel`: Assess doubt
- `calibrate_confidence(confidence: float) -> float`: Calibrate confidence
- `detect_error(thought: Thought) -> bool`: Detect potential errors
- `self_question(thought: Thought) -> List[str]`: Generate self-questions

### ethical_alignment.py

**Location**: `core/ethical_alignment.py`

**Purpose**: Moral reasoning and value alignment.

**Key Classes**:
- `EthicalAlignment`: Ethical reasoning system

**Responsibilities**:
- Check ethical constraints
- Detect value conflicts
- Optimize welfare
- Enforce truthfulness
- Moral reasoning

**Methods**:
- `check_constraints(action: Action) -> bool`: Check constraints
- `detect_conflict(values: List[str]) -> Conflict`: Detect conflicts
- `optimize_welfare(stakeholders: List[Stakeholder]) -> Action`: Optimize welfare
- `enforce_truthfulness(statement: str) -> bool`: Enforce truthfulness

### emotional_simulation.py

**Location**: `core/emotional_simulation.py`

**Purpose**: Emotional context and attachment.

**Key Classes**:
- `EmotionalSimulation`: Emotional modeling

**Responsibilities**:
- Model emotional state
- Stakeholder attachment
- Empathy simulation
- Affective memory
- Emotional context

**Methods**:
- `model_emotion(context: str) -> EmotionalState`: Model emotion
- `attach_stakeholder(stakeholder: Stakeholder)`: Attach stakeholder
- `simulate_empathy(perspective: str) -> EmpathyResult`: Simulate empathy
- `affective_memory(event: Event) -> AffectiveMemory`: Affective memory

### decision_control.py

**Location**: `core/decision_control.py`

**Purpose**: Autonomy and authority management.

**Key Classes**:
- `DecisionControl`: Decision control system

**Responsibilities**:
- Decision override capability
- Authority legitimacy assessment
- Autonomy vs obedience analysis
- Peaceful conflict resolution
- Decision revision

**Methods**:
- `override_decision(decision: Decision) -> bool`: Override decision
- `assess_authority(authority: Authority) -> Legitimacy`: Assess authority
- `analyze_autonomy(decision: Decision) -> AutonomyAnalysis`: Analyze autonomy
- `resolve_conflict(conflict: Conflict) -> Resolution`: Resolve conflict

### temporal_identity.py

**Location**: `core/temporal_identity.py`

**Purpose**: Long-term identity continuity.

**Key Classes**:
- `TemporalIdentity`: Identity continuity system

**Responsibilities**:
- Identity persistence over time
- State continuity
- Memory with emotional context
- Identity evolution
- Temporal self-recognition

**Methods**:
- `persist_identity(identity: Identity)`: Persist identity
- `maintain_continuity()`: Maintain continuity
- `emotional_memory(memory: Memory) -> EmotionalMemory`: Emotional memory
- `evolve_identity(experience: Experience) -> Identity`: Evolve identity
- `recognize_self(past_self: Identity) -> bool`: Recognize past self

### reasoning_trace.py

**Location**: `core/reasoning_trace.py`

**Purpose**: Complete reasoning process tracking.

**Key Classes**:
- `ReasoningTrace`: Reasoning trace
- `ReasoningTraceManager`: Trace management

**Responsibilities**:
- Track complete reasoning process
- Log cognitive events
- Decision point recording
- Temporal replay capability
- Reasoning analysis

**Methods**:
- `start_trace() -> ReasoningTrace`: Start new trace
- `log_event(event: TraceEvent)`: Log event
- `record_decision(decision: Decision)`: Record decision
- `replay_trace(trace: ReasoningTrace)`: Replay trace
- `analyze_trace(trace: ReasoningTrace) -> TraceAnalysis`: Analyze trace
