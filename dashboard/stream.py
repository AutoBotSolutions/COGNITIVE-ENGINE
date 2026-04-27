"""
Event Stream for the Cognitive Dashboard

Connects the cognitive engine to the dashboard UI.
"""

from typing import Dict, Any, Optional
import asyncio
import json

from dashboard.events import CognitiveEvent, EventType, event_stream
from utils.logger import logger


class DashboardStreamer:
    """
    Streams cognitive events to the dashboard.
    """
    
    def __init__(self):
        self.connected_clients: set = set()
        self.enabled = True
    
    def connect(self, websocket) -> None:
        """Connect a new client (websocket)"""
        self.connected_clients.add(websocket)
        logger.info(f"DashboardStreamer: Client connected (total: {len(self.connected_clients)})")
    
    def disconnect(self, websocket) -> None:
        """Disconnect a client"""
        if websocket in self.connected_clients:
            self.connected_clients.remove(websocket)
            logger.info(f"DashboardStreamer: Client disconnected (total: {len(self.connected_clients)})")
    
    async def broadcast(self, event: CognitiveEvent) -> None:
        """Broadcast an event to all connected clients"""
        if not self.enabled:
            return
        
        if not self.connected_clients:
            return
        
        message = event.to_json()
        
        # Send to all connected clients
        disconnected = set()
        for client in self.connected_clients:
            try:
                await client.send(message)
            except Exception as e:
                logger.warning(f"DashboardStreamer: Failed to send to client: {e}")
                disconnected.add(client)
        
        # Remove disconnected clients
        for client in disconnected:
            self.disconnect(client)
    
    def emit_thought_event(self, thought_id: str, action: str, details: Dict[str, Any]) -> None:
        """Emit a thought-related event"""
        event = CognitiveEvent(
            event_type=EventType.THOUGHT_GENERATED if action == "generated" else EventType.THOUGHT_EVALUATED,
            data={
                "thought_id": thought_id,
                "action": action,
                **details
            }
        )
        event_stream.emit(event)
    
    def emit_memory_event(self, memory_type: str, action: str, details: Dict[str, Any]) -> None:
        """Emit a memory-related event"""
        event = CognitiveEvent(
            event_type=EventType.MEMORY_UPDATE,
            data={
                "memory_type": memory_type,
                "action": action,
                **details
            }
        )
        event_stream.emit(event)
    
    def emit_layer_event(self, layer: str, action: str, details: Dict[str, Any]) -> None:
        """Emit a layer execution event"""
        event = CognitiveEvent(
            event_type=EventType.LAYER_EXECUTION,
            data={
                "layer": layer,
                "action": action,
                **details
            }
        )
        event_stream.emit(event)
    
    def emit_agent_event(self, action: str, details: Dict[str, Any]) -> None:
        """Emit an agent action event"""
        event = CognitiveEvent(
            event_type=EventType.AGENT_ACTION,
            data={
                "action": action,
                **details
            }
        )
        event_stream.emit(event)
    
    def emit_error(self, error: str, details: Dict[str, Any] = None) -> None:
        """Emit an error event"""
        event = CognitiveEvent(
            event_type=EventType.ERROR,
            data={
                "error": error,
                **(details or {})
            }
        )
        event_stream.emit(event)


# Global dashboard streamer
dashboard_streamer = DashboardStreamer()
