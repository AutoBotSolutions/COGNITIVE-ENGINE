# Frequently Asked Questions

Common questions about the Cognitive Engine.

## General Questions

### What is the Cognitive Engine?

The Cognitive Engine is an AI system that implements explicit, persistent, and inspectable thought formation. Unlike traditional AI that provides immediate answers, the Cognitive Engine:
- Generates multiple competing thoughts
- Deliberates and refines those thoughts
- Selects the best thought based on evaluation
- Provides confidence scores for answers
- Learns from experience over time

### How is it different from ChatGPT or other AI assistants?

Key differences:
- **Thought Process**: You can see the reasoning process, not just the final answer
- **Confidence Scores**: The engine tells you how certain it is about its answer
- **Learning**: It learns from interactions and improves over time
- **Transparency**: All cognitive processes are inspectable
- **Customization**: You can adjust how deeply it thinks

### What can I use it for?

Common use cases:
- Research and learning
- Decision making
- Creative writing
- Code assistance
- Problem solving
- Complex analysis
- Autonomous task execution (agent mode)

### Do I need programming knowledge?

**No** for basic usage. The interactive mode is designed for non-technical users. Programming knowledge is only needed for:
- Advanced configuration
- API integration
- Custom tool development
- Deployment

---

## Installation and Setup

### What are the system requirements?

**Minimum**:
- Python 3.9+
- 4 GB RAM
- 10 GB storage
- Internet connection for LLM APIs

**Recommended**:
- Python 3.10+
- 8 GB RAM
- 20 GB SSD storage
- Stable internet connection

### Do I need an API key?

Yes, you need at least one LLM provider API key:
- OpenAI API key (https://platform.openai.com/api-keys)
- Anthropic API key (https://console.anthropic.com/)

You can use either or both.

### Can I use it offline?

Partially. The core engine runs locally, but it requires internet access to call LLM APIs (OpenAI, Anthropic). Some features like the dashboard and agent tools (web search) also require internet.

### How do I install it?

```bash
# Clone the repository
git clone <repository-url>
cd cognitive_engine

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
python run.py
```

---

## Usage

### How do I ask a question?

In interactive mode:
```bash
python run.py
```

Then enter your question when prompted:
```
Enter your query: What is machine learning?
```

### What do the confidence scores mean?

- **0.8-1.0 (High)**: Very certain, can rely on the answer
- **0.5-0.8 (Medium)**: Reasonably certain but may have nuances
- **0.0-0.5 (Low)**: Uncertain, answer may be incomplete or speculative

### Why does it take longer than ChatGPT?

The Cognitive Engine deliberates on multiple thoughts before answering. This takes more time but produces more considered responses. You can reduce the time by:
- Lowering `MAX_ITERATIONS`
- Lowering `MIN_ITERATIONS`
- Setting `EARLY_STOP_CONFIDENCE` to a lower value

### Can I see how it reached its answer?

Yes! Enable reasoning traces:
```bash
ENABLE_REASONING_TRACE=true python run.py
```

Or use the Python API:
```python
result = engine.process("Your question")
print(result.reasoning_trace)
```

### How do I get faster responses?

Reduce iteration depth:
```bash
MIN_ITERATIONS=1 MAX_ITERATIONS=5 python run.py
```

Or use the faster LLM provider:
```bash
DEFAULT_LLM_PROVIDER=openai python run.py
```

### How do I get better quality answers?

Increase iteration depth:
```bash
MIN_ITERATIONS=5 MAX_ITERATIONS=50 python run.py
```

Or require higher confidence:
```bash
CONFIDENCE_THRESHOLD=0.9 python run.py
```

---

## Features

### What is the dashboard?

The dashboard is a real-time visualization of the cognitive process. It shows:
- Thought generation and relationships
- Memory growth and content
- Strategy shifts over time
- Deliberation evolution

Start it with:
```bash
python run.py dashboard
```

Access at `http://localhost:8000`

### What is agent mode?

Agent mode enables goal-directed autonomous behavior. The agent can:
- Accept high-level goals
- Create execution plans
- Use tools (web search, code execution)
- Learn from results
- Adapt its strategy

Start with:
```bash
python run.py agent
```

### What is the learning system?

The learning system extracts patterns from memory and converts them into rules. Over time, the engine:
- Recognizes recurring patterns in its reasoning
- Learns which strategies work best
- Applies learned rules to future queries
- Improves its performance

### Can I disable the learning system?

Yes:
```bash
ENABLE_LEARNING=false python run.py
```

### What is prompt evolution?

Prompt evolution is an experimental feature where the system:
- Suggests improvements to its own prompts
- Tests new prompts via A/B testing
- Adopts only validated improvements
- Can roll back if performance degrades

It's disabled by default. Enable with:
```bash
ENABLE_PROMPT_EVOLUTION=true python run.py
```

---

## Configuration

### How do I change the LLM provider?

Set the environment variable:
```bash
DEFAULT_LLM_PROVIDER=anthropic  # or 'openai'
```

Or in Python:
```python
from core.config import Config
config = Config(default_llm_provider="anthropic")
```

### What are the iteration limits?

- **MIN_ITERATIONS**: Minimum iterations before considering early stop (default: 3)
- **MAX_ITERATIONS**: Maximum iterations to prevent infinite loops (default: 50)

### What is the confidence threshold?

The minimum confidence required for acceptable output (default: 0.7). If no thought meets this threshold after MAX_ITERATIONS, the best available thought is used.

### How do I adjust the memory size?

Set the environment variable:
```bash
MAX_MEMORY_SIZE=10000
```

This limits the number of entries stored in memory.

---

## Memory and Learning

### Does it remember previous conversations?

Yes, it stores all interactions in its three-layer memory system:
- **Episodic Memory**: Raw events and interactions
- **Pattern Memory**: Recurring behaviors and structures
- **Rule Memory**: Learned strategies

### Can I clear the memory?

Yes:
```bash
# Clear all memory
rm cognitive_engine.db

# Or use the Python API
from core.memory import ThreeLayerMemory
memory = ThreeLayerMemory()
memory.clear_all()
```

### How do I access the memory?

```python
engine = CognitiveEngine()
memory = engine.get_memory()

episodic = memory.get_episodic_memory()
patterns = memory.get_pattern_memory()
rules = memory.get_rule_memory()
```

### Does learning happen automatically?

Yes, if enabled. The system:
- Extracts patterns every `LEARNING_INTERVAL` cycles
- Synthesizes rules from patterns
- Applies rules to future queries

You can control this with:
```bash
ENABLE_LEARNING=true
LEARNING_INTERVAL=100
```

---

## API and Integration

### Can I use it programmatically?

Yes, via the Python API:
```python
from core.engine import CognitiveEngine

engine = CognitiveEngine()
result = engine.process("Your question")
print(result.final_output)
```

### Is there a REST API?

Yes, you can create one using FastAPI:
```python
from fastapi import FastAPI
from core.engine import CognitiveEngine

app = FastAPI()
engine = CognitiveEngine()

@app.post("/query")
async def query(query: str):
    result = engine.process(query)
    return {"answer": result.final_output}
```

### Can I integrate it with my application?

Yes, see the [Integration Guide](Integration.md) for details.

### What programming languages are supported?

The engine is written in Python but can be integrated with any language via:
- REST API
- WebSocket
- Command-line interface
- Docker containers

---

## Troubleshooting

### The engine won't start

Check:
1. Python version is 3.9+
2. All dependencies installed: `pip install -r requirements.txt`
3. API keys are set in `.env`
4. Check logs: `tail -f cognitive_engine.log`

### I get "API key not found"

Ensure:
1. `.env` file exists in project root
2. API key is set: `OPENAI_API_KEY=your_key`
3. No spaces around `=` in `.env`
4. Environment variables are loaded

### It's too slow

Try:
1. Reduce iterations: `MAX_ITERATIONS=10`
2. Use faster provider: `DEFAULT_LLM_PROVIDER=openai`
3. Disable learning: `ENABLE_LEARNING=false`

### Memory usage is high

Try:
1. Limit memory: `MAX_MEMORY_SIZE=5000`
2. Enable cleanup: `ENABLE_MEMORY_CLEANUP=true`
3. Clear old data: `python run.py cleanup`

### Dashboard won't load

Check:
1. Dashboard enabled: `ENABLE_DASHBOARD=true`
2. Port not in use: `DASHBOARD_PORT=8000`
3. Browser console for errors
4. Firewall settings

For more issues, see the [Troubleshooting Guide](Troubleshooting.md).

---

## Cost and Pricing

### Does it cost money to use?

The Cognitive Engine itself is free (AGPL-3.0 license), but you pay for:
- LLM API calls (OpenAI, Anthropic)
- Your own infrastructure/hosting
- Any third-party services you use

### How much do LLM APIs cost?

It depends on usage:
- **OpenAI**: ~$0.002 per 1K tokens (GPT-3.5), ~$0.03 per 1K tokens (GPT-4)
- **Anthropic**: ~$0.008 per 1K tokens (Claude Instant), ~$0.03 per 1K tokens (Claude)

A typical query might use 1-5K tokens.

### Can I limit costs?

Yes:
- Use cheaper models (GPT-3.5 instead of GPT-4)
- Reduce iterations to minimize API calls
- Enable response caching
- Set usage alerts with your LLM provider

---

## Privacy and Security

### Is my data private?

Your data is processed locally and stored in your own database. However:
- Queries are sent to LLM providers (OpenAI, Anthropic)
- Check their privacy policies for details
- You can self-host LLMs for complete privacy

### Are my queries stored?

Yes, in the local memory database. You can:
- Disable learning: `ENABLE_LEARNING=false`
- Clear memory periodically
- Not store sensitive information

### Is it secure?

The engine includes security features:
- Input validation
- Output sanitization
- API key protection
- Secure default configurations

See the [Security Guide](Security.md) for details.

---

## Advanced Questions

### Can I add custom tools?

Yes, see the [Development Guide](Development.md) for details on creating custom tools.

### Can I modify the prompts?

Yes, you can customize layer-specific prompts in `llm/prompts.py`.

### Can I use my own LLM?

Yes, extend the LLM client in `llm/client.py` to support additional providers.

### Can I run it on multiple machines?

Yes, deploy using:
- Docker containers
- Kubernetes
- Cloud services (AWS, GCP, Azure)

See the [Deployment Guide](Deployment.md) for details.

---

## Comparison with Other Systems

### How does it compare to LangChain?

The Cognitive Engine is more focused on explicit thought formation and deliberation, while LangChain is a framework for building LLM applications. They can be complementary.

### How does it compare to AutoGPT?

Both support autonomous agents, but the Cognitive Engine has more sophisticated cognitive modeling, memory systems, and meta-cognition.

### How does it compare to standard ChatGPT?

The Cognitive Engine shows its reasoning process, provides confidence scores, and learns over time. ChatGPT is faster but less transparent.

---

## Support

### Where can I get help?

- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- **Documentation**: Check the wiki
- **GitHub Issues**: Report bugs there

### How do I report a bug?

1. Check existing issues
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Log excerpts

### How do I request a feature?

1. Check existing feature requests
2. Create a new issue with:
   - Feature description
   - Use case
   - Proposed implementation (if known)

### How do I contribute?

See the [Development Guide](Development.md) for contributing guidelines.

---

## License

### What license is it under?

AGPL-3.0 (GNU Affero General Public License)

### What does AGPL-3.0 mean?

- You can use, modify, and distribute the software
- You must provide source code for any modifications
- If you run it as a network service, users must have access to the source
- You must include the license and copyright notice

### Can I use it commercially?

Yes, but you must:
- Provide source code for any modifications
- Make the source available to users of network services
- Include attribution

### Can I use it in a proprietary product?

Only if you provide source code for any modifications and make it available to users of the network service. For purely proprietary use, consider a commercial license agreement.

---

## Miscellaneous

### What's the roadmap?

Future planned features:
- Improved learning algorithms
- More tool integrations
- Better visualization
- Performance optimizations
- Additional LLM provider support

### Is there a community?

Join our community for:
- Discussions
- Feature requests
- Bug reports
- Collaboration opportunities

### How often is it updated?

Release frequency depends on:
- Bug fixes (as needed)
- Feature development (ongoing)
- Security updates (immediate)

### Can I sponsor development?

Yes! Contact us at autobotsolution@gmail.com for sponsorship opportunities.

### Where can I learn more?

- [Architecture Documentation](Architecture.md)
- [API Reference](API-Reference.md)
- [User Guide](User-Guide.md)
- [Development Guide](Development.md)
