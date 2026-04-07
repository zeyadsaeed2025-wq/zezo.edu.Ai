from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from app.core.database import get_db
from app.models.models import User, Project, Lesson, Unit, Alert, Evaluation
from app.schemas.schemas import (
    ProjectCreate, ProjectResponse, ProjectUpdate,
    LessonCreate, LessonResponse,
    UnitCreate, UnitResponse,
    AlertResponse, EvaluationResponse,
    CurriculumRequest, CurriculumResponse
)
from app.api.auth import get_current_user
from app.services.ai_service import ai_service
from app.services.websocket_manager import realtime_service

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_project = Project(**project.model_dump(), owner_id=current_user.id)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Project).where(Project.owner_id == current_user.id).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await db.execute(delete(Project).where(Project.id == project_id))
    await db.commit()
    return {"message": "Project deleted"}

@router.get("/{project_id}/lessons", response_model=List[LessonResponse])
async def get_lessons(project_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Lesson).where(Lesson.project_id == project_id).order_by(Lesson.order_index)
    )
    return result.scalars().all()

@router.get("/{project_id}/alerts", response_model=List[AlertResponse])
async def get_alerts(project_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Alert).where(Alert.project_id == project_id).order_by(Alert.created_at.desc())
    )
    return result.scalars().all()

@router.get("/{project_id}/evaluations", response_model=List[EvaluationResponse])
async def get_evaluations(project_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Evaluation).where(Evaluation.project_id == project_id).order_by(Evaluation.evaluated_at.desc())
    )
    return result.scalars().all()

@router.post("/generate-curriculum", response_model=CurriculumResponse)
async def generate_curriculum(request: CurriculumRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    curriculum_data = await ai_service.generate_curriculum(
        topic=request.topic,
        target_audience=request.target_audience,
        audience_type=request.audience_type.value,
        num_lessons=request.num_lessons,
        num_units=request.num_units_per_lesson
    )
    
    project = Project(
        title=f"{request.topic} Curriculum",
        topic=request.topic,
        target_audience=request.target_audience,
        audience_type=request.audience_type.value,
        owner_id=current_user.id,
        status="generated"
    )
    db.add(project)
    await db.flush()
    
    lessons = []
    for idx, lesson_data in enumerate(curriculum_data.get("lessons", [])):
        lesson = Lesson(
            project_id=project.id,
            title=lesson_data.get("title", f"Lesson {idx+1}"),
            description=lesson_data.get("description", ""),
            learning_objectives=lesson_data.get("learning_objectives", []),
            duration_minutes=lesson_data.get("duration_minutes", 45),
            order_index=idx
        )
        db.add(lesson)
        await db.flush()
        
        for unit_idx, unit_data in enumerate(lesson_data.get("units", [])):
            content = unit_data.get("content", {})
            unit = Unit(
                lesson_id=lesson.id,
                title=unit_data.get("title", f"Unit {unit_idx+1}"),
                content=content,
                activities=unit_data.get("activities", []),
                assessments=unit_data.get("assessments", []),
                order_index=unit_idx
            )
            db.add(unit)
        
        lesson.content_standard = {"units": lesson_data.get("units", [])}
        lesson.content_simplified = {"units": lesson_data.get("units", [])}
        lesson.content_accessibility = {"units": lesson_data.get("units", [])}
        lessons.append(lesson)
    
    await db.commit()
    await db.refresh(project)
    
    return CurriculumResponse(
        project=ProjectResponse.model_validate(project),
        lessons=[LessonResponse.model_validate(l) for l in lessons],
        message="Curriculum generated successfully"
    )

@router.post("/{project_id}/lessons")
async def create_lesson(lesson: LessonCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_lesson = Lesson(**lesson.model_dump())
    db.add(db_lesson)
    await db.commit()
    await db.refresh(db_lesson)
    return db_lesson

@router.post("/lessons/{lesson_id}/units")
async def create_unit(unit: UnitCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_unit = Unit(**unit.model_dump())
    db.add(db_unit)
    await db.commit()
    await db.refresh(db_unit)
    return db_unit
