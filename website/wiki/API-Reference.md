# API Reference

This document provides reference documentation for the Cognitive Engine's public APIs.

## Table of Contents

- [Core Engine API](#core-engine-api)
- [Cognitive Layers API](#cognitive-layers-api)
- [Model Classes API](#model-classes-api)
- [Memory System API](#memory-system-api)
- [Agent API](#agent-api)
- [Learning System API](#learning-system-api)
- [Dashboard API](#dashboard-api)
- [LLM Client API](#llm-client-api)
- [Tools API](#tools-api)

---

## Core Engine API

### CognitiveEngine

**Module**: `core.engine`

**Class**: `CognitiveEngine`

Main orchestration engine that coordinates all cognitive layers.

#### Constructor

```python
def __init__(config: Optional[Config] = None)
```

**Parameters**:
- `config` (Optional[Config]): Configuration object. If None, uses default config.

**Example**:
```python
from core.engine import CognitiveEngine

engine = CognitiveEngine()
```

#### process()

```python
def process(self, input: str) -> ProcessResult
```

Process a user input through the cognitive engine.

**Parameters**:
- `input` (str): User query or problem statement

**Returns**:
- `ProcessResult`: Object containing final output and metadata

**Example**:
```python
result = engine.process("What is the meaning of life?")
print(result.final_output)
print(result.iteration_count)
print(result.reasoning_trace)
```

#### initialize_layers()

```python
def initialize_layers(self) -> None
```

Initialize all cognitive layers (Interpreter, Generator, Deliberator, Committer, Meta).

**Example**:
```python
engine.initialize_layers()
```

#### get_thought_graph()

```python
def get_thought_graph(self) -> ThoughtGraph
```

Get the current thought graph containing all generated thoughts.

**Returns**:
- `ThoughtGraph`: Graph of interconnected thoughts

**Example**:
```python
graph = engine.get_thought_graph()
for thought_id, thought in graph.thoughts.items():
    print(f"{thought.premise}: {thought.confidence}")
```

#### get_memory()

```python
def get_memory(self) -> ThreeLayerMemory
```

Get the three-layer memory system.

**Returns**:
- `ThreeLayerMemory`: Memory system with episodic, pattern, and rule layers

**Example**:
```python
memory = engine.get_memory()
episodic = memory.get_episodic_memory()
patterns = memory.get_pattern_memory()
rules = memory.get_rule_memory()
```

---

## Cognitive Layers API

### Interpreter

**Module**: `layers.interpreter`

**Class**: `Interpreter`

Transform raw input into structured ProblemState.

#### interpret()

```python
def interpret(self, input: str) -> ProblemState
```

Transform raw input into structured problem state.

**Parameters**:
- `input` (str): Raw user input

**Returns**:
- `ProblemState`: Structured problem definition

**Example**:
```python
from layers.interpreter import Interpreter

interpreter = Interpreter()
state = interpreter.interpret("How do I learn Python?")
print(state.goals)
print(state.constraints)
print(state.knowns)
```

### Generator

**Module**: `layers.generator`

**Class**: `Generator`

Create multiple competing thought candidates.

#### generate()

```python
def generate(self, problem_state: ProblemState) -> List[Thought]
```

Generate thought candidates from problem state.

**Parameters**:
- `problem_state` (ProblemState): Structured problem definition

**Returns**:
- `List[Thought]`: List of generated thought objects

**Example**:
```python
from layers.generator import Generator

generator = Generator()
thoughts = generator.generate(problem_state)
for thought in thoughts:
    print(f"{thought.premise}: {thought.confidence}")
```

### Deliberator

**Module**: `layers.deliberator`

**Class**: `Deliberator`

Evaluate, test, and evolve thoughts.

#### deliberate()

```python
def deliberate(self, thoughts: List[Thought]) -> List[Thought]
```

Evaluate and evolve a list of thoughts.

**Parameters**:
- `thoughts` (List[Thought]): List of thoughts to deliberate

**Returns**:
- `List[Thought]`: Evolved and scored list of thoughts

**Example**:
```python
from layers.deliberator import Deliberator

deliberator = Deliberator()
evolved_thoughts = deliberator.deliberate(thoughts)
for thought in evolved_thoughts:
    print(f"Score: {thought.score}, Confidence: {thought.confidence}")
```

### Committer

**Module**: `layers.committer`

**Class**: `Committer`

Select best thought and express output.

#### commit()

```python
def commit(self, thoughts: List[Thought]) -> ProcessResult
```

Commit to the best thought and produce output.

**Parameters**:
- `thoughts` (List[Thought]): List of thoughts to choose from

**Returns**:
- `ProcessResult`: Final result with output and metadata

**Example**:
```python
from layers.committer import Committer

committer = Committer()
result = committer.commit(evolved_thoughts)
print(result.final_output)
```

### Meta-Cognition

**Module**: `layers.meta`

**Class**: `MetaCognition`

Govern the thinking process itself.

#### should_continue()

```python
def should_continue(self, iteration: int, thoughts: List[Thought]) -> bool
```

Determine if cognitive process should continue.

**Parameters**:
- `iteration` (int): Current iteration number
- `thoughts` (List[Thought]): Current thoughts

**Returns**:
- `bool`: True if should continue, False if should stop

**Example**:
```python
from layers.meta import MetaCognition

meta = MetaCognition({
    "min_iterations": 3,
    "max_iterations": 50,
    "early_stop_confidence": 0.95
})

if meta.should_continue(iteration, thoughts):
    # Continue deliberation
    pass
else:
    # Stop and commit
    pass
```

---

## Model Classes API

### Thought

**Module**: `models.thought`

**Class**: `Thought`

First-class thought object with state, history, and evaluative properties.

#### Constructor

```python
def __init__(
    id: str,
    premise: str,
    confidence: float = 0.5,
    parent_nodes: Optional[List[str]] = None
)
```

**Parameters**:
- `id` (str): Unique identifier
- `premise` (str): Core hypothesis
- `confidence` (float): Initial confidence (0-1)
- `parent_nodes` (Optional[List[str]]): Parent thought IDs

**Example**:
```python
from models.thought import Thought

thought = Thought(
    id="thought_1",
    premise="Python is a versatile programming language",
    confidence=0.7
)
```

#### Methods

**update_confidence()**
```python
def update_confidence(self, new_confidence: float) -> None
```

**add_weakness()**
```python
def add_weakness(self, weakness: str) -> None
```

**record_test()**
```python
def record_test(self, test_result: Dict[str, Any]) -> None
```

**revise()**
```python
def revise(self, new_premise: str) -> Thought
```

### ThoughtGraph

**Module**: `models.thought`

**Class**: `ThoughtGraph`

Graph of interconnected thoughts.

#### Methods

**add_thought()**
```python
def add_thought(self, thought: Thought) -> None
```

**get_thought()**
```python
def get_thought(self, thought_id: str) -> Optional[Thought]
```

**get_related()**
```python
def get_related(self, thought_id: str) -> List[Thought]
```

**find_path()**
```python
def find_path(self, from_id: str, to_id: str) -> List[Thought]
```

### ProblemState

**Module**: `models.state`

**Class**: `ProblemState`

Structured problem definition.

#### Constructor

```python
def __init__(
    goals: List[str],
    constraints: List[str] = None,
    knowns: List[str] = None,
    unknowns: List[str] = None,
    context: str = ""
)
```

**Example**:
```python
from models.state import ProblemState

state = ProblemState(
    goals=["Learn Python programming"],
    constraints=["Limited time available"],
    knowns=["Python is popular", "Python has good documentation"],
    unknowns=["Best learning resources", "Time required"]
)
```

---

## Memory System API

### ThreeLayerMemory

**Module**: `core.memory`

**Class**: `ThreeLayerMemory`

Three-layer memory system (Episodic, Pattern, Rule).

#### Methods

**store_episodic()**
```python
def store_episodic(self, event: Dict[str, Any]) -> None
```

Store a raw event in episodic memory.

**Parameters**:
- `event` (Dict): Event data to store

**Example**:
```python
memory.store_episodic({
    "type": "thought_generation",
    "timestamp": datetime.now(),
    "data": {"thought_premise": "..."}
})
```

**extract_patterns()**
```python
def extract_patterns(self) -> List[Pattern]
```

Extract recurring patterns from episodic memory.

**Returns**:
- `List[Pattern]`: List of extracted patterns

**synthesize_rules()**
```python
def synthesize_rules(self, patterns: List[Pattern]) -> List[Rule]
```

Convert patterns into actionable rules.

**Parameters**:
- `patterns` (List[Pattern]): Patterns to convert

**Returns**:
- `List[Rule]`: List of synthesized rules

**apply_rules()**
```python
def apply_rules(self, state: ProblemState) -> ProblemState
```

Apply learned rules to problem state.

**Parameters**:
- `state` (ProblemState): Problem state to modify

**Returns**:
- `ProblemState`: Modified problem state

**get_episodic_memory()**
```python
def get_episodic_memory(self) -> List[Dict]
```

Retrieve episodic memory.

**Returns**:
- `List[Dict]`: All episodic events

**get_pattern_memory()**
```python
def get_pattern_memory(self) -> List[Pattern]
```

Retrieve pattern memory.

**Returns**:
- `List[Pattern]`: All extracted patterns

**get_rule_memory()**
```python
def get_rule_memory(self) -> List[Rule]
```

Retrieve rule memory.

**Returns**:
- `List[Rule]`: All learned rules

---

## Agent API

### Agent

**Module**: `agent.agent`

**Class**: `Agent`

Autonomous agent with goal-directed behavior.

#### Constructor

```python
def __init__(self, tool_registry: Optional[ToolRegistry] = None)
```

#### run()

```python
def run(self, goal: str) -> AgentResult
```

Execute agent with a goal.

**Parameters**:
- `goal` (str): Goal to achieve

**Returns**:
- `AgentResult`: Result of agent execution

**Example**:
```python
from agent.agent import Agent

agent = Agent()
result = agent.run("Research the latest developments in AI")
print(result.final_state)
print(result.actions_taken)
```

### Planner

**Module**: `agent.planner`

**Class**: `Planner`

Convert goals into actionable plans.

#### create_plan()

```python
def create_plan(self, goal: str) -> Plan
```

Create execution plan from goal.

**Parameters**:
- `goal` (str): Goal to plan for

**Returns**:
- `Plan`: Execution plan

### Executor

**Module**: `agent.executor`

**Class**: `Executor`

Execute actions using tools.

#### execute()

```python
def execute(self, plan: Plan) -> ActionResult
```

Execute a plan.

**Parameters**:
- `plan` (Plan): Plan to execute

**Returns**:
- `ActionResult`: Result of execution

### Observer

**Module**: `agent.observer`

**Class**: `Observer`

Interpret and analyze execution results.

#### observe()

```python
def observe(self, result: ActionResult) -> Observation
```

Observe and analyze execution results.

**Parameters**:
- `result` (ActionResult): Result to observe

**Returns**:
- `Observation`: Analysis of results

---

## Learning System API

### PatternExtractor

**Module**: `learning.extractor`

**Class**: `PatternExtractor`

Extract patterns from memory.

#### extract_patterns()

```python
def extract_patterns(self, memory: List[Dict]) -> List[Pattern]
```

Extract patterns from episodic memory.

**Parameters**:
- `memory` (List[Dict]): Episodic memory events

**Returns**:
- `List[Pattern]`: Extracted patterns

### RuleSynthesizer

**Module**: `learning.synthesizer`

**Class**: `RuleSynthesizer`

Convert patterns into rules.

#### synthesize_rules()

```python
def synthesize_rules(self, patterns: List[Pattern]) -> List[Rule]
```

Synthesize rules from patterns.

**Parameters**:
- `patterns` (List[Pattern]): Patterns to convert

**Returns**:
- `List[Rule]`: Synthesized rules

### KnowledgeUpdater

**Module**: `learning.updater`

**Class**: `KnowledgeUpdater`

Inject learned knowledge into reasoning system.

#### update_rules()

```python
def update_rules(self, rules: List[Rule]) -> None
```

Update rule memory with new rules.

**Parameters**:
- `rules` (List[Rule]): Rules to add

**apply_rule()**
```python
def apply_rule(self, rule: Rule, state: ProblemState) -> ProblemState
```

Apply a rule to problem state.

**Parameters**:
- `rule` (Rule): Rule to apply
- `state` (ProblemState): Problem state to modify

**Returns**:
- `ProblemState`: Modified problem state

---

## Dashboard API

### DashboardServer

**Module**: `dashboard.server`

**Class**: `DashboardServer`

WebSocket server for real-time telemetry.

#### Constructor

```python
def __init__(self, host: str = "0.0.0.0", port: int = 8000)
```

#### start()

```python
def start(self) -> None
```

Start the WebSocket server.

**Example**:
```python
from dashboard.server import DashboardServer

server = DashboardServer(port=8000)
server.start()
```

### DashboardStreamer

**Module**: `dashboard.stream`

**Class**: `DashboardStreamer`

Stream cognitive events to dashboard.

#### stream_event()

```python
def stream_event(self, event: CognitiveEvent) -> None
```

Stream a cognitive event to dashboard.

**Parameters**:
- `event` (CognitiveEvent): Event to stream

**Example**:
```python
from dashboard.stream import dashboard_streamer
from dashboard.events import ThoughtEvent

event = ThoughtEvent(
    thought_id="thought_1",
    premise="Example thought",
    confidence=0.8
)
dashboard_streamer.stream_event(event)
```

---

## LLM Client API

### LLMClient

**Module**: `llm.client`

**Class**: `LLMClient`

Single entry point for LLM interactions.

#### Constructor

```python
def __init__(self, provider: str = "openai")
```

**Parameters**:
- `provider` (str): LLM provider ("openai" or "anthropic")

#### generate()

```python
def generate(self, prompt: str) -> str
```

Generate response from LLM.

**Parameters**:
- `prompt` (str): Prompt to send to LLM

**Returns**:
- `str**: LLM response

**Example**:
```python
from llm.client import LLMClient

client = LLMClient(provider="openai")
response = client.generate("Explain quantum computing")
print(response)
```

#### generate_with_context()

```python
def generate_with_context(self, prompt: str, context: Dict) -> str
```

Generate response with additional context.

**Parameters**:
- `prompt` (str): Prompt to send
- `context` (Dict): Additional context

**Returns**:
- `str`: LLM response

#### stream_response()

```python
def stream_response(self, prompt: str) -> Iterator[str]
```

Stream response from LLM.

**Parameters**:
- `prompt` (str): Prompt to send

**Returns**:
- `Iterator[str]`: Stream of response chunks

---

## Tools API

### ToolRegistry

**Module**: `tools.registry`

**Class**: `ToolRegistry`

Manage and execute tools.

#### register_tool()

```python
def register_tool(self, tool: Tool) -> None
```

Register a tool.

**Parameters**:
- `tool` (Tool): Tool to register

#### call_tool()

```python
def call_tool(self, name: str, params: Dict) -> ToolResult
```

Call a registered tool.

**Parameters**:
- `name` (str): Tool name
- `params` (Dict): Tool parameters

**Returns**:
- `ToolResult`: Result of tool execution

**Example**:
```python
from tools.registry import tool_registry

result = tool_registry.call_tool("web_search", {"query": "AI news"})
print(result.data)
```

### WebSearchTool

**Module**: `tools.web_search`

**Class**: `WebSearchTool`

Web search tool for information retrieval.

#### search()

```python
def search(self, query: str) -> List[SearchResult]
```

Execute web search.

**Parameters**:
- `query` (str): Search query

**Returns**:
- `List[SearchResult]`: Search results

**Example**:
```python
from tools.web_search import WebSearchTool

tool = WebSearchTool()
results = tool.search("latest AI developments")
for result in results:
    print(f"{result.title}: {result.url}")
```

### CodeExecutionTool

**Module**: `tools.code_exec`

**Class**: `CodeExecutionTool`

Safe code execution tool.

#### execute()

```python
def execute(self, code: str) -> ExecutionResult
```

Execute code safely.

**Parameters**:
- `code` (str): Code to execute

**Returns**:
- `ExecutionResult`: Execution result with output

**Example**:
```python
from tools.code_exec import CodeExecutionTool

tool = CodeExecutionTool()
result = tool.execute("print('Hello, World!')")
print(result.output)
```

---

## Configuration API

### Config

**Module**: `core.config`

**Class**: `Config`

Configuration management.

#### Constructor

```python
def __init__(
    min_iterations: int = 3,
    max_iterations: int = 50,
    early_stop_confidence: float = 0.95,
    confidence_threshold: float = 0.7,
    enable_dashboard: bool = True,
    dashboard_port: int = 8000,
    default_llm_provider: str = "openai"
)
```

#### load_from_env()

```python
@classmethod
def load_from_env(cls) -> Config
```

Load configuration from environment variables.

**Returns**:
- `Config`: Configuration object

**Example**:
```python
from core.config import Config

config = Config.load_from_env()
print(config.min_iterations)
print(config.default_llm_provider)
```

---

## Error Handling

### Common Exceptions

**CognitiveEngineError**
Base exception for cognitive engine errors.

**MemoryError**
Exception raised for memory-related errors.

**ToolExecutionError**
Exception raised when tool execution fails.

**LLMError**
Exception raised for LLM-related errors.

**PatternExtractionError**
Exception raised for pattern extraction failures.

**RuleSynthesisError**
Exception raised for rule synthesis failures.

### Example Error Handling

```python
from core.engine import CognitiveEngine
from core.engine import CognitiveEngineError

try:
    engine = CognitiveEngine()
    result = engine.process("Your query here")
except CognitiveEngineError as e:
    print(f"Cognitive engine error: {e}")
except MemoryError as e:
    print(f"Memory error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Type Definitions

### ProcessResult

```python
class ProcessResult:
    final_output: str
    iteration_count: int
    reasoning_trace: Optional[str]
    thought_graph: ThoughtGraph
    confidence: float
    timestamp: datetime
```

### AgentResult

```python
class AgentResult:
    final_state: Dict
    actions_taken: List[Action]
    observations: List[Observation]
    goal_achieved: bool
    execution_time: float
```

### ToolResult

```python
class ToolResult:
    success: bool
    data: Any
    error: Optional[str]
    execution_time: float
```

### SearchResult

```python
class SearchResult:
    title: str
    url: str
    snippet: str
    relevance: float
```

### ExecutionResult

```python
class ExecutionResult:
    output: str
    error: Optional[str]
    execution_time: float
    success: bool
```

---

## Usage Examples

### Basic Usage

```python
from core.engine import CognitiveEngine

# Initialize engine
engine = CognitiveEngine()

# Process a query
result = engine.process("What is cognitive science?")

# Access results
print(result.final_output)
print(result.confidence)
print(result.iteration_count)
```

### With Custom Configuration

```python
from core.engine import CognitiveEngine
from core.config import Config

# Create custom config
config = Config(
    min_iterations=5,
    max_iterations=20,
    confidence_threshold=0.8
)

# Initialize with config
engine = CognitiveEngine(config)
result = engine.process("Explain quantum computing")
```

### Accessing Thought Graph

```python
from core.engine import CognitiveEngine

engine = CognitiveEngine()
result = engine.process("Compare Python and JavaScript")

# Access thought graph
graph = engine.get_thought_graph()
for thought_id, thought in graph.thoughts.items():
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
memory = engine.get_memory()
episodic = memory.get_episodic_memory()
patterns = memory.get_pattern_memory()
rules = memory.get_rule_memory()

print(f"Episodic entries: {len(episodic)}")
print(f"Patterns found: {len(patterns)}")
print(f"Rules learned: {len(rules)}")
```

### Agent Mode

```python
from agent.agent import Agent

agent = Agent()
result = agent.run("Research the latest developments in AI")

print(f"Goal achieved: {result.goal_achieved}")
print(f"Actions taken: {len(result.actions_taken)}")
```

### Using Tools

```python
from tools.registry import tool_registry

# Call web search tool
result = tool_registry.call_tool("web_search", {
    "query": "latest AI news"
})

# Call code execution tool
result = tool_registry.call_tool("code_exec", {
    "code": "print(2 + 2)"
})
```
