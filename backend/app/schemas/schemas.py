from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class AudienceType(str, Enum):
    GENERAL = "general"
    SPECIAL_NEEDS = "special_needs"
    MIXED = "mixed"

class ContentVersion(str, Enum):
    STANDARD = "standard"
    SIMPLIFIED = "simplified"
    ACCESSIBILITY = "accessibility"

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    topic: Optional[str] = None
    target_audience: Optional[str] = None
    audience_type: AudienceType = AudienceType.GENERAL

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    topic: Optional[str] = None
    target_audience: Optional[str] = None
    audience_type: Optional[str] = None
    status: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    order_index: int = 0
    duration_minutes: int = 30

class LessonCreate(LessonBase):
    project_id: int

class LessonResponse(LessonBase):
    id: int
    project_id: int
    learning_objectives: List[str]
    content_standard: Dict[str, Any]
    content_simplified: Dict[str, Any]
    content_accessibility: Dict[str, Any]
    
    class Config:
        from_attributes = True

class UnitBase(BaseModel):
    title: str
    content: Dict[str, Any] = {}
    order_index: int = 0

class UnitCreate(UnitBase):
    lesson_id: int

class UnitResponse(UnitBase):
    id: int
    lesson_id: int
    activities: List[Dict[str, Any]]
    assessments: List[Dict[str, Any]]
    
    class Config:
        from_attributes = True

class AlertResponse(BaseModel):
    id: int
    project_id: int
    alert_type: str
    severity: str
    message: str
    suggestion: Optional[str]
    is_resolved: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class EvaluationResponse(BaseModel):
    id: int
    project_id: int
    interactivity_score: float
    multimedia_score: float
    assessment_score: float
    inclusiveness_score: float
    overall_score: float
    feedback: Optional[str]
    suggestions: List[str]
    evaluated_at: datetime
    
    class Config:
        from_attributes = True

class CurriculumRequest(BaseModel):
    topic: str
    target_audience: str = "university students"
    audience_type: AudienceType = AudienceType.GENERAL
    num_lessons: int = 5
    num_units_per_lesson: int = 3

class CurriculumResponse(BaseModel):
    project: ProjectResponse
    lessons: List[LessonResponse]
    message: str

class ContentGenerationRequest(BaseModel):
    topic: str
    target_audience: str = "university students"
    lesson_title: Optional[str] = None
    include_multimedia: bool = True
    include_assessments: bool = True

class SmartAssistRequest(BaseModel):
    text: str
    context: Optional[str] = None

class SmartAssistResponse(BaseModel):
    suggestions: List[Dict[str, Any]]
    score: float

class AlertFixRequest(BaseModel):
    alert_id: int
    project_id: int

class QualityMetrics(BaseModel):
    interactivity: float
    multimedia: float
    assessment: float
    inclusiveness: float
    overall: float
