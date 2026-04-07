from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.core.database import get_db
from app.models.models import User, Project, Alert, Evaluation
from app.schemas.schemas import (
    SmartAssistRequest, SmartAssistResponse,
    ContentGenerationRequest,
    QualityMetrics
)
from app.api.auth import get_current_user
from app.services.ai_service import ai_service
from app.services.websocket_manager import realtime_service

router = APIRouter(prefix="/ai", tags=["AI Features"])

@router.post("/smart-assist", response_model=SmartAssistResponse)
async def smart_assist(request: SmartAssistRequest, current_user: User = Depends(get_current_user)):
    result = await ai_service.smart_assist(text=request.text, context=request.context)
    return result

@router.post("/generate-content")
async def generate_content(request: ContentGenerationRequest, current_user: User = Depends(get_current_user)):
    result = await ai_service.generate_lesson_content(
        topic=request.topic,
        target_audience=request.target_audience,
        lesson_title=request.lesson_title or request.topic,
        include_multimedia=request.include_multimedia,
        include_assessments=request.include_assessments
    )
    return result

@router.post("/evaluate/{project_id}")
async def evaluate_project(project_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_data = {
        "id": project.id,
        "title": project.title,
        "topic": project.topic,
        "target_audience": project.target_audience
    }
    
    evaluation = await ai_service.analyze_content_quality(project_data)
    
    db_evaluation = Evaluation(
        project_id=project_id,
        interactivity_score=evaluation.get("interactivity_score", 0),
        multimedia_score=evaluation.get("multimedia_score", 0),
        assessment_score=evaluation.get("assessment_score", 0),
        inclusiveness_score=evaluation.get("inclusiveness_score", 0),
        overall_score=evaluation.get("overall_score", 0),
        feedback=evaluation.get("feedback", ""),
        suggestions=evaluation.get("suggestions", [])
    )
    db.add(db_evaluation)
    await db.commit()
    await db.refresh(db_evaluation)
    
    metrics = {
        "interactivity": evaluation.get("interactivity_score", 0),
        "multimedia": evaluation.get("multimedia_score", 0),
        "assessment": evaluation.get("assessment_score", 0),
        "inclusiveness": evaluation.get("inclusiveness_score", 0),
        "overall": evaluation.get("overall_score", 0)
    }
    await realtime_service.send_quality_update(project_id, metrics)
    
    return {"evaluation": db_evaluation, "metrics": metrics}

@router.post("/analyze/{project_id}")
async def analyze_project(project_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_data = {
        "id": project.id,
        "title": project.title,
        "topic": project.topic
    }
    
    alerts = await ai_service.detect_alerts(project_data)
    
    for alert_data in alerts:
        db_alert = Alert(
            project_id=project_id,
            alert_type=alert_data.get("alert_type", "quality"),
            severity=alert_data.get("severity", "warning"),
            message=alert_data.get("message", ""),
            suggestion=alert_data.get("suggestion")
        )
        db.add(db_alert)
        await realtime_service.send_alert(project_id, alert_data)
    
    await db.commit()
    
    return {"alerts": alerts, "count": len(alerts)}

@router.post("/fix-alert/{alert_id}")
async def fix_alert(alert_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    fixed = await ai_service.fix_content_issue(
        issue_type=alert.alert_type,
        content={}
    )
    
    alert.is_resolved = True
    await db.commit()
    
    return fixed

@router.delete("/alerts/{alert_id}")
async def delete_alert(alert_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await db.execute(delete(Alert).where(Alert.id == alert_id))
    await db.commit()
    return {"message": "Alert deleted"}

@router.get("/quality-metrics/{project_id}")
async def get_quality_metrics(project_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> QualityMetrics:
    result = await db.execute(
        select(Evaluation).where(Evaluation.project_id == project_id).order_by(Evaluation.evaluated_at.desc())
    )
    evaluation = result.scalar_one_or_none()
    
    if evaluation:
        return QualityMetrics(
            interactivity=evaluation.interactivity_score,
            multimedia=evaluation.multimedia_score,
            assessment=evaluation.assessment_score,
            inclusiveness=evaluation.inclusiveness_score,
            overall=evaluation.overall_score
        )
    
    return QualityMetrics(interactivity=0, multimedia=0, assessment=0, inclusiveness=0, overall=0)
