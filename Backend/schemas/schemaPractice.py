from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

# Enumeración que define los tipos posibles de práctica
class PracticeType(str, Enum):
    INSTITUCIONAL_I = "Informes de práctica institucional I"
    INSTITUCIONAL_II = "Informes de práctica institucional II"
    VIDA_FAMILIAR_I = "Informes de proyectos de vida familiar y comunitaria I"
    VIDA_FAMILIAR_II = "Informes de proyectos de vida familiar y comunitaria II"
    VIDA_FAMILIAR_III = "Informes de proyectos de vida familiar y comunitaria III"
    VIDA_FAMILIAR_IV = "Informes de proyectos de vida familiar y comunitaria IV"

# Esquema base para representar una práctica académica
class PracticeBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)  # Título de la práctica
    year: int = Field(..., gt=2000, lt=2100)  # Año de elaboración, entre 2001 y 2099
    practice_type: PracticeType  # Tipo de práctica, según la enumeración
    institution: Optional[str] = None  # Institución relacionada (opcional)
    author: Optional[str] = None  # Autor de la práctica (opcional)
    municipality: Optional[str] = None  # Municipio relacionado (opcional)
    document_path: str  # Ruta del archivo/documento asociado

# Esquema para creación de una práctica (igual al base)
class PracticeCreate(PracticeBase):
    pass

# Esquema que incluye el ID de la práctica (respuesta al cliente)
class Practice(BaseModel):
    id: str  # Identificador único de la práctica
    title: str
    year: int
    practice_type: PracticeType
    institution: Optional[str] = None
    author: Optional[str] = None
    municipality: Optional[str] = None
    document_path: str

    class Config:
        from_attributes = True  # Permite cargar el modelo desde atributos de un ORM

# Esquema para representar un fragmento de previsualización de un documento
class PreviewFragment(BaseModel):
    content: str  # Contenido extraído de la página
    page_number: int  # Número de página del fragmento
    total_pages: int  # Total de páginas del documento
