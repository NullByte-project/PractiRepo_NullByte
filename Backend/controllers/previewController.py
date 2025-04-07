# controllers/preview_controller.py
from fastapi import HTTPException
import PyPDF2

from models.practiceModel import PracticeModel

async def generate_preview(practice_id: str):
    practice = PracticeModel.get_by_id(practice_id)
    if not practice:
        raise HTTPException(404, "Práctica no encontrada")
    
    try:
        with open(practice["document_path"], "rb") as file:
            reader = PyPDF2.PdfReader(file)
            first_page = reader.pages[0]
            content = first_page.extract_text()[:500] + "..."  # Limitar a 500 caracteres
            
            return {
                "content": content,
                "page_number": 1,
                "total_pages": len(reader.pages)
            }
    except Exception as e:
        raise HTTPException(500, f"No se pudo generar previsualización: {str(e)}")