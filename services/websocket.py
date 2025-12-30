"""WebSocket Server for Real-time Agent Communication"""
from typing import List

class ConnectionManager:
    """Manage WebSocket connections"""
    def __init__(self):
        self.active_connections: List = []
    
    async def connect(self, websocket):
        """Connect a new WebSocket"""
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket):
        """Disconnect a WebSocket"""
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        """Broadcast to all connections"""
        for connection in self.active_connections:
            await connection.send_text(message)

class WebSocketServer:
    """WebSocket server for real-time agent updates"""
    def __init__(self):
        self.manager = ConnectionManager()
        print("🔌 WebSocket server initialized")

