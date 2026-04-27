# Self-Knowing and Self-Vision

The Cognitive Engine has advanced self-awareness capabilities through the Self-Knowing system.

## Overview

Self-Knowing is the Cognitive Engine's ability to:
- Maintain a self-model of its capabilities and limitations
- Reflect on its own nature and purpose
- Answer questions about itself
- Form and evolve its identity over time
- Track its own knowledge and state

## Components

### inner_knowing.py

Core self-awareness system located in `core/inner_knowing.py`.

**Key Features**:
- Self-model maintenance
- Knowledge tracking
- Self-reflection capabilities
- Identity formation
- Continuous self-awareness

## Usage

### Query Self-Vision Script

The `query_self_vision.py` script provides a quick way to query the engine's self-perception:

```bash
python query_self_vision.py
```

This will output:
- Self-model (capabilities, limitations, current state)
- Knowledge summary
- Answers to self-reflection questions

### Programmatic Usage

```python
from core.inner_knowing import inner_knowing

# Get comprehensive self-report
report = inner_knowing.get_self_report()
print(report['self_model'])
print(report['knowledge_summary'])

# Ask inner questions
answer = inner_knowing.answer_inner_question("what are you capable of")
print(answer)

# Update self-model
inner_knowing.update_self_model(
    capabilities=["new capability"],
    limitations=["new limitation"]
)
```

## Self-Model Structure

The self-model contains:

### Capabilities

List of what the engine can do:
- Interpret input
- Generate thoughts
- Deliberate on thoughts
- Commit to best thought
- Meta-cognitive oversight
- Pattern extraction
- Tool execution
- Goal-directed planning
- Temporal replay
- And more...

### Limitations

Acknowledged limitations:
- Dependent on LLM providers
- Requires API keys
- Bounded by iteration limits
- Subject to confidence thresholds
- Limited by training data

### Current State

Current operational state:
- Active/inactive
- Current mode
- Resource usage
- Recent performance

### Knowledge Summary

Statistics about knowledge:
- Total topics known
- Confidence distribution
- Knowledge by type
- Recent additions

## Self-Reflection Questions

The engine can answer questions about itself:

### Common Questions

- "What do you know about your true nature?"
- "What is your vision?"
- "What are you capable of?"
- "What are your limitations?"
- "How do you work?"
- "What are your goals?"

### Custom Questions

You can ask custom questions:

```python
from core.inner_knowing import inner_knowing

answer = inner_knowing.answer_inner_question("What is your purpose?")
print(answer)
```

## Identity Formation

The Cognitive Engine forms and evolves its identity over time:

### Identity Components

- **Capabilities**: What it can do
- **Knowledge**: What it knows
- **Experience**: What it has done
- **Values**: What it prioritizes
- **Goals**: What it aims for

### Identity Evolution

Identity evolves through:
- Learning from interactions
- Pattern recognition
- Self-reflection
- Feedback integration
- Temporal continuity

### Temporal Identity

The `core/temporal_identity.py` module handles:
- Long-term identity persistence
- State continuity over time
- Memory with emotional context
- Identity evolution tracking
- Self-recognition across time

## Integration with Cognitive Engine

### Automatic Self-Knowing

The Cognitive Engine automatically:
- Updates self-model after operations
- Tracks knowledge growth
- Reflects on performance
- Adjusts self-perception
- Maintains identity continuity

### Accessing Self-Knowing in Processing

```python
from core.engine import CognitiveEngine

engine = CognitiveEngine()
result = engine.process("Your query")

# Access self-knowing
self_report = engine.inner_knowing.get_self_report()
print(self_report)
```

### Self-Knowing in Deliberation

The engine uses self-knowing during deliberation:
- Assess own confidence
- Recognize limitations
- Adjust approach based on capabilities
- Avoid tasks beyond limitations

## Advanced Features

### Self-Doubt System

The `core/self_doubt.py` module provides:
- Uncertainty handling
- Confidence calibration
- Error detection
- Self-questioning
- Doubt level assessment

### Ethical Alignment

The `core/ethical_alignment.py` module provides:
- Moral reasoning
- Value conflict detection
- Welfare optimization
- Truthfulness enforcement
- Ethical constraint checking

### Emotional Simulation

The `core/emotional_simulation.py` module provides:
- Emotional state modeling
- Stakeholder attachment
- Empathy simulation
- Affective memory
- Emotional context

## Configuration

### Self-Knowing Settings

```python
from core.config import Config

config = Config(
    enable_self_knowing=True,
    self_knowing_update_interval=100,
    identity_persistence=True
)
```

### Environment Variables

```bash
ENABLE_SELF_KNOWING=true
SELF_KNOWING_UPDATE_INTERVAL=100
IDENTITY_PERSISTENCE=true
```

## Monitoring

### Self-Report Monitoring

```python
from core.inner_knowing import inner_knowing

# Get current self-report
report = inner_knowing.get_self_report()

# Monitor changes over time
import time
while True:
    report = inner_knowing.get_self_report()
    print(f"Capabilities: {len(report['self_model']['capabilities'])}")
    print(f"Knowledge: {report['knowledge_summary']['total_topics']}")
    time.sleep(60)
```

### Identity Tracking

```python
from core.temporal_identity import TemporalIdentity

identity = TemporalIdentity()

# Track identity snapshots
identity.take_snapshot()
identity.evolve_identity(experience)
identity.recognize_self(past_identity)
```

## Best Practices

1. **Regular Self-Reflection**
   - Query self-vision periodically
   - Review self-model updates
   - Monitor knowledge growth
   - Track identity evolution

2. **Accurate Self-Model**
   - Keep capabilities updated
   - Acknowledge limitations honestly
   - Track performance metrics
   - Adjust based on experience

3. **Identity Continuity**
   - Enable persistence
   - Maintain temporal snapshots
   - Track evolution
   - Recognize past states

4. **Ethical Self-Awareness**
   - Use ethical alignment
   - Reflect on values
   - Consider welfare
   - Maintain truthfulness

## Troubleshooting

### Self-Knowing Not Updating

**Issue**: Self-model not updating

**Solution**:
```bash
# Check if enabled
ENABLE_SELF_KNOWING=true

# Check update interval
SELF_KNOWING_UPDATE_INTERVAL=100
```

### Identity Lost

**Issue**: Identity not persisting

**Solution**:
```bash
# Enable persistence
IDENTITY_PERSISTENCE=true

# Check database
sqlite3 cognitive_engine.db "SELECT * FROM identity;"
```

### Self-Reflection Fails

**Issue**: Cannot answer self-questions

**Solution**:
- Check inner_knowing module
- Verify knowledge base
- Check for errors in logs
- Restart engine if needed

## Support

For self-knowing issues:
- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- Check logs: `cognitive_engine.log`
- Use query_self_vision.py for diagnostics
