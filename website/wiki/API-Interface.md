# API Interface Documentation

The Cognitive Engine provides a programmatic API for integration with external applications.

## Overview

The API interface is located in the `api/` directory and provides:
- External access to Cognitive Engine functionality
- RESTful endpoints for web applications
- WebSocket support for real-time communication
- Authentication and authorization
- Rate limiting and throttling

## Components

### interface.py

Main API interface providing external access to the Cognitive Engine.

**Location**: `api/interface.py`

**Key Features**:
- Query processing endpoint
- Configuration management
- Session management
- Authentication
- Error handling

## API Endpoints

### POST /api/query

Process a query through the Cognitive Engine.

**Request**:
```json
{
  "query": "What is artificial intelligence?",
  "config": {
    "min_iterations": 3,
    "max_iterations": 50,
    "confidence_threshold": 0.7
  }
}
```

**Response**:
```json
{
  "answer": "AI is the simulation of human intelligence...",
  "confidence": 0.87,
  "iterations": 5,
  "reasoning_trace": "...",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### GET /api/health

Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

### POST /api/config

Update configuration.

**Request**:
```json
{
  "min_iterations": 5,
  "max_iterations": 30,
  "confidence_threshold": 0.8
}
```

**Response**:
```json
{
  "status": "success",
  "config": { ... }
}
```

### GET /api/config

Get current configuration.

**Response**:
```json
{
  "min_iterations": 3,
  "max_iterations": 50,
  "confidence_threshold": 0.7
}
```

### GET /api/memory

Access memory system.

**Response**:
```json
{
  "episodic_count": 1000,
  "pattern_count": 50,
  "rule_count": 20
}
```

### POST /api/session

Create a new session.

**Request**:
```json
{
  "user_id": "user123",
  "metadata": {}
}
```

**Response**:
```json
{
  "session_id": "session_abc123",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### GET /api/session/:id

Get session information.

**Response**:
```json
{
  "session_id": "session_abc123",
  "created_at": "2024-01-01T00:00:00Z",
  "query_count": 10,
  "last_activity": "2024-01-01T01:00:00Z"
}
```

## WebSocket API

### Connection

Connect to WebSocket endpoint:

```
ws://localhost:8000/ws
```

### Message Format

**Client to Server**:
```json
{
  "type": "query",
  "session_id": "optional-session-id",
  "query": "Your question here",
  "config": { ... }
}
```

**Server to Client**:
```json
{
  "type": "response",
  "answer": "Response from Cognitive Engine",
  "confidence": 0.87,
  "iterations": 5
}
```

### Event Types

- `query`: Process a query
- `response`: Query response
- `error`: Error message
- `status`: Status update
- `memory_update`: Memory change notification

## Authentication

### API Key Authentication

Include API key in request header:

```http
Authorization: Bearer your-api-key
```

### Session Authentication

Use session ID for authentication:

```http
X-Session-ID: session_abc123
```

## Rate Limiting

Default rate limits:
- 100 requests per minute per IP
- 1000 requests per hour per IP
- 10000 requests per day per IP

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional details"
  }
}
```

### Common Error Codes

- `INVALID_REQUEST`: Malformed request
- `AUTHENTICATION_FAILED`: Invalid credentials
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error
- `CONFIGURATION_ERROR`: Invalid configuration

## Usage Examples

### Python Requests

```python
import requests

# Process query
response = requests.post(
    'http://localhost:8000/api/query',
    json={'query': 'What is AI?'},
    headers={'Authorization': 'Bearer your-api-key'}
)

result = response.json()
print(result['answer'])
```

### cURL

```bash
# Process query
curl -X POST http://localhost:8000/api/query \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is AI?"}'
```

### JavaScript Fetch

```javascript
fetch('http://localhost:8000/api/query', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-api-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ query: 'What is AI?' })
})
.then(response => response.json())
.then(data => console.log(data.answer));
```

### WebSocket Client

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'query',
    query: 'What is AI?'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'response') {
    console.log(data.answer);
  }
};
```

## Configuration

### Server Configuration

```python
from api.interface import APIServer

server = APIServer(
    host='0.0.0.0',
    port=8000,
    debug=False,
    enable_auth=True,
    rate_limit=100
)
server.start()
```

### Environment Variables

```bash
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
API_AUTH=true
API_RATE_LIMIT=100
API_KEY=your-api-key
```

## SDKs

### Python SDK

```python
from cognitive_engine import CognitiveEngineClient

client = CognitiveEngineClient(
    api_key='your-api-key',
    base_url='http://localhost:8000'
)

result = client.query('What is AI?')
print(result.answer)
```

### JavaScript SDK

```javascript
import { CognitiveEngineClient } from 'cognitive-engine-js';

const client = new CognitiveEngineClient({
  apiKey: 'your-api-key',
  baseUrl: 'http://localhost:8000'
});

const result = await client.query('What is AI?');
console.log(result.answer);
```

## Deployment

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "api.interface"]
```

### Docker Compose

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_KEY=your-api-key
      - API_HOST=0.0.0.0
      - API_PORT=8000
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cognitive-engine-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cognitive-engine-api
  template:
    metadata:
      labels:
        app: cognitive-engine-api
    spec:
      containers:
      - name: api
        image: cognitive-engine:latest
        ports:
        - containerPort: 8000
        env:
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: api-key
```

## Monitoring

### Metrics Endpoint

```
GET /api/metrics
```

Returns Prometheus-compatible metrics.

### Health Check

```
GET /api/health
```

Returns health status.

### Logging

API logs to `cognitive_engine.log` with prefix `[API]`.

## Security

### HTTPS

Use HTTPS in production:

```python
server = APIServer(
    ssl_keyfile='path/to/key.pem',
    ssl_certfile='path/to/cert.pem'
)
```

### CORS

Configure CORS:

```python
server = APIServer(
    cors_origins=['https://yourdomain.com']
)
```

### Input Validation

All inputs are validated using Pydantic models.

### Output Sanitization

All outputs are sanitized to prevent XSS.

## Support

For API issues:
- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- Check logs: `cognitive_engine.log`
- Review error responses
