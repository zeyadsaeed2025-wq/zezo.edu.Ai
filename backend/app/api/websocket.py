from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Optional
from app.services.websocket_manager import manager
from app.services.ai_service import ai_service
from app.core.security import decode_token

router = APIRouter(prefix="/ws", tags=["WebSocket"])

@router.websocket("/{project_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    project_id: int,
    token: Optional[str] = Query(None)
):
    user_id = None
    if token:
        payload = decode_token(token)
        if payload:
            user_id = payload.get("sub")
    
    if not user_id:
        await websocket.close(code=4001, reason="Authentication required")
        return
    
    conn_id = await manager.connect(websocket, user_id, project_id)
    
    try:
        await websocket.send_json({
            "type": "connected",
            "data": {"message": "Connected to EduForge AI", "conn_id": conn_id},
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        })
        
        while True:
            data = await websocket.receive_json()
            await handle_message(websocket, data, user_id, project_id)
            
    except WebSocketDisconnect:
        manager.disconnect(user_id, conn_id, project_id)

async def handle_message(websocket: WebSocket, data: dict, user_id: int, project_id: int):
    msg_type = data.get("type")
    msg_data = data.get("data", {})
    
    from app.services.websocket_manager import realtime_service
    
    if msg_type == "ping":
        await websocket.send_json({
            "type": "pong",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        })
    
    elif msg_type == "smart_assist":
        result = await ai_service.smart_assist(
            text=msg_data.get("text", ""),
            context=msg_data.get("context")
        )
        await websocket.send_json({
            "type": "smart_assist_result",
            "data": result,
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        })
        await realtime_service.send_suggestion(project_id, result)
    
    elif msg_type == "analyze":
        alerts = await ai_service.detect_alerts(msg_data.get("project_data", {}))
        await websocket.send_json({
            "type": "alerts_result",
            "data": {"alerts": alerts},
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        })
        for alert in alerts:
            await realtime_service.send_alert(project_id, alert)
    
    elif msg_type == "evaluate":
        result = await ai_service.analyze_content_quality(msg_data.get("project_data", {}))
        await websocket.send_json({
            "type": "evaluation_result",
            "data": result,
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        })
        metrics = {
            "interactivity": result.get("interactivity_score", 0),
            "multimedia": result.get("multimedia_score", 0),
            "assessment": result.get("assessment_score", 0),
            "inclusiveness": result.get("inclusiveness_score", 0),
            "overall": result.get("overall_score", 0)
        }
        await realtime_service.send_quality_update(project_id, metrics)
    
    elif msg_type == "fix":
        result = await ai_service.fix_content_issue(
            issue_type=msg_data.get("issue_type", "no_interaction"),
            content=msg_data.get("content", {})
        )
        await websocket.send_json({
            "type": "fix_result",
            "data": result,
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        })
    
    else:
        await websocket.send_json({
            "type": "error",
            "data": {"message": f"Unknown message type: {msg_type}"},
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        })
