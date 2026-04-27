# User Guide

This guide helps users effectively use the Cognitive Engine for various tasks.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Using the Dashboard](#using-the-dashboard)
- [Agent Mode](#agent-mode)
- [Best Practices](#best-practices)
- [Common Use Cases](#common-use-cases)
- [Tips and Tricks](#tips-and-tricks)

---

## Introduction

The Cognitive Engine is an AI system that thinks before it answers. Unlike traditional AI that provides immediate responses, the Cognitive Engine:

- **Explores multiple perspectives** before concluding
- **Evaluates and refines thoughts** through deliberation
- **Provides confidence scores** for its answers
- **Shows reasoning traces** for transparency
- **Learns from experience** over time

### Key Concepts

**Thoughts**: Structured ideas with confidence scores, not just text
**Deliberation**: The process of testing and refining thoughts
**Meta-Cognition**: The system's oversight of its own thinking
**Memory**: Three layers (episodic, pattern, rule) for learning
**Confidence**: How certain the system is about its answer

---

## Getting Started

### First Time Setup

1. **Install the Engine**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure API Keys**
```bash
cp .env.example .env
nano .env
# Add your OPENAI_API_KEY or ANTHROPIC_API_KEY
```

3. **Test the Installation**
```bash
python run.py test
```

4. **Start Using**
```bash
python run.py
```

### Your First Query

When you start the engine, you'll see:

```
Cognitive Engine v1.0.0
Enter your query (or 'quit' to exit): 
```

Try a simple question:
```
What is cognitive science?
```

The engine will:
1. Interpret your question
2. Generate multiple thoughts about the answer
3. Deliberate and refine those thoughts
4. Select the best thought
5. Provide the final answer with confidence

Example output:
```
[Processing thoughts...]
[Iteration 1/10] Generated 3 candidate thoughts
[Iteration 2/10] Deliberating on thoughts...
[Iteration 3/10] Confidence threshold reached

Answer: Cognitive science is the interdisciplinary study of the mind and its processes...
Confidence: 0.87
Iterations: 3
```

---

## Basic Usage

### Interactive Mode

The most common way to use the engine is in interactive mode:

```bash
python run.py
# or
python run.py interactive
```

#### Example Session

```
Enter your query: Explain quantum computing to a beginner

[Processing thoughts...]
[Iteration 1/10] Generated 4 candidate thoughts
[Iteration 2/10] Deliberating on thoughts...
[Iteration 3/10] Refining weak thoughts...
[Iteration 4/10] Confidence threshold reached

Answer: Quantum computing is a type of computation that uses quantum mechanics...
Confidence: 0.92
Iterations: 4

Reasoning trace available? [y/n]: y

Thought 1: Quantum computing uses qubits instead of bits
  Confidence: 0.85
  Weaknesses: Lacks concrete examples

Thought 2: Quantum computing leverages superposition and entanglement
  Confidence: 0.90
  Weaknesses: Technical terms may confuse beginners

Thought 3: Quantum computing can solve certain problems exponentially faster
  Confidence: 0.88
  Weaknesses: Doesn't explain why

Final selected: Thought 2 (refined to add beginner-friendly examples)

Enter your query: 
```

### Command Line Usage

You can also use the engine from the command line:

```bash
# Single query
python run.py query "What is machine learning?"

# With output to file
python run.py query "Explain AI" > output.txt

# With custom configuration
MIN_ITERATIONS=5 python run.py query "Your question"
```

### Python API

For programmatic use:

```python
from core.engine import CognitiveEngine

# Initialize engine
engine = CognitiveEngine()

# Process a query
result = engine.process("What is the meaning of life?")

# Access results
print(result.final_output)
print(result.confidence)
print(result.iteration_count)

# Access thought graph
for thought_id, thought in engine.thought_graph.thoughts.items():
    print(f"{thought.premise}: {thought.confidence}")
```

---

## Advanced Features

### Customizing Iteration Depth

Control how deeply the engine thinks:

```bash
# Fast, shallow thinking
MIN_ITERATIONS=1 MAX_ITERATIONS=5 python run.py

# Deep, thorough thinking
MIN_ITERATIONS=5 MAX_ITERATIONS=50 python run.py
```

In Python:

```python
from core.config import Config
from core.engine import CognitiveEngine

config = Config(min_iterations=5, max_iterations=30)
engine = CognitiveEngine(config)
```

### Adjusting Confidence Thresholds

Set how confident the engine must be:

```bash
# Accept lower confidence for faster responses
CONFIDENCE_THRESHOLD=0.6 python run.py

# Require high confidence for quality
CONFIDENCE_THRESHOLD=0.9 python run.py
```

### Enabling Reasoning Traces

See how the engine reached its conclusion:

```bash
# Enable detailed reasoning traces
ENABLE_REASONING_TRACE=true python run.py
```

### Using Memory

The engine learns from previous interactions:

```python
engine = CognitiveEngine()

# Process multiple queries - engine learns patterns
engine.process("What is Python?")
engine.process("How do I learn programming?")
engine.process("What are good Python resources?")

# Access learned patterns
memory = engine.get_memory()
patterns = memory.get_pattern_memory()
print(f"Learned {len(patterns)} patterns")

# Access learned rules
rules = memory.get_rule_memory()
print(f"Learned {len(rules)} rules")
```

---

## Using the Dashboard

The dashboard provides real-time visualization of the cognitive process.

### Starting the Dashboard

```bash
python run.py dashboard
```

Access at: `http://localhost:8000`

### Dashboard Features

**Thought Graph**: Visual representation of thoughts and relationships
- Nodes represent thoughts
- Edges show relationships
- Colors indicate confidence levels
- Size shows importance

**Memory Panel**: Shows memory growth and content
- Episodic memory: Raw events
- Pattern memory: Discovered patterns
- Rule memory: Learned rules

**Strategy Panel**: Displays cognitive strategy shifts
- Parameter changes over time
- Confidence trends
- Iteration patterns

**Deliberation Panel**: Shows thought evolution
- Initial thoughts
- Refinements and mutations
- Final selection

### Interpreting the Dashboard

**Thought Clusters**: Groups of related thoughts
- Dense clusters = focused reasoning
- Sparse clusters = exploration

**Confidence Trends**: Upward trends indicate improving certainty
- Steady rise = good deliberation
- Fluctuations = uncertainty or reconsideration

**Memory Growth**: Shows learning over time
- Steady growth = active learning
- Plateaus = saturation or insufficient data

---

## Agent Mode

Agent mode enables goal-directed autonomous behavior.

### Starting Agent Mode

```bash
python run.py agent
```

### Agent Capabilities

The agent can:
- Accept high-level goals
- Create execution plans
- Use tools (web search, code execution)
- Observe and learn from results
- Adapt its strategy

### Example Agent Session

```
Enter goal: Research the latest developments in AI and summarize key findings

[Planning...]
Plan created with 5 steps:
1. Search for recent AI developments
2. Read top 5 articles
3. Extract key findings
4. Synthesize summary
4. Report results

[Executing...]
Step 1: Searching for recent AI developments...
  Tool: web_search
  Query: "latest AI developments 2024"
  Results: Found 15 articles

Step 2: Reading top 5 articles...
  Tool: web_search
  Reading: Article 1, 2, 3, 4, 5
  Extracted: 23 key points

Step 3: Extracting key findings...
  Identified: 8 major themes
  Confidence: 0.85

Step 4: Synthesizing summary...
  Generated: Comprehensive summary
  Confidence: 0.91

Step 5: Reporting results...
  Summary: [Full summary text]

Goal achieved: Yes
Steps taken: 5
Execution time: 2m 34s
```

### Agent Configuration

```bash
# Limit agent steps
AGENT_STEP_LIMIT=50 python run.py agent

# Enable goal validation
AGENT_GOAL_VALIDATION=true python run.py agent

# Enable memory control
AGENT_MEMORY_CONTROL=true python run.py agent
```

---

## Best Practices

### Formulating Effective Queries

**Be Specific**
- Good: "Explain how neural networks learn from data"
- Poor: "Tell me about AI"

**Provide Context**
- Good: "As a beginner programmer, explain recursion with simple examples"
- Poor: "Explain recursion"

**Ask for What You Need**
- Good: "Compare Python and JavaScript for web development, focusing on performance and ecosystem"
- Poor: "Python vs JavaScript"

**Set Constraints**
- Good: "Explain quantum computing in under 200 words for a non-technical audience"
- Poor: "Explain quantum computing briefly"

### When to Use Deep Thinking

**Use Deep Thinking (high iterations) for:**
- Complex problems requiring careful consideration
- Important decisions where accuracy matters
- Creative tasks requiring exploration
- Learning new topics

**Use Shallow Thinking (low iterations) for:**
- Simple factual questions
- Quick reference lookups
- Routine tasks
- When speed is critical

### Interpreting Confidence Scores

**High Confidence (0.8-1.0)**: Engine is very certain
- Can rely on the answer
- Good for factual information

**Medium Confidence (0.5-0.8)**: Engine is reasonably certain
- Answer is likely correct but may have nuances
- Consider verifying important information

**Low Confidence (0.0-0.5)**: Engine is uncertain
- Answer may be incomplete or speculative
- Consider asking for clarification
- May need more context

### Using Reasoning Traces

Review reasoning traces to:
- Understand how the engine reached its conclusion
- Identify alternative perspectives it considered
- Spot weaknesses in the reasoning
- Learn from the deliberation process

### Leveraging Memory

The engine learns from all interactions:
- Be consistent in your queries
- Provide feedback when answers are helpful or not
- Allow the engine to build context over time
- Review learned patterns periodically

---

## Common Use Cases

### Research and Learning

**Scenario**: Learning a new topic

```
Query: Explain machine learning to someone with a programming background

[Engine provides detailed explanation with technical depth]

Query: How does gradient descent work in practice?

[Engine remembers context, provides practical examples]

Query: What are common pitfalls when implementing ML?

[Engine draws on previous answers, provides comprehensive guidance]
```

### Decision Making

**Scenario**: Making an informed choice

```
Query: Compare PostgreSQL vs MongoDB for a social media application

[Engine provides detailed comparison]

Query: What are the long-term maintenance considerations?

[Engine considers trade-offs, provides nuanced advice]

Query: Based on a small team and limited budget, which would you recommend?

[Engine applies constraints, provides recommendation with confidence]
```

### Creative Writing

**Scenario**: Generating creative content

```
Query: Write a short story about an AI that learns to love

[Engine generates story with character development]

Query: Make the story more hopeful and less dystopian

[Engine refines with new direction]

Query: Add a subplot about the AI's relationship with its creator

[Engine integrates subplot coherently]
```

### Code Assistance

**Scenario**: Programming help

```
Query: How do I implement a binary search tree in Python?

[Engine provides implementation with explanation]

Query: Show me how to add deletion functionality

[Engine extends previous answer with deletion logic]

Query: What's the time complexity of this implementation?

[Engine analyzes and provides complexity analysis]
```

### Problem Solving

**Scenario**: Debugging an issue

```
Query: My Python script is slow, how can I profile it?

[Engine provides profiling methods]

Query: I used cProfile and found that database queries are slow. What now?

[Engine suggests optimization strategies]

Query: Should I use caching or indexing first?

[Engine analyzes trade-offs, provides recommendation]
```

---

## Tips and Tricks

### Speed Up Responses

```bash
# Reduce iterations
MIN_ITERATIONS=1 MAX_ITERATIONS=10

# Use faster LLM
DEFAULT_LLM_PROVIDER=openai

# Disable learning for one-time queries
ENABLE_LEARNING=false
```

### Improve Quality

```bash
# Increase iterations
MIN_ITERATIONS=5 MAX_ITERATIONS=50

# Require high confidence
CONFIDENCE_THRESHOLD=0.9

# Enable reasoning traces to understand decisions
ENABLE_REASONING_TRACE=true
```

### Save and Restore State

```python
import pickle

# Save engine state
with open('engine_state.pkl', 'wb') as f:
    pickle.dump(engine, f)

# Restore engine state
with open('engine_state.pkl', 'rb') as f:
    engine = pickle.load(f)
```

### Batch Processing

```python
queries = [
    "What is Python?",
    "What is JavaScript?",
    "What is Rust?"
]

results = []
for query in queries:
    result = engine.process(query)
    results.append(result)
    print(f"{query}: {result.confidence}")
```

### Custom Scoring

```python
from utils.scoring import ThoughtScorer

class CustomScorer(ThoughtScorer):
    def score_thought(self, thought):
        score = super().score_thought(thought)
        # Add custom scoring logic
        if "example" in thought.premise.lower():
            score += 0.1
        return score

# Use custom scorer
engine.deliberator.scorer = CustomScorer()
```

### Monitoring Performance

```python
import time

start = time.time()
result = engine.process("Your query")
end = time.time()

print(f"Processing time: {end - start:.2f}s")
print(f"Iterations: {result.iteration_count}")
print(f"Confidence: {result.confidence}")
```

---

## Troubleshooting Common Issues

### Engine Gives Wrong Answer

**Possible causes:**
- Insufficient iterations
- Low confidence threshold
- Ambiguous query
- Insufficient context

**Solutions:**
- Increase iterations: `MAX_ITERATIONS=50`
- Increase confidence threshold: `CONFIDENCE_THRESHOLD=0.9`
- Provide more context in your query
- Ask for reasoning trace to understand

### Engine Takes Too Long

**Possible causes:**
- Too many iterations
- Slow LLM provider
- Complex query
- Learning system active

**Solutions:**
- Reduce iterations: `MAX_ITERATIONS=10`
- Use faster provider: `DEFAULT_LLM_PROVIDER=openai`
- Simplify query
- Disable learning: `ENABLE_LEARNING=false`

### Confidence Always Low

**Possible causes:**
- Difficult or ambiguous topic
- Insufficient iterations
- High confidence threshold
- LLM uncertainty

**Solutions:**
- Provide more context
- Increase iterations
- Lower threshold slightly: `CONFIDENCE_THRESHOLD=0.7`
- Accept that some topics are inherently uncertain

### Memory Not Working

**Possible causes:**
- Learning disabled
- Insufficient data
- Database issues

**Solutions:**
- Enable learning: `ENABLE_LEARNING=true`
- Process more queries to build data
- Check database: `sqlite3 cognitive_engine.db "SELECT COUNT(*) FROM episodic_memory;"`

---

## Advanced Topics

### Custom Tools

Create custom tools for agent mode:

```python
from tools.registry import ToolRegistry, Tool

class CustomTool(Tool):
    def execute(self, params):
        # Your custom logic
        return {"result": "custom output"}

# Register tool
tool_registry.register_tool(CustomTool())
```

### Custom Prompts

Modify how the engine thinks:

```python
from llm.prompts import PromptTemplates

templates = PromptTemplates()
templates.generator_prompt = """
Your custom generator prompt here...
"""
```

### Integration with Other Systems

```python
# Flask integration example
from flask import Flask, request, jsonify
from core.engine import CognitiveEngine

app = Flask(__name__)
engine = CognitiveEngine()

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    result = engine.process(data['query'])
    return jsonify({
        'answer': result.final_output,
        'confidence': result.confidence
    })
```

---

## Support

For help:
- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- Check the [Troubleshooting Guide](Troubleshooting.md) for common issues
- Review logs in `cognitive_engine.log`
