"""
WebSocket Server for the Cognitive Dashboard

FastAPI WebSocket server for real-time cognitive telemetry.
"""

from typing import Dict, Any
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from dashboard.stream import dashboard_streamer
from dashboard.events import event_stream
from core.config import config
from utils.logger import logger


app = FastAPI(title="Cognitive Engine Dashboard")

# Mount static files directory
try:
    app.mount("/static", StaticFiles(directory="ui"), name="static")
except Exception:
    pass  # If ui directory doesn't exist, continue without static files


@app.get("/")
async def get_dashboard():
    """Serve the dashboard HTML"""
    try:
        with open("ui/index.html", "r") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("<html><body><h1>Dashboard UI not found. Please create ui/index.html</h1></body></html>")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    
    dashboard_streamer.connect(websocket)
    
    # Send recent events on connection
    recent_events = event_stream.get_recent(50)
    for event in recent_events:
        try:
            await websocket.send(event.to_json())
        except:
            break
    
    # Set up event forwarding
    async def event_forwarder(event):
        try:
            await websocket.send(event.to_json())
        except:
            pass
    
    event_stream.subscribe(event_forwarder)
    
    try:
        # Keep connection alive
        while True:
            # Ping/pong to keep connection alive
            await asyncio.sleep(30)
            try:
                await websocket.send_json({"type": "ping"})
            except:
                break
    except WebSocketDisconnect:
        logger.info("Dashboard: WebSocket disconnected")
    finally:
        event_stream.unsubscribe(event_forwarder)
        dashboard_streamer.disconnect(websocket)


@app.get("/api/events")
async def get_events(limit: int = 100):
    """Get recent events via REST API"""
    events = event_stream.get_recent(limit)
    return {"events": [e.to_dict() for e in events]}


@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics"""
    return {
        "total_events": len(event_stream.events),
        "connected_clients": len(dashboard_streamer.connected_clients),
        "recent_events": len(event_stream.get_recent(100))
    }


def start_dashboard():
    """Start the dashboard server"""
    if not config.enable_dashboard:
        logger.info("Dashboard: Disabled in config")
        return
    
    logger.info(f"Dashboard: Starting on {config.dashboard_host}:{config.dashboard_port}")
    
    uvicorn.run(
        app,
        host=config.dashboard_host,
        port=config.dashboard_port,
        log_level="info"
    )


if __name__ == "__main__":
    start_dashboard()
