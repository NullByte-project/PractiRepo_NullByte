from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class PracticeType(str, Enum):
    INSTITUCIONAL_I = "Informes de práctica institucional I"
    INSTITUCIONAL_II = "Informes de práctica institucional II"
    VIDA_FAMILIAR_I = "Informes de proyectos de vida familiar y comunitaria I"
    VIDA_FAMILIAR_II = "Informes de proyectos de vida familiar y comunitaria II"
    VIDA_FAMILIAR_III = "Informes de proyectos de vida familiar y comunitaria III"
    VIDA_FAMILIAR_IV = "Informes de proyectos de vida familiar y comunitaria IV"

class PracticeBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    year: int = Field(..., gt=2000, lt=2100)
    practice_type: PracticeType
    institution: Optional[str] = None
    author: Optional[str] = None
    municipality: Optional[str] = None
    document_path: str

class PracticeCreate(PracticeBase):
    pass

class Practice(PracticeBase):
    id: str
    
    class Config:
        from_attributes = True

class PreviewFragment(BaseModel):
    content: str
    page_number: int
    total_pages: int