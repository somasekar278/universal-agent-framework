"""
Services Module

Production service implementations:
- FastAPI REST API
- WebSocket server
- Background workers
- Service health endpoints

Usage:
    from services import AgentAPI, BackgroundWorker
    
    # Start API server
    api = AgentAPI()
    api.run(host="0.0.0.0", port=8000)
    
    # Background worker
    worker = BackgroundWorker()
    worker.start()
"""

from .api import (
    AgentAPI,
    create_app
)

from .worker import (
    BackgroundWorker,
    TaskQueue
)

from .websocket import (
    WebSocketServer,
    ConnectionManager
)

__all__ = [
    # API
    "AgentAPI",
    "create_app",
    
    # Workers
    "BackgroundWorker",
    "TaskQueue",
    
    # WebSocket
    "WebSocketServer",
    "ConnectionManager",
]

