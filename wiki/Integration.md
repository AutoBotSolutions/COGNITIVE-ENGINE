This guide covers integrating the Cognitive Engine with other systems and applications.

## Table of Contents

- [Integration Overview](#integration-overview)
- [REST API Integration](#rest-api-integration)
- [WebSocket Integration](#websocket-integration)
- [Python Library Integration](#python-library-integration)
- [Web Application Integration](#web-application-integration)
- [CLI Integration](#cli-integration)
- [Database Integration](#database-integration)
- [Message Queue Integration](#message-queue-integration)
- [Cloud Service Integration](#cloud-service-integration)
- [Custom Tool Development](#custom-tool-development)

---

## Integration Overview

The Cognitive Engine can be integrated with various systems through multiple interfaces:

- **REST API**: HTTP-based API for web applications
- **WebSocket**: Real-time bidirectional communication
- **Python Library**: Direct Python imports
- **CLI**: Command-line interface for scripts
- **Database**: Direct database access
- **Message Queues**: Asynchronous processing

### Integration Patterns

- **Synchronous**: Direct request/response
- **Asynchronous**: Background processing
- **Event-Driven**: React to cognitive events
- **Batch Processing**: Process multiple queries
- **Streaming**: Real-time cognitive telemetry

---

## REST API Integration

### Basic FastAPI Setup

Create a REST API wrapper:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.engine import CognitiveEngine
import uvicorn

app = FastAPI(title="Cognitive Engine API")
engine = CognitiveEngine()

class QueryRequest(BaseModel):
    query: str
    min_iterations: int = 3
    max_iterations: int = 50
    confidence_threshold: float = 0.7

class QueryResponse(BaseModel):
    answer: str
    confidence: float
    iterations: int
    reasoning_trace: str = None

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a query through the Cognitive Engine."""
    try:
        # Configure engine for this request
        from core.config import Config
        config = Config(
            min_iterations=request.min_iterations,
            max_iterations=request.max_iterations,
            confidence_threshold=request.confidence_threshold
        )
        
        # Process query
        result = engine.process(request.query)
        
        return QueryResponse(
            answer=result.final_output,
            confidence=result.confidence,
            iterations=result.iteration_count,
            reasoning_trace=result.reasoning_trace
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Authentication

Add authentication to your API:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != os.environ.get('API_TOKEN'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication token"
        )
    return token

@app.post("/query")
async def process_query(
    request: QueryRequest,
    token: str = Depends(verify_token)
):
    # Protected endpoint
    pass
```

### Rate Limiting

Add rate limiting:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/query")
@limiter.limit("10/minute")
async def process_query(request: QueryRequest):
    # Rate limited endpoint
    pass
```

### Docker Deployment

Deploy the API with Docker:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## WebSocket Integration

### Real-Time Cognitive Events

Stream cognitive events via WebSocket:

```python
from fastapi import WebSocket, WebSocketDisconnect
from dashboard.stream import dashboard_streamer

@app.websocket("/ws/cognitive")
async def cognitive_websocket(websocket: WebSocket):
    """WebSocket endpoint for real-time cognitive events."""
    await websocket.accept()
    
    try:
        # Subscribe to dashboard stream
        dashboard_streamer.subscribe(websocket)
        
        while True:
            # Keep connection alive
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        dashboard_streamer.unsubscribe(websocket)
```

### Client-Side JavaScript

Connect from JavaScript:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/cognitive');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'thought_generated':
            displayThought(data.thought);
            break;
        case 'memory_updated':
            updateMemoryDisplay(data.memory);
            break;
        case 'deliberation_complete':
            showResult(data.result);
            break;
    }
};

function displayThought(thought) {
    // Update UI with new thought
}

function updateMemoryDisplay(memory) {
    // Update memory visualization
}

function showResult(result) {
    // Display final result
}
```

---

## Python Library Integration

### Direct Import

Use the engine directly in Python:

```python
from core.engine import CognitiveEngine

# Initialize engine
engine = CognitiveEngine()

# Process query
result = engine.process("What is AI?")

# Access results
print(result.final_output)
print(result.confidence)
print(result.iteration_count)
```

### Custom Configuration

Configure the engine programmatically:

```python
from core.config import Config
from core.engine import CognitiveEngine

config = Config(
    min_iterations=5,
    max_iterations=30,
    confidence_threshold=0.8,
    enable_dashboard=False
)

engine = CognitiveEngine(config)
```

### Batch Processing

Process multiple queries:

```python
def process_batch(queries):
    """Process multiple queries efficiently."""
    results = []
    for query in queries:
        result = engine.process(query)
        results.append({
            'query': query,
            'answer': result.final_output,
            'confidence': result.confidence
        })
    return results

queries = [
    "What is Python?",
    "What is JavaScript?",
    "What is Rust?"
]
results = process_batch(queries)
```

### Async Processing

Use async for concurrent processing:

```python
import asyncio

async def process_async(query):
    """Process query asynchronously."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, engine.process, query)
    return result

async def process_batch_async(queries):
    """Process multiple queries concurrently."""
    tasks = [process_async(q) for q in queries]
    results = await asyncio.gather(*tasks)
    return results
```

---

## Web Application Integration

### Flask Integration

Integrate with Flask:

```python
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

if __name__ == '__main__':
    app.run(debug=True)
```

### Django Integration

Integrate with Django:

```python
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.engine import CognitiveEngine

engine = CognitiveEngine()

@csrf_exempt
def query_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = engine.process(data['query'])
        return JsonResponse({
            'answer': result.final_output,
            'confidence': result.confidence
        })
```

### React Integration

Integrate with React:

```javascript
// api.js
export async function queryCognitiveEngine(query) {
    const response = await fetch('/api/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
    });
    return response.json();
}

// Component.js
import { useState } from 'react';
import { queryCognitiveEngine } from './api';

function CognitiveQuery() {
    const [query, setQuery] = useState('');
    const [result, setResult] = useState(null);
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await queryCognitiveEngine(query);
        setResult(response);
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <input 
                value={query} 
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your query"
            />
            <button type="submit">Submit</button>
            {result && (
                <div>
                    <p>{result.answer}</p>
                    <p>Confidence: {result.confidence}</p>
                </div>
            )}
        </form>
    );
}
```

---

## CLI Integration

### Command-Line Tool

Create a CLI tool:

```python
#!/usr/bin/env python3
import argparse
from core.engine import CognitiveEngine

def main():
    parser = argparse.ArgumentParser(description='Cognitive Engine CLI')
    parser.add_argument('query', help='Query to process')
    parser.add_argument('--iterations', type=int, default=10,
                       help='Maximum iterations')
    parser.add_argument('--confidence', type=float, default=0.7,
                       help='Confidence threshold')
    parser.add_argument('--output', help='Output file')
    
    args = parser.parse_args()
    
    # Configure engine
    from core.config import Config
    config = Config(
        max_iterations=args.iterations,
        confidence_threshold=args.confidence
    )
    
    engine = CognitiveEngine(config)
    result = engine.process(args.query)
    
    output = f"Answer: {result.final_output}\n"
    output += f"Confidence: {result.confidence}\n"
    output += f"Iterations: {result.iteration_count}\n"
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
    else:
        print(output)

if __name__ == '__main__':
    main()
```

### Shell Script Integration

Use from shell scripts:

```bash
#!/bin/bash
QUERY="$1"
OUTPUT="$2"

python3 cognitive_cli.py "$QUERY" --output "$OUTPUT"

if [ $? -eq 0 ]; then
    echo "Query processed successfully"
    cat "$OUTPUT"
else
    echo "Query processing failed"
    exit 1
fi
```

---

## Database Integration

### Direct Database Access

Access memory database directly:

```python
import sqlite3

def get_memory_stats():
    """Get statistics from memory database."""
    conn = sqlite3.connect('cognitive_engine.db')
    cursor = conn.cursor()
    
    # Get episodic memory count
    cursor.execute("SELECT COUNT(*) FROM episodic_memory")
    episodic_count = cursor.fetchone()[0]
    
    # Get pattern memory count
    cursor.execute("SELECT COUNT(*) FROM pattern_memory")
    pattern_count = cursor.fetchone()[0]
    
    # Get rule memory count
    cursor.execute("SELECT COUNT(*) FROM rule_memory")
    rule_count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'episodic': episodic_count,
        'patterns': pattern_count,
        'rules': rule_count
    }
```

### PostgreSQL Integration

Use PostgreSQL for production:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure PostgreSQL
DATABASE_URL = "postgresql://user:pass@localhost/cognitive_engine"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def store_result(result):
    """Store processing result in PostgreSQL."""
    session = Session()
    
    from models import ProcessResult
    db_result = ProcessResult(
        query=result.query,
        answer=result.final_output,
        confidence=result.confidence,
        iterations=result.iteration_count,
        timestamp=datetime.now()
    )
    
    session.add(db_result)
    session.commit()
    session.close()
```

---

## Message Queue Integration

### RabbitMQ Integration

Use RabbitMQ for async processing:

```python
import pika
from core.engine import CognitiveEngine

def process_query(ch, method, properties, body):
    """Process query from message queue."""
    query = body.decode('utf-8')
    
    engine = CognitiveEngine()
    result = engine.process(query)
    
    # Send response
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=str(result.final_output)
    )
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Setup connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='cognitive_queries')
channel.basic_consume(queue='cognitive_queries', on_message_callback=process_query)

print('Waiting for messages...')
channel.start_consuming()
```

### Celery Integration

Use Celery for distributed task processing:

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

## Cloud Service Integration

### AWS Lambda

Deploy as AWS Lambda function:

```python
import json
from core.engine import CognitiveEngine

def lambda_handler(event, context):
    """AWS Lambda handler."""
    query = event.get('query')
    
    engine = CognitiveEngine()
    result = engine.process(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'answer': result.final_output,
            'confidence': result.confidence
        })
    }
```

### Google Cloud Functions

Deploy as Google Cloud Function:

```python
import functions_framework
from core.engine import CognitiveEngine

@functions_framework.http
def process_query(request):
    """HTTP Cloud Function."""
    request_json = request.get_json(silent=True)
    query = request_json.get('query')
    
    engine = CognitiveEngine()
    result = engine.process(query)
    
    return {
        'answer': result.final_output,
        'confidence': result.confidence
    }
```

### Azure Functions

Deploy as Azure Function:

```python
import azure.functions as func
from core.engine import CognitiveEngine

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function handler."""
    query = req.params.get('query')
    
    engine = CognitiveEngine()
    result = engine.process(query)
    
    return func.HttpResponse(
        json.dumps({
            'answer': result.final_output,
            'confidence': result.confidence
        }),
        status_code=200
    )
```

---

## Custom Tool Development

### Creating Custom Tools

Add custom tools for agent mode:

```python
from tools.registry import Tool, ToolRegistry

class CustomTool(Tool):
    """Custom tool example."""
    
    def __init__(self):
        super().__init__(
            name="custom_tool",
            description="Description of what this tool does"
        )
    
    def execute(self, params):
        """Execute the tool."""
        # Your custom logic here
        result = self.perform_operation(params)
        return {
            'success': True,
            'data': result,
            'execution_time': 0.5
        }
    
    def perform_operation(self, params):
        """Implement your operation."""
        # Your implementation
        return "result"

# Register the tool
tool_registry = ToolRegistry()
tool_registry.register_tool(CustomTool())
```

### Tool with API Integration

Create a tool that calls external APIs:

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
        
        url = f"http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={location}"
        response = requests.get(url)
        data = response.json()
        
        return {
            'success': True,
            'data': data,
            'location': location
        }
```

### Database Tool

Create a tool for database operations:

```python
import sqlite3

class DatabaseQueryTool(Tool):
    """Tool for querying databases."""
    
    def __init__(self, db_path):
        super().__init__(
            name="db_query",
            description="Execute SQL queries on a database"
        )
        self.db_path = db_path
    
    def execute(self, params):
        """Execute SQL query."""
        query = params.get('query')
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        conn.close()
        
        return {
            'success': True,
            'data': results,
            'row_count': len(results)
        }
```

---

## Monitoring Integration

### Prometheus Integration

Export metrics to Prometheus:

```python
from prometheus_client import Counter, Histogram, start_http_server

# Define metrics
query_counter = Counter('cognitive_queries_total', 'Total queries processed')
query_duration = Histogram('cognitive_query_duration_seconds', 'Query duration')

def process_with_metrics(query):
    """Process query with metrics."""
    query_counter.inc()
    
    with query_duration.time():
        result = engine.process(query)
    
    return result

# Start metrics server
start_http_server(8001)
```

### Grafana Integration

Create Grafana dashboard:

```json
{
  "dashboard": {
    "title": "Cognitive Engine Metrics",
    "panels": [
      {
        "title": "Query Rate",
        "targets": [
          {
            "expr": "rate(cognitive_queries_total[5m])"
          }
        ]
      },
      {
        "title": "Query Duration",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, cognitive_query_duration_seconds)"
          }
        ]
      }
    ]
  }
}
```

---

## Testing Integration

### Unit Tests

Test integration points:

```python
import pytest
from core.engine import CognitiveEngine

def test_api_integration():
    """Test API integration."""
    engine = CognitiveEngine()
    result = engine.process("Test query")
    assert result.final_output is not None
    assert result.confidence >= 0
    assert result.iteration_count > 0

def test_batch_processing():
    """Test batch processing."""
    queries = ["Query 1", "Query 2", "Query 3"]
    results = [engine.process(q) for q in queries]
    assert len(results) == len(queries)
```

### Integration Tests

Test full integration:

```python
def test_websocket_integration():
    """Test WebSocket integration."""
    import websockets
    
    async def test():
        async with websockets.connect('ws://localhost:8000/ws/cognitive') as ws:
            # Send test message
            await ws.send('test')
            # Receive response
            response = await ws.recv()
            assert response is not None
    
    asyncio.run(test())
```

---

## Best Practices

### Error Handling

Implement robust error handling:

```python
from fastapi import HTTPException

@app.post("/query")
async def process_query(request: QueryRequest):
    try:
        result = engine.process(request.query)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal error")
```

### Logging

Log integration events:

```python
import logging

logger = logging.getLogger('integration')

@app.post("/query")
async def process_query(request: QueryRequest):
    logger.info(f"Processing query: {request.query[:50]}...")
    result = engine.process(request.query)
    logger.info(f"Query processed in {result.iteration_count} iterations")
    return result
```

### Validation

Validate inputs:

```python
from pydantic import BaseModel, validator

class QueryRequest(BaseModel):
    query: str
    
    @validator('query')
    def validate_query(cls, v):
        if len(v) > 10000:
            raise ValueError("Query too long")
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v
```

### Security

Implement security measures:

```python
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != os.environ.get("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key
```

---

## Support

For integration issues:
- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- Check logs: `cognitive_engine.log`
- Review API documentation
- Test integration endpoints
