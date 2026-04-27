"""
CogChat Web Server

FastAPI web server for the Cognitive Engine chat interface.
"""

from typing import Optional, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from .chat import chat, CogChat
from .config import cogchat_config

app = FastAPI(title="CogChat - Cognitive Engine Chat Interface")


@app.get("/")
async def get_chat_interface():
    """Serve the chat interface HTML"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CogChat - Cognitive Engine Chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 100%);
            color: #00ffd9;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            flex: 1;
        }
        
        header {
            text-align: center;
            padding: 30px 0;
            border-bottom: 1px solid rgba(0, 255, 217, 0.2);
            margin-bottom: 30px;
        }
        
        h1 {
            font-size: 2.5em;
            text-shadow: 0 0 20px rgba(0, 255, 217, 0.5);
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #7df9ff;
            font-size: 1.1em;
        }
        
        .chat-container {
            display: flex;
            flex-direction: column;
            height: calc(100vh - 200px);
            border: 1px solid rgba(0, 255, 217, 0.3);
            border-radius: 10px;
            overflow: hidden;
            background: rgba(0, 40, 70, 0.2);
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }
        
        .message {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 8px;
            max-width: 80%;
        }
        
        .message.user {
            background: rgba(0, 255, 217, 0.1);
            margin-left: auto;
            border: 1px solid rgba(0, 255, 217, 0.3);
        }
        
        .message.assistant {
            background: rgba(125, 249, 255, 0.1);
            margin-right: auto;
            border: 1px solid rgba(125, 249, 255, 0.3);
        }
        
        .message.system {
            background: rgba(255, 100, 100, 0.1);
            text-align: center;
            border: 1px solid rgba(255, 100, 100, 0.3);
            font-style: italic;
        }
        
        .message-role {
            font-weight: bold;
            margin-bottom: 5px;
            color: #7df9ff;
        }
        
        .message-content {
            line-height: 1.6;
        }
        
        .message-meta {
            font-size: 0.8em;
            color: #5a7a8a;
            margin-top: 8px;
        }
        
        .input-area {
            padding: 20px;
            border-top: 1px solid rgba(0, 255, 217, 0.3);
            background: rgba(0, 30, 50, 0.3);
        }
        
        .input-form {
            display: flex;
            gap: 10px;
        }
        
        #user-input {
            flex: 1;
            padding: 12px;
            background: rgba(0, 20, 40, 0.5);
            border: 1px solid rgba(0, 255, 217, 0.3);
            border-radius: 5px;
            color: #00ffd9;
            font-family: 'Courier New', monospace;
            font-size: 1em;
        }
        
        #user-input:focus {
            outline: none;
            border-color: #00ffd9;
            box-shadow: 0 0 10px rgba(0, 255, 217, 0.3);
        }
        
        #send-btn {
            padding: 12px 30px;
            background: rgba(0, 255, 217, 0.2);
            border: 1px solid rgba(0, 255, 217, 0.5);
            border-radius: 5px;
            color: #00ffd9;
            font-family: 'Courier New', monospace;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        #send-btn:hover {
            background: rgba(0, 255, 217, 0.3);
            box-shadow: 0 0 15px rgba(0, 255, 217, 0.4);
        }
        
        .session-info {
            padding: 10px 20px;
            background: rgba(0, 30, 50, 0.5);
            border-bottom: 1px solid rgba(0, 255, 217, 0.2);
            font-size: 0.9em;
        }
        
        .controls {
            display: flex;
            gap: 10px;
        }
        
        .control-btn {
            padding: 5px 15px;
            background: rgba(0, 255, 217, 0.1);
            border: 1px solid rgba(0, 255, 217, 0.3);
            border-radius: 3px;
            color: #00ffd9;
            font-family: 'Courier New', monospace;
            font-size: 0.8em;
            cursor: pointer;
        }
        
        .control-btn:hover {
            background: rgba(0, 255, 217, 0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>COGCHAT</h1>
            <div class="subtitle">Cognitive Engine Chat Interface</div>
        </header>
        
        <div class="chat-container">
            <div class="session-info">
                <span id="session-id">Session: Loading...</span>
                <div class="controls">
                    <button class="control-btn" onclick="newSession()">New Session</button>
                    <button class="control-btn" onclick="clearChat()">Clear Chat</button>
                </div>
            </div>
            
            <div class="chat-messages" id="chat-messages">
                <div class="message system">
                    <div class="message-content">Connected to Cognitive Engine. Start typing to chat.</div>
                </div>
            </div>
            
            <div class="input-area">
                <form class="input-form" onsubmit="sendMessage(event)">
                    <input type="text" id="user-input" placeholder="Type your message..." autocomplete="off">
                    <button type="submit" id="send-btn">Send</button>
                </form>
            </div>
        </div>
    </div>
    
    <script>
        let currentSessionId = null;
        
        async function initSession() {
            const response = await fetch('/api/session/new', {
                method: 'POST'
            });
            const data = await response.json();
            currentSessionId = data.session_id;
            document.getElementById('session-id').textContent = `Session: ${currentSessionId}`;
        }
        
        async function sendMessage(event) {
            event.preventDefault();
            
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage('user', message);
            input.value = '';
            
            // Send to server
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        message: message,
                        session_id: currentSessionId
                    })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    addMessage('system', data.error);
                } else {
                    addMessage('assistant', data.response);
                }
                
            } catch (error) {
                addMessage('system', 'Error: Failed to send message');
            }
        }
        
        function addMessage(role, content) {
            const messagesDiv = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            
            const roleDiv = document.createElement('div');
            roleDiv.className = 'message-role';
            roleDiv.textContent = role.charAt(0).toUpperCase() + role.slice(1);
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            
            const metaDiv = document.createElement('div');
            metaDiv.className = 'message-meta';
            metaDiv.textContent = new Date().toLocaleTimeString();
            
            messageDiv.appendChild(roleDiv);
            messageDiv.appendChild(contentDiv);
            messageDiv.appendChild(metaDiv);
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        async function newSession() {
            await initSession();
            clearChat();
            addMessage('system', 'New session started.');
        }
        
        function clearChat() {
            const messagesDiv = document.getElementById('chat-messages');
            messagesDiv.innerHTML = '';
            addMessage('system', 'Chat cleared.');
        }
        
        // Initialize on load
        initSession();
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html)


@app.post("/api/session/new")
async def create_session():
    """Create a new chat session"""
    session_id = chat.create_session()
    return {"session_id": session_id}


@app.post("/api/chat")
async def send_message(request: Dict[str, Any]):
    """Send a message to the Cognitive Engine"""
    message = request.get("message")
    session_id = request.get("session_id")
    
    if not message:
        return {"error": "Message is required"}
    
    result = await chat.chat(message, session_id=session_id)
    return result


@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    session_info = chat.get_session_info(session_id)
    if session_info:
        return session_info
    return {"error": "Session not found"}


@app.get("/api/sessions")
async def list_sessions():
    """List all sessions"""
    return {"sessions": chat.list_sessions()}


@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    success = chat.delete_session(session_id)
    if success:
        return {"success": True}
    return {"error": "Session not found"}


def start_server():
    """Start the CogChat web server"""
    print(f"\nCogChat Server")
    print(f"Starting on {cogchat_config.host}:{cogchat_config.port}\n")
    
    uvicorn.run(
        app,
        host=cogchat_config.host,
        port=cogchat_config.port,
        log_level="info"
    )


if __name__ == "__main__":
    start_server()
