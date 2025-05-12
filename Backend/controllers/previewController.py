from fastapi import HTTPException
from models.practiceModel import PracticeModel
from models.previewModels import PreviewModel
from schemas.schemaPractice import PreviewFragment
import PyPDF2
import os
from typing import List

async def generate_preview(practice_id: str) -> List[PreviewFragment]:
    """Genera fragmentos de previsualización para un documento"""
    try:
        existing_preview = await PreviewModel.get_preview(practice_id)
        if existing_preview:
            return [PreviewFragment(**frag) for frag in existing_preview.get("fragments", [])]

        practice = await PracticeModel.get_by_id(practice_id)
        if not practice:
            raise HTTPException(status_code=404, detail="Practice not found")

        # Validar existencia del documento
        document_path = practice.get("document_path")
        if not document_path or not os.path.exists(document_path):
            raise HTTPException(status_code=404, detail="Document file not found")

        # Extraer fragmentos del PDF
        fragments = []
        try:
            with open(document_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                total_pages = len(reader.pages)

                for i in range(min(3, total_pages)):
                    page = reader.pages[i]
                    text = page.extract_text() or "[Contenido no textual]"
                    fragments.append({
                        "content": text[:500] + "..." if len(text) > 500 else text,
                        "page_number": i + 1,
                        "total_pages": total_pages
                    })

                if fragments:
                    await PreviewModel.create_preview(practice_id, fragments)

                return [PreviewFragment(**frag) for frag in fragments]

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing document: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating preview: {str(e)}"
        )