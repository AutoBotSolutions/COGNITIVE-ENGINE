# Performance Tuning Guide

This guide covers optimizing the Cognitive Engine for performance and efficiency.

## Table of Contents

- [Performance Overview](#performance-overview)
- [Configuration Optimization](#configuration-optimization)
- [LLM Provider Optimization](#llm-provider-optimization)
- [Memory Optimization](#memory-optimization)
- [Caching Strategies](#caching-strategies)
- [Concurrency and Async](#concurrency-and-async)
- [Database Optimization](#database-optimization)
- [Resource Management](#resource-management)
- [Monitoring and Profiling](#monitoring-and-profiling)
- [Scaling Strategies](#scaling-strategies)

---

## Performance Overview

### Performance Bottlenecks

Common performance bottlenecks in the Cognitive Engine:

1. **LLM API Calls**: Network latency and provider response time
2. **Cognitive Iterations**: Multiple iterations increase processing time
3. **Memory Operations**: Database queries and memory lookups
4. **Dashboard Streaming**: WebSocket overhead for real-time updates
5. **Learning Operations**: Pattern extraction and rule synthesis

### Performance Metrics

Key metrics to monitor:

- **Response Time**: Time from query to answer
- **Iteration Count**: Number of cognitive iterations
- **API Call Count**: Number of LLM API calls
- **Memory Usage**: RAM consumption
- **CPU Usage**: Processor utilization
- **Database Query Time**: Time for memory operations

### Baseline Performance

Typical performance on recommended hardware (4 CPU, 8 GB RAM):

- Simple query: 5-15 seconds
- Complex query: 15-60 seconds
- Agent task: 1-5 minutes
- Memory growth: ~1 KB per query

---

## Configuration Optimization

### Iteration Tuning

Adjust iteration limits based on use case:

```bash
# Fast responses (speed over quality)
MIN_ITERATIONS=1
MAX_ITERATIONS=5
EARLY_STOP_CONFIDENCE=0.8

# Balanced (default)
MIN_ITERATIONS=3
MAX_ITERATIONS=50
EARLY_STOP_CONFIDENCE=0.95

# Deep thinking (quality over speed)
MIN_ITERATIONS=5
MAX_ITERATIONS=100
EARLY_STOP_CONFIDENCE=0.98
```

### Confidence Thresholds

Set appropriate confidence thresholds:

```bash
# Accept lower confidence for faster responses
CONFIDENCE_THRESHOLD=0.6

# Default balanced threshold
CONFIDENCE_THRESHOLD=0.7

# Require high confidence
CONFIDENCE_THRESHOLD=0.9
```

### Feature Toggles

Disable unused features to improve performance:

```bash
# Disable dashboard for CLI-only usage
ENABLE_DASHBOARD=false

# Disable learning for one-time queries
ENABLE_LEARNING=false

# Disable prompt evolution (experimental)
ENABLE_PROMPT_EVOLUTION=false

# Disable reasoning traces
ENABLE_REASONING_TRACE=false
```

---

## LLM Provider Optimization

### Provider Selection

Choose the right provider for your needs:

```bash
# OpenAI (generally faster)
DEFAULT_LLM_PROVIDER=openai

# Anthropic (often more nuanced)
DEFAULT_LLM_PROVIDER=anthropic
```

### Model Selection

Use appropriate models for different tasks:

```python
# For simple tasks (faster, cheaper)
DEFAULT_MODEL=gpt-3.5-turbo

# For complex tasks (slower, more capable)
DEFAULT_MODEL=gpt-4

# For code tasks
DEFAULT_MODEL=gpt-4
```

### API Call Optimization

Minimize API calls:

```python
# Batch similar queries
queries = ["What is X?", "Explain X", "X examples"]
# Process together to benefit from context

# Use context efficiently
# Provide comprehensive context in single query
# rather than multiple follow-ups
```

### Response Caching

Cache LLM responses to avoid repeated calls:

```python
import redis
import hashlib
import json

class LLMCache:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.ttl = 3600  # 1 hour
    
    def get_cache_key(self, prompt, provider, model):
        key_data = f"{prompt}:{provider}:{model}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def get(self, prompt, provider, model):
        key = self.get_cache_key(prompt, provider, model)
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None
    
    def set(self, prompt, provider, model, response):
        key = self.get_cache_key(prompt, provider, model)
        self.redis.setex(key, self.ttl, json.dumps(response))

# Use in LLM client
cache = LLMCache()
cached = cache.get(prompt, provider, model)
if cached:
    return cached
response = llm_client.generate(prompt)
cache.set(prompt, provider, model, response)
return response
```

---

## Memory Optimization

### Memory Size Limits

Control memory growth:

```bash
# Reduce memory footprint
MAX_MEMORY_SIZE=5000

# Increase for learning-heavy use
MAX_MEMORY_SIZE=20000
```

### Memory Cleanup

Implement periodic cleanup:

```python
from datetime import datetime, timedelta

def cleanup_old_memory():
    """Remove old episodic memory entries."""
    cutoff = datetime.now() - timedelta(days=30)
    memory.db.query(EpisodicMemory).filter(
        EpisodicMemory.created_at < cutoff
    ).delete()
```

### Memory Indexing

Add indexes for faster queries:

```python
# In database initialization
# Add indexes on frequently queried fields
CREATE INDEX idx_timestamp ON episodic_memory(timestamp);
CREATE INDEX idx_type ON episodic_memory(type);
CREATE INDEX idx_confidence ON thoughts(confidence);
```

### Memory Compression

Compress large memory entries:

```python
import gzip
import pickle

def compress_data(data):
    """Compress data before storage."""
    serialized = pickle.dumps(data)
    compressed = gzip.compress(serialized)
    return compressed

def decompress_data(compressed):
    """Decompress data after retrieval."""
    decompressed = gzip.decompress(compressed)
    return pickle.loads(decompressed)
```

---

## Caching Strategies

### Thought Graph Caching

Cache thought graph queries:

```python
from functools import lru_cache

class ThoughtGraph:
    @lru_cache(maxsize=1000)
    def get_thought(self, thought_id):
        return self.thoughts.get(thought_id)
    
    @lru_cache(maxsize=100)
    def get_related(self, thought_id):
        return [self.thoughts[t] for t in self.relationships.get(thought_id, [])]
```

### Pattern Caching

Cache extracted patterns:

```python
class PatternMemory:
    def __init__(self):
        self.pattern_cache = {}
        self.cache_ttl = 3600
    
    def get_patterns(self, force_refresh=False):
        cache_key = "all_patterns"
        
        if not force_refresh and cache_key in self.pattern_cache:
            cached_time, patterns = self.pattern_cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                return patterns
        
        patterns = self.extract_patterns()
        self.pattern_cache[cache_key] = (time.time(), patterns)
        return patterns
```

### Rule Caching

Cache rule application results:

```python
class RuleMemory:
    @lru_cache(maxsize=500)
    def apply_rule(self, rule_id, state_hash):
        rule = self.rules[rule_id]
        return rule.apply(state_hash)
```

### HTTP Caching

For web interfaces:

```python
from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

@app.get("/query")
async def query():
    response = Response()
    response.headers["Cache-Control"] = "public, max-age=300"
    return response
```

---

## Concurrency and Async

### Async I/O

Use async for network operations:

```python
import asyncio
import aiohttp

class AsyncLLMClient:
    async def generate_async(self, prompt):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                json={"prompt": prompt}
            ) as response:
                return await response.json()
```

### Concurrent Processing

Process multiple thoughts concurrently:

```python
async def deliberate_concurrently(thoughts):
    """Deliberate on multiple thoughts concurrently."""
    tasks = [self.deliberate_single(thought) for thought in thoughts]
    results = await asyncio.gather(*tasks)
    return results
```

### Connection Pooling

Pool database connections:

```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'sqlite:///cognitive_engine.db',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### Thread Pool

Use thread pools for CPU-bound tasks:

```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

def process_thoughts(thoughts):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(score_thought, thoughts))
    return results
```

---

## Database Optimization

### SQLite Optimization

Optimize SQLite settings:

```python
import sqlite3

conn = sqlite3.connect('cognitive_engine.db')
conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency
conn.execute("PRAGMA synchronous=NORMAL")  # Faster writes
conn.execute("PRAGMA cache_size=10000")  # Larger cache
conn.execute("PRAGMA temp_store=MEMORY")  # Memory for temp tables
```

### Query Optimization

Optimize common queries:

```python
# Use indexes
CREATE INDEX idx_timestamp ON episodic_memory(timestamp);

# Use prepared statements
stmt = "SELECT * FROM thoughts WHERE confidence > ?"
cursor.execute(stmt, (0.7,))

# Batch operations
# Instead of multiple INSERTs
for item in items:
    cursor.execute("INSERT...", item)

# Use executemany
cursor.executemany("INSERT...", items)
```

### Database Vacuum

Periodically vacuum the database:

```bash
# In maintenance script
sqlite3 cognitive_engine.db "VACUUM;"
```

### Connection Management

Manage database connections efficiently:

```python
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = sqlite3.connect('cognitive_engine.db')
    try:
        yield conn
    finally:
        conn.close()

# Usage
with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM thoughts")
```

---

## Resource Management

### Memory Profiling

Profile memory usage:

```python
import tracemalloc

tracemalloc.start()

# Run your code
engine.process("Your query")

# Get snapshot
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

### CPU Profiling

Profile CPU usage:

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

engine.process("Your query")

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

### Resource Limits

Set resource limits:

```python
import resource

# Limit memory to 2GB
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024 * 1024 * 1024, -1))

# Limit CPU time
resource.setrlimit(resource.RLIMIT_CPU, (300, 300))  # 5 minutes
```

### Garbage Collection

Manage garbage collection:

```python
import gc

# Force garbage collection
gc.collect()

# Adjust collection frequency
gc.set_threshold(700, 10, 5)
```

---

## Monitoring and Profiling

### Performance Monitoring

Monitor key metrics:

```python
import time
from prometheus_client import Counter, Histogram

# Metrics
query_duration = Histogram('query_duration_seconds')
iteration_count = Histogram('iteration_count')
api_calls = Counter('api_calls_total')

# Usage
start = time.time()
result = engine.process(query)
duration = time.time() - start
query_duration.observe(duration)
iteration_count.observe(result.iteration_count)
```

### Logging Performance

Log performance data:

```python
import logging

logger = logging.getLogger('performance')

def log_performance(query, result, duration):
    logger.info({
        'query': query[:50],
        'duration': duration,
        'iterations': result.iteration_count,
        'confidence': result.confidence,
        'timestamp': datetime.now().isoformat()
    })
```

### Dashboard Metrics

Display performance metrics in dashboard:

```python
# Add to dashboard events
class PerformanceEvent:
    def __init__(self, metric_name, value):
        self.metric_name = metric_name
        self.value = value
        self.timestamp = datetime.now()

# Stream to dashboard
dashboard_streamer.stream_event(PerformanceEvent('response_time', duration))
```

### Alerting

Set up performance alerts:

```python
def check_performance(duration):
    if duration > 60:  # 60 seconds
        alert("Slow query detected", f"Duration: {duration}s")
```

---

## Scaling Strategies

### Horizontal Scaling

Run multiple instances:

```yaml
# docker-compose.yml
services:
  cognitive-engine:
    image: cognitive-engine:latest
    deploy:
      replicas: 3
    environment:
      - ENABLE_DASHBOARD=false
```

### Load Balancing

Use a load balancer:

```nginx
upstream cognitive_engine {
    server 10.0.0.1:8000;
    server 10.0.0.2:8000;
    server 10.0.0.3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://cognitive_engine;
    }
}
```

### Vertical Scaling

Increase resources:

```yaml
# Kubernetes
resources:
  limits:
    cpu: "4"
    memory: 8Gi
  requests:
    cpu: "2"
    memory: 4Gi
```

### Database Scaling

Use PostgreSQL for high load:

```python
# Switch from SQLite to PostgreSQL
DATABASE_URL=postgresql://user:pass@localhost/cognitive_engine

# Use connection pooling
from sqlalchemy.pool import QueuePool
engine = create_engine(DATABASE_URL, pool_size=20)
```

---

## Specific Optimization Scenarios

### High-Throughput Scenario

For processing many queries quickly:

```bash
# Configuration
MIN_ITERATIONS=1
MAX_ITERATIONS=5
ENABLE_LEARNING=false
ENABLE_DASHBOARD=false
ENABLE_REASONING_TRACE=false
DEFAULT_LLM_PROVIDER=openai
DEFAULT_MODEL=gpt-3.5-turbo
```

### High-Quality Scenario

For maximum quality regardless of speed:

```bash
# Configuration
MIN_ITERATIONS=5
MAX_ITERATIONS=100
EARLY_STOP_CONFIDENCE=0.98
CONFIDENCE_THRESHOLD=0.9
ENABLE_LEARNING=true
DEFAULT_LLM_PROVIDER=openai
DEFAULT_MODEL=gpt-4
```

### Cost-Optimized Scenario

For minimizing LLM costs:

```bash
# Configuration
MIN_ITERATIONS=1
MAX_ITERATIONS=10
ENABLE_RESPONSE_CACHE=true
CACHE_TTL=86400
DEFAULT_LLM_PROVIDER=openai
DEFAULT_MODEL=gpt-3.5-turbo
```

### Memory-Constrained Scenario

For systems with limited RAM:

```bash
# Configuration
MAX_MEMORY_SIZE=1000
ENABLE_MEMORY_CLEANUP=true
MEMORY_RETENTION_DAYS=7
ENABLE_LEARNING=false
```

---

## Performance Testing

### Load Testing

Test with concurrent load:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def load_test(queries, concurrency=10):
    """Test system under concurrent load."""
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        results = list(executor.map(process_query, queries))
    return results

queries = ["Query " + str(i) for i in range(100)]
load_test(queries, concurrency=10)
```

### Benchmarking

Establish performance baselines:

```python
import time

def benchmark():
    """Run benchmark tests."""
    test_queries = [
        "What is AI?",
        "Explain machine learning",
        "Compare Python and JavaScript"
    ]
    
    for query in test_queries:
        times = []
        for _ in range(5):
            start = time.time()
            engine.process(query)
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        print(f"{query}: {avg_time:.2f}s average")
```

### Performance Regression Testing

Detect performance regressions:

```python
def check_regression(current_baseline, historical_baseline, threshold=0.2):
    """Check if performance has regressed."""
    if current_baseline > historical_baseline * (1 + threshold):
        raise PerformanceRegressionError(
            f"Performance regression detected: {current_baseline:.2f}s "
            f"vs baseline {historical_baseline:.2f}s"
        )
```

---

## Troubleshooting Performance Issues

### Slow Response Times

**Symptoms**: Queries taking too long

**Diagnosis**:
```python
# Profile to find bottleneck
import cProfile
cProfile.run('engine.process("query")')
```

**Solutions**:
- Reduce iterations
- Use faster LLM provider
- Enable caching
- Disable unused features

### High Memory Usage

**Symptoms**: Memory growing continuously

**Diagnosis**:
```python
import tracemalloc
tracemalloc.start()
# Run operations
snapshot = tracemalloc.take_snapshot()
snapshot.statistics('lineno')
```

**Solutions**:
- Reduce MAX_MEMORY_SIZE
- Enable memory cleanup
- Clear old data
- Check for memory leaks

### High CPU Usage

**Symptoms**: CPU near 100%

**Diagnosis**:
```bash
top -p <PID>
```

**Solutions**:
- Reduce concurrency
- Optimize database queries
- Use async operations
- Profile CPU-intensive functions

### Database Slowdowns

**Symptoms**: Memory operations slow

**Diagnosis**:
```python
import time
start = time.time()
memory.get_episodic_memory()
print(f"Query took {time.time() - start:.2f}s")
```

**Solutions**:
- Add indexes
- Use WAL mode
- Increase cache size
- Vacuum database
- Consider PostgreSQL

---

## Best Practices

1. **Profile Before Optimizing**
   - Measure before making changes
   - Identify actual bottlenecks
   - Focus on high-impact optimizations

2. **Use Appropriate Configurations**
   - Match configuration to use case
   - Don't over-optimize for simple tasks
   - Balance speed vs quality

3. **Monitor Continuously**
   - Track performance metrics
   - Set up alerts for degradation
   - Review performance regularly

4. **Test After Changes**
   - Verify optimizations work
   - Check for regressions
   - Benchmark improvements

5. **Document Optimizations**
   - Record what works
   - Share with team
   - Maintain performance baseline

---

## Support

For performance issues:
- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- Check logs: `cognitive_engine.log`
- Review this guide
- Use profiling tools to identify bottlenecks
