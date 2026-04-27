# CogChat Documentation

CogChat is the interactive chat interface for the Cognitive Engine.

## Overview

CogChat provides a conversational interface to interact with the Cognitive Engine. It supports multiple modes:
- **CLI Mode**: Command-line interface for terminal users
- **Server Mode**: WebSocket server for web-based chat
- **Chat Mode**: Interactive chat with the Cognitive Engine

## Components

### chat.py

Core chat functionality for interacting with the Cognitive Engine.

**Key Features**:
- Session management
- Conversation history
- Context awareness
- Multi-turn conversations

### cli.py

Command-line interface for CogChat.

**Usage**:
```bash
python -m cogchat.cli
```

**Features**:
- Interactive terminal chat
- Command history
- Color-coded output
- Session persistence

### server.py

WebSocket server for web-based chat interface.

**Usage**:
```bash
python -m cogchat.server
```

**Features**:
- Real-time WebSocket communication
- Multiple concurrent sessions
- Session management
- CORS support

### config.py

Configuration for CogChat components.

**Configuration Options**:
- Server host and port
- Session timeout
- History retention
- Debug mode

## Usage Examples

### CLI Chat

```bash
# Start CLI chat
python -m cogchat.cli

# Interactive session
You: What is artificial intelligence?
CogChat: AI is the simulation of human intelligence in machines...
```

### Server Mode

```bash
# Start WebSocket server
python -m cogchat.server --host 0.0.0.0 --port 8080

# Connect from client
# WebSocket URL: ws://localhost:8080/ws
```

### Programmatic Usage

```python
from cogchat.chat import CogChat

# Initialize chat
chat = CogChat()

# Send message
response = chat.send_message("What is AI?")
print(response)
```

## Configuration

### Environment Variables

```bash
# Server configuration
COGCHAT_HOST=0.0.0.0
COGCHAT_PORT=8080
COGCHAT_DEBUG=false

# Session configuration
SESSION_TIMEOUT=3600
HISTORY_LIMIT=100
```

### Configuration File

Create `cogchat_config.yaml`:

```yaml
server:
  host: "0.0.0.0"
  port: 8080
  debug: false

session:
  timeout: 3600
  history_limit: 100
  persistence: true

engine:
  min_iterations: 3
  max_iterations: 50
  confidence_threshold: 0.7
```

## API Reference

### CogChat Class

```python
class CogChat:
    """Main chat interface class."""
    
    def __init__(self, config=None):
        """Initialize CogChat with optional configuration."""
    
    def send_message(self, message, session_id=None):
        """Send a message and get response."""
    
    def get_session(self, session_id):
        """Get session information."""
    
    def clear_session(self, session_id):
        """Clear session history."""
```

### WebSocket Endpoints

**Connect**: `ws://localhost:8080/ws`
**Message Format**:
```json
{
  "type": "message",
  "session_id": "optional-session-id",
  "content": "Your message here"
}
```

**Response Format**:
```json
{
  "type": "response",
  "content": "Response from Cognitive Engine",
  "confidence": 0.87,
  "iterations": 5
}
```

## Integration

### Web Frontend

```javascript
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'response') {
        console.log(data.content);
    }
};

ws.send(JSON.stringify({
    type: 'message',
    content: 'What is AI?'
}));
```

### Python Client

```python
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(data['content'])

ws = websocket.WebSocketApp('ws://localhost:8080/ws')
ws.on_message = on_message
ws.run_forever()
```

## Advanced Features

### Session Management

```python
from cogchat.chat import CogChat

chat = CogChat()

# Create session
session_id = chat.create_session()

# Send message in session
response = chat.send_message("Hello", session_id=session_id)

# Get session history
history = chat.get_session_history(session_id)

# Clear session
chat.clear_session(session_id)
```

### Context Awareness

CogChat maintains context across conversations:

```python
# First message
response1 = chat.send_message("What is Python?")

# Follow-up question (uses context)
response2 = chat.send_message("What about JavaScript?")
```

### Custom Prompts

Customize the chat prompts:

```python
from cogchat.chat import CogChat

chat = CogChat()
chat.set_system_prompt("You are a helpful AI assistant specializing in Python programming.")
```

## Troubleshooting

### Server Won't Start

**Issue**: Server fails to start

**Solution**:
- Check if port is available
- Verify configuration
- Check logs for errors

### WebSocket Connection Failed

**Issue**: Cannot connect to WebSocket server

**Solution**:
- Verify server is running
- Check firewall settings
- Verify URL is correct

### Session Lost

**Issue**: Session data is lost

**Solution**:
- Check session timeout settings
- Enable session persistence
- Check disk space

## Security Considerations

- Use HTTPS/WSS in production
- Implement authentication
- Rate limit connections
- Sanitize user input
- Session encryption

## Support

For CogChat issues:
- **Email**: autobotsolution@gmail.com
- **Address**: Flushing MI
- Check logs for error messages
