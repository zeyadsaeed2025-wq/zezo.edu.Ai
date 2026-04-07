from fastapi import WebSocket
from typing import Dict, Set, Optional
from datetime import datetime
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict[str, WebSocket]] = {}
        self.project_subscribers: Dict[int, Set[int]] = {}

    async def connect(self, websocket: WebSocket, user_id: int, project_id: Optional[int] = None):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = {}
        
        conn_id = f"{user_id}_{datetime.utcnow().timestamp()}"
        self.active_connections[user_id][conn_id] = websocket
        
        if project_id:
            if project_id not in self.project_subscribers:
                self.project_subscribers[project_id] = set()
            self.project_subscribers[project_id].add(user_id)
        
        return conn_id

    def disconnect(self, user_id: int, conn_id: str, project_id: Optional[int] = None):
        if user_id in self.active_connections:
            self.active_connections[user_id].pop(conn_id, None)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        if project_id and project_id in self.project_subscribers:
            self.project_subscribers[project_id].discard(user_id)

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            for conn_id, websocket in self.active_connections[user_id].items():
                try:
                    await websocket.send_json(message)
                except Exception:
                    pass

    async def broadcast_to_project(self, message: dict, project_id: int):
        if project_id in self.project_subscribers:
            for user_id in self.project_subscribers[project_id]:
                await self.send_personal_message(message, user_id)

manager = ConnectionManager()

class RealtimeService:
    def __init__(self):
        self.manager = manager

    async def send_alert(self, project_id: int, alert: dict):
        message = {
            "type": "alert",
            "data": alert,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.manager.broadcast_to_project(message, project_id)

    async def send_quality_update(self, project_id: int, metrics: dict):
        message = {
            "type": "quality_update",
            "data": metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.manager.broadcast_to_project(message, project_id)

    async def send_suggestion(self, project_id: int, suggestion: dict):
        message = {
            "type": "suggestion",
            "data": suggestion,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.manager.broadcast_to_project(message, project_id)

realtime_service = RealtimeService()
