# Examples and Tutorials

Practical examples and tutorials for using the Cognitive Engine.

## Table of Contents

- [Quick Start Examples](#quick-start-examples)
- [Python API Examples](#python-api-examples)
- [Web Application Examples](#web-application-examples)
- [Agent Mode Examples](#agent-mode-examples)
- [Custom Tool Examples](#custom-tool-examples)
- [Integration Examples](#integration-examples)
- [Advanced Examples](#advanced-examples)

---

## Quick Start Examples

### Basic Query

Process a simple query:

```python
from core.engine import CognitiveEngine

engine = CognitiveEngine()
result = engine.process("What is artificial intelligence?")

print(f"Answer: {result.final_output}")
print(f"Confidence: {result.confidence}")
print(f"Iterations: {result.iteration_count}")
```

### Query with Custom Configuration

Use custom iteration settings:

```python
from core.config import Config
from core.engine import CognitiveEngine

config = Config(
    min_iterations=5,
    max_iterations=20,
    confidence_threshold=0.8
)

engine = CognitiveEngine(config)
result = engine.process("Explain quantum computing")
```

### Accessing Thought Graph

Inspect the reasoning process:

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
    print(f"Weaknesses: {thought.weaknesses}")
    print("---")
```

### Using Memory

Access learned patterns and rules:

```python
from core.engine import CognitiveEngine

engine = CognitiveEngine()

# Process multiple queries to build memory
engine.process("What is machine learning?")
engine.process("How do neural networks work?")
engine.process("What is deep learning?")

# Access memory
memory = engine.get_memory()
episodic = memory.get_episodic_memory()
patterns = memory.get_pattern_memory()
rules = memory.get_rule_memory()

print(f"Episodic entries: {len(episodic)}")
print(f"Patterns found: {len(patterns)}")
print(f"Rules learned: {len(rules)}")
```

---

## Python API Examples

### Batch Processing

Process multiple queries efficiently:

```python
from core.engine import CognitiveEngine

def process_batch(queries):
    """Process multiple queries."""
    engine = CognitiveEngine()
    results = []
    
    for query in queries:
        result = engine.process(query)
        results.append({
            'query': query,
            'answer': result.final_output,
            'confidence': result.confidence,
            'iterations': result.iteration_count
        })
    
    return results

queries = [
    "What is Python?",
    "What is JavaScript?",
    "What is Rust?",
    "What is Go?"
]

results = process_batch(queries)
for r in results:
    print(f"{r['query']}: {r['confidence']:.2f}")
```

### Async Processing

Process queries asynchronously:

```python
import asyncio
from core.engine import CognitiveEngine
from concurrent.futures import ThreadPoolExecutor

async def process_async(query):
    """Process query asynchronously."""
    loop = asyncio.get_event_loop()
    engine = CognitiveEngine()
    
    with ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, engine.process, query)
    
    return result

async def process_batch_async(queries):
    """Process multiple queries concurrently."""
    tasks = [process_async(q) for q in queries]
    results = await asyncio.gather(*tasks)
    return results

queries = ["Query 1", "Query 2", "Query 3"]
results = asyncio.run(process_batch_async(queries))
```

### Custom Scoring

Implement custom thought scoring:

```python
from utils.scoring import ThoughtScorer

class CustomScorer(ThoughtScorer):
    """Custom scoring function."""
    
    def score_thought(self, thought):
        """Score thought with custom logic."""
        base_score = super().score_thought(thought)
        
        # Bonus for thoughts with examples
        if "example" in thought.premise.lower():
            base_score += 0.1
        
        # Bonus for practical thoughts
        if "practical" in thought.premise.lower():
            base_score += 0.05
        
        return min(base_score, 1.0)

# Use custom scorer
engine = CognitiveEngine()
engine.deliberator.scorer = CustomScorer()
result = engine.process("Your query")
```

### Error Handling

Handle errors gracefully:

```python
from core.engine import CognitiveEngine

engine = CognitiveEngine()

try:
    result = engine.process("Your query")
    print(f"Success: {result.final_output}")
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    # Log error
    import logging
    logging.error(f"Error processing query: {e}")
```

---

## Web Application Examples

### Flask API

Create a simple Flask API:

```python
from flask import Flask, request, jsonify
from core.engine import CognitiveEngine

app = Flask(__name__)
engine = CognitiveEngine()

@app.route('/query', methods=['POST'])
def query():
    """Process a query."""
    data = request.json
    query = data.get('query')
    
    result = engine.process(query)
    
    return jsonify({
        'answer': result.final_output,
        'confidence': result.confidence,
        'iterations': result.iteration_count
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check."""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### FastAPI with WebSocket

Create a FastAPI app with WebSocket support:

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from core.engine import CognitiveEngine

app = FastAPI()
engine = CognitiveEngine()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def process_query(request: QueryRequest):
    """Process a query."""
    result = engine.process(request.query)
    return {
        "answer": result.final_output,
        "confidence": result.confidence
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            result = engine.process(data)
            await websocket.send_json({
                "answer": result.final_output,
                "confidence": result.confidence
            })
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### React Frontend

Create a React component to interact with the API:

```javascript
import React, { useState } from 'react';

function CognitiveEngine() {
    const [query, setQuery] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        
        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            
            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Enter your query"
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Processing...' : 'Submit'}
                </button>
            </form>
            
            {result && (
                <div>
                    <h3>Answer:</h3>
                    <p>{result.answer}</p>
                    <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
                </div>
            )}
        </div>
    );
}

export default CognitiveEngine;
```

---

## Agent Mode Examples

### Simple Agent Task

Run a simple agent task:

```python
from agent.agent import Agent

agent = Agent()
result = agent.run("What is 2+2?")

print(f"Goal achieved: {result.goal_achieved}")
print(f"Actions taken: {len(result.actions_taken)}")
print(f"Final state: {result.final_state}")
```

### Research Agent

Create an agent for research tasks:

```python
from agent.agent import Agent

agent = Agent()
result = agent.run(
    "Research the latest developments in AI and "
    "summarize the key findings"
)

print(f"Research completed: {result.goal_achieved}")
print(f"Time taken: {result.execution_time}")
```

### Agent with Custom Tools

Add custom tools to the agent:

```python
from agent.agent import Agent
from tools.registry import ToolRegistry
from tools.web_search import WebSearchTool

# Register custom tool
registry = ToolRegistry()
registry.register_tool(WebSearchTool())

# Create agent with custom tools
agent = Agent(tool_registry=registry)
result = agent.run("Search for information about Python")
```

### Multi-Step Agent

Agent with complex multi-step planning:

```python
from agent.agent import Agent

agent = Agent()
result = agent.run(
    "Analyze the pros and cons of using Python vs JavaScript "
    "for web development, then provide a recommendation"
)

print(f"Steps taken: {len(result.actions_taken)}")
for action in result.actions_taken:
    print(f"  - {action.description}")
```

---

## Custom Tool Examples

### Simple Custom Tool

Create a simple custom tool:

```python
from tools.registry import Tool

class CalculatorTool(Tool):
    """A simple calculator tool."""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Perform basic calculations"
        )
    
    def execute(self, params):
        """Execute calculation."""
        operation = params.get('operation')
        a = params.get('a')
        b = params.get('b')
        
        if operation == 'add':
            result = a + b
        elif operation == 'subtract':
            result = a - b
        elif operation == 'multiply':
            result = a * b
        elif operation == 'divide':
            result = a / b
        else:
            return {'success': False, 'error': 'Unknown operation'}
        
        return {
            'success': True,
            'result': result,
            'operation': operation
        }

# Register the tool
from tools.registry import tool_registry
tool_registry.register_tool(CalculatorTool())
```

### API Tool

Create a tool that calls an external API:

```python
import requests

class WeatherTool(Tool):
    """Tool for getting weather information."""
    
    def __init__(self, api_key):
        super().__init__(
            name="weather",
            description="Get current weather for a location"
        )
        self.api_key = api_key
    
    def execute(self, params):
        """Get weather for location."""
        location = params.get('location')
        
        url = f"http://api.weatherapi.com/v1/current.json"
        response = requests.get(url, params={
            'key': self.api_key,
            'q': location
        })
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'location': location,
                'temperature': data['current']['temp_c'],
                'condition': data['current']['condition']['text']
            }
        else:
            return {
                'success': False,
                'error': 'Failed to fetch weather'
            }
```

### File Operation Tool

Create a tool for file operations:

```python
import os

class FileReaderTool(Tool):
    """Tool for reading files."""
    
    def __init__(self, base_path="/safe/directory"):
        super().__init__(
            name="file_reader",
            description="Read files from a safe directory"
        )
        self.base_path = base_path
    
    def execute(self, params):
        """Read a file."""
        filename = params.get('filename')
        
        # Security: ensure file is in base directory
        full_path = os.path.join(self.base_path, filename)
        if not os.path.abspath(full_path).startswith(self.base_path):
            return {
                'success': False,
                'error': 'Access denied: file outside safe directory'
            }
        
        try:
            with open(full_path, 'r') as f:
                content = f.read()
            
            return {
                'success': True,
                'filename': filename,
                'content': content,
                'size': len(content)
            }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'File not found'
            }
```

---

## Integration Examples

### Database Integration

Store results in a database:

```python
import sqlite3
from core.engine import CognitiveEngine

def store_result(query, result):
    """Store result in database."""
    conn = sqlite3.connect('results.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO results 
        (query, answer, confidence, iterations, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        query,
        result.final_output,
        result.confidence,
        result.iteration_count,
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()

# Usage
engine = CognitiveEngine()
result = engine.process("What is AI?")
store_result("What is AI?", result)
```

### Message Queue Integration

Process queries from a message queue:

```python
import pika
from core.engine import CognitiveEngine

def process_from_queue():
    """Process queries from RabbitMQ."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()
    
    channel.queue_declare(queue='cognitive_queries')
    
    engine = CognitiveEngine()
    
    def callback(ch, method, properties, body):
        query = body.decode('utf-8')
        result = engine.process(query)
        
        # Send response
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id
            ),
            body=str(result.final_output)
        )
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_consume(
        queue='cognitive_queries',
        on_message_callback=callback
    )
    
    print('Waiting for messages...')
    channel.start_consuming()
```

### Celery Integration

Use Celery for distributed processing:

```python
# tasks.py
from celery import Celery
from core.engine import CognitiveEngine

app = Celery('cognitive_tasks', broker='redis://localhost:6379')

@app.task
def process_query_task(query):
    """Celery task for processing queries."""
    engine = CognitiveEngine()
    result = engine.process(query)
    return {
        'answer': result.final_output,
        'confidence': result.confidence,
        'iterations': result.iteration_count
    }

# Usage
from tasks import process_query_task
result = process_query_task.delay("What is AI?")
```

---

## Advanced Examples

### Custom Cognitive Layer

Create a custom cognitive layer:

```python
from layers.deliberator import Deliberator

class CustomDeliberator(Deliberator):
    """Custom deliberation layer with special logic."""
    
    def deliberate(self, thoughts):
        """Custom deliberation logic."""
        # Add custom preprocessing
        thoughts = self.preprocess_thoughts(thoughts)
        
        # Call parent deliberation
        evolved = super().deliberate(thoughts)
        
        # Add custom postprocessing
        evolved = self.postprocess_thoughts(evolved)
        
        return evolved
    
    def preprocess_thoughts(self, thoughts):
        """Custom preprocessing."""
        # Your custom logic
        return thoughts
    
    def postprocess_thoughts(self, thoughts):
        """Custom postprocessing."""
        # Your custom logic
        return thoughts

# Use custom layer
engine = CognitiveEngine()
engine.deliberator = CustomDeliberator()
```

### Memory Customization

Customize memory behavior:

```python
from core.memory import ThreeLayerMemory

class CustomMemory(ThreeLayerMemory):
    """Custom memory with special features."""
    
    def store_episodic(self, event):
        """Custom episodic storage."""
        # Add custom metadata
        event['custom_metadata'] = "custom_value"
        
        # Call parent method
        super().store_episodic(event)
    
    def extract_patterns(self):
        """Custom pattern extraction."""
        patterns = super().extract_patterns()
        
        # Add custom pattern filtering
        filtered = [p for p in patterns if p.frequency > 3]
        
        return filtered

# Use custom memory
engine = CognitiveEngine()
engine.memory = CustomMemory()
```

### Prompt Customization

Customize LLM prompts:

```python
from llm.prompts import PromptTemplates

templates = PromptTemplates()

# Customize generator prompt
templates.generator_prompt = """
You are an expert in {topic}. 
Provide detailed, accurate information about {query}.
Focus on practical applications and examples.
"""

# Customize deliberator prompt
templates.deliberator_prompt = """
Critically evaluate the following thought:
{thought}

Consider:
- Accuracy
- Completeness
- Practicality
- Clarity

Provide specific feedback and suggestions for improvement.
"""

# Use custom prompts
engine = CognitiveEngine()
engine.generator.prompt_templates = templates
```

### Multi-Engine Setup

Run multiple engine instances:

```python
from core.engine import CognitiveEngine
from core.config import Config

# Fast engine for quick queries
fast_config = Config(
    min_iterations=1,
    max_iterations=5,
    confidence_threshold=0.6
)
fast_engine = CognitiveEngine(fast_config)

# Quality engine for important queries
quality_config = Config(
    min_iterations=5,
    max_iterations=50,
    confidence_threshold=0.9
)
quality_engine = CognitiveEngine(quality_config)

def process_query(query, importance='normal'):
    """Route query to appropriate engine."""
    if importance == 'high':
        return quality_engine.process(query)
    else:
        return fast_engine.process(query)
```

### Streaming Results

Stream results as they're generated:

```python
import asyncio
from core.engine import CognitiveEngine

async def stream_process(engine, query):
    """Stream processing results."""
    # Override to yield intermediate results
    for iteration in range(10):
        # Process one iteration
        result = engine.process(query)
        
        # Yield intermediate result
        yield {
            'iteration': iteration + 1,
            'confidence': result.confidence,
            'partial_answer': result.final_output
        }

# Usage
async def main():
    engine = CognitiveEngine()
    
    async for update in stream_process(engine, "Your query"):
        print(f"Iteration {update['iteration']}: {update['confidence']:.2f}")

asyncio.run(main())
```

---

## Tutorial: Building a Research Assistant

### Step 1: Setup

```python
from core.engine import CognitiveEngine
from agent.agent import Agent
from tools.web_search import WebSearchTool

# Initialize engine and agent
engine = CognitiveEngine()
agent = Agent()

# Register web search tool
from tools.registry import tool_registry
tool_registry.register_tool(WebSearchTool())
```

### Step 2: Research Function

```python
def research_topic(topic):
    """Research a topic comprehensively."""
    
    # Step 1: Get overview
    overview = engine.process(f"What is {topic}?")
    print(f"Overview: {overview.final_output}\n")
    
    # Step 2: Search for recent developments
    agent_goal = f"Search for recent developments in {topic}"
    agent_result = agent.run(agent_goal)
    print(f"Recent developments found\n")
    
    # Step 3: Analyze findings
    analysis = engine.process(
        f"Analyze the key developments in {topic} "
        f"and identify the most important trends"
    )
    print(f"Analysis: {analysis.final_output}\n")
    
    # Step 4: Synthesize summary
    summary = engine.process(
        f"Based on the overview and analysis, provide a "
        f"comprehensive summary of {topic} with key takeaways"
    )
    print(f"Summary: {summary.final_output}\n")
    
    return {
        'overview': overview.final_output,
        'analysis': analysis.final_output,
        'summary': summary.final_output
    }
```

### Step 3: Use the Assistant

```python
# Research a topic
results = research_topic("quantum computing")

# Save results
with open('quantum_computing_research.txt', 'w') as f:
    f.write(f"Overview:\n{results['overview']}\n\n")
    f.write(f"Analysis:\n{results['analysis']}\n\n")
    f.write(f"Summary:\n{results['summary']}\n")
```

---

## Tutorial: Creating a Chatbot

### Step 1: Setup Flask App

```python
from flask import Flask, request, jsonify, render_template_string
from core.engine import CognitiveEngine

app = Flask(__name__)
engine = CognitiveEngine()

# Store conversation history
conversations = {}
```

### Step 2: Chat Endpoint

```python
@app.route('/chat', methods=['POST'])
def chat():
    """Process chat message."""
    data = request.json
    session_id = data.get('session_id')
    message = data.get('message')
    
    # Get conversation history
    history = conversations.get(session_id, [])
    
    # Build context from history
    context = "\n".join([f"User: {h['user']}\nAI: {h['ai']}" for h in history[-5:]])
    
    # Process with context
    full_query = f"Context:\n{context}\n\nCurrent message: {message}"
    result = engine.process(full_query)
    
    # Store in history
    history.append({'user': message, 'ai': result.final_output})
    conversations[session_id] = history
    
    return jsonify({
        'response': result.final_output,
        'confidence': result.confidence
    })
```

### Step 3: Web Interface

```python
@app.route('/')
def index():
    """Serve chat interface."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cognitive Chat</title>
    </head>
    <body>
        <div id="chat"></div>
        <input type="text" id="message" placeholder="Type a message">
        <button onclick="sendMessage()">Send</button>
        <script>
            let sessionId = Math.random().toString(36).substring(7);
            
            async function sendMessage() {
                const message = document.getElementById('message').value;
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({session_id: sessionId, message})
                });
                const data = await response.json();
                
                document.getElementById('chat').innerHTML += 
                    `<p>User: ${message}</p><p>AI: ${data.response}</p>`;
                document.getElementById('message').value = '';
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)
```

### Step 4: Run the Chatbot

```python
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## Tutorial: Data Analysis Assistant

### Step 1: Setup

```python
from core.engine import CognitiveEngine
import pandas as pd

engine = CognitiveEngine()
```

### Step 2: Load Data

```python
def analyze_dataset(data_path):
    """Analyze a dataset with cognitive assistance."""
    
    # Load dataset
    df = pd.read_csv(data_path)
    
    # Get basic info
    info = engine.process(
        f"Analyze this dataset with {len(df)} rows and {len(df.columns)} columns. "
        f"Columns: {', '.join(df.columns)}. "
        f"What kind of analysis would be appropriate?"
    )
    
    print(f"Analysis suggestion: {info.final_output}\n")
    
    return info
```

### Step 3: Ask Questions

```python
def ask_about_data(df, question):
    """Ask a question about the data."""
    
    # Provide context about data
    context = f"""
    Dataset has {len(df)} rows and {len(df.columns)} columns.
    Columns: {', '.join(df.columns)}.
    Sample data:
    {df.head().to_string()}
    """
    
    full_query = f"{context}\n\nQuestion: {question}"
    result = engine.process(full_query)
    
    return result.final_output
```

### Step 4: Generate Insights

```python
def generate_insights(df):
    """Generate insights from the data."""
    
    insights = engine.process(
        f"Analyze this dataset and provide 5 key insights. "
        f"Data summary:\n{df.describe().to_string()}"
    )
    
    return insights.final_output
```

---

## Support

For help with examples:
- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- Check documentation for more details
- Review error messages carefully
