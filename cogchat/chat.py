"""
CogChat - Cognitive Engine Chat Interface

A friendly interface for interacting with the Cognitive Engine.
"""

import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
from collections import defaultdict

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.interface import interface
from core.config import config


class ChatSession:
    """Represents a chat session with the Cognitive Engine"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.utcnow()
        self.message_count = 0
        self.history: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {}
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a message to the session history"""
        self.message_count += 1
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "message_number": self.message_count
        }
        if metadata:
            message["metadata"] = metadata
        self.history.append(message)
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get message history, optionally limited"""
        if limit:
            return self.history[-limit:]
        return self.history
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary"""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "message_count": self.message_count,
            "history": self.history,
            "metadata": self.metadata
        }


class CogChat:
    """
    Main chat interface for the Cognitive Engine.
    
    Provides a simple, friendly interface for interacting with the
    Cognitive Engine's cognitive layers and thought formation process.
    """
    
    def __init__(self):
        self.sessions: Dict[str, ChatSession] = {}
        self.active_session_id: Optional[str] = None
        self.session_counter = 0
        
    def create_session(self) -> str:
        """Create a new chat session"""
        self.session_counter += 1
        session_id = f"session_{self.session_counter}"
        session = ChatSession(session_id)
        self.sessions[session_id] = session
        self.active_session_id = session_id
        return session_id
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a session by ID"""
        return self.sessions.get(session_id)
    
    def get_active_session(self) -> Optional[ChatSession]:
        """Get the currently active session"""
        if self.active_session_id:
            return self.sessions.get(self.active_session_id)
        return None
    
    async def chat(self, message: str, session_id: Optional[str] = None, include_trace: bool = False) -> Dict[str, Any]:
        """
        Send a message to the Cognitive Engine and get a response.
        
        Args:
            message: The user's message
            session_id: Optional session ID (uses active if not provided)
            include_trace: Whether to include cognitive trace in response
        
        Returns:
            Dictionary containing response, session info, and optional trace
        """
        # Determine session
        if session_id:
            session = self.get_session(session_id)
        else:
            session = self.get_active_session()
        
        # Create session if none exists
        if not session:
            session_id = self.create_session()
            session = self.get_session(session_id)
        
        # Add user message to history
        session.add_message("user", message)
        
        # Process through Cognitive Engine
        try:
            response = await interface.process_async(message)
            
            # Extract human-readable output from API response
            if isinstance(response, dict) and 'output' in response:
                human_readable = response['output']
            else:
                human_readable = str(response)
            
            # Add assistant response to history
            session.add_message("assistant", human_readable)
            
            # Build response
            result = {
                "response": human_readable,
                "session_id": session.session_id,
                "message_number": session.message_count,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            if include_trace:
                result["trace"] = self._get_cognitive_trace(session)
                result["full_api_response"] = response  # Include full response for debugging
            
            return result
            
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            session.add_message("system", error_msg)
            return {
                "error": error_msg,
                "session_id": session.session_id,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _get_cognitive_trace(self, session: ChatSession) -> Dict[str, Any]:
        """Get cognitive trace information for the session"""
        # In a full implementation, this would extract trace from the cognitive engine
        # For now, return session-level trace info
        return {
            "session_id": session.session_id,
            "message_count": session.message_count,
            "session_duration": str(datetime.utcnow() - session.created_at)
        }
    
    def get_session_info(self, session_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get information about a session"""
        if session_id:
            session = self.get_session(session_id)
        else:
            session = self.get_active_session()
        
        if session:
            return session.to_dict()
        return None
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions"""
        return [session.to_dict() for session in self.sessions.values()]
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            if self.active_session_id == session_id:
                self.active_session_id = None
            return True
        return False
    
    def clear_all_sessions(self):
        """Clear all sessions"""
        self.sessions.clear()
        self.active_session_id = None
        self.session_counter = 0


# Global chat instance
chat = CogChat()
