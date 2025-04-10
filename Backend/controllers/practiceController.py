from fastapi import HTTPException, UploadFile
from models.practiceModel import PracticeModel
from schemas.schemaPractice import Practice
from typing import List, Optional
import os
from pathlib import Path
from datetime import datetime
import shutil
import mimetypes

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper Functions


async def save_uploaded_file(file: UploadFile) -> str:
    try:
        file_type = mimetypes.guess_type(file.filename)[0]
        if file_type not in ['application/pdf', 'application/msword',
                             'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            raise ValueError("Formato de archivo no permitido")

        timestamp = int(datetime.now().timestamp())
        file_ext = Path(file.filename).suffix
        safe_filename = f"{timestamp}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path
    except Exception as e:
        raise HTTPException(400, f"Error al guardar archivo: {str(e)}")


def delete_file(file_path: str) -> bool:
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False

# CRUD Operations


async def create_practice(
    title: str,
    year: int,
    practice_type: str,
    file: UploadFile,
    institution: Optional[str] = None,
    author: Optional[str] = None,
    municipality: Optional[str] = None
) -> Practice:
    try:
        file_path = await save_uploaded_file(file)

        practice_data = {
            "title": title,
            "year": year,
            "practice_type": practice_type,
            "institution": institution,
            "author": author,
            "municipality": municipality,
            "document_path": file_path,
            "uploaded_at": datetime.utcnow()
        }

        practice_id = await PracticeModel.create(practice_data)
        return Practice(**practice_data, id=practice_id)

    except HTTPException:
        raise
    except Exception as e:
        if 'file_path' in locals():
            delete_file(file_path)
        raise HTTPException(500, f"Error al crear práctica: {str(e)}")


async def get_practice(practice_id: str) -> Practice:
    try:
        practice = await PracticeModel.get_by_id(practice_id)
        if not practice:
            raise HTTPException(404, "Práctica no encontrada")

        practice["id"] = str(practice["_id"])
        return Practice(**practice)
    except Exception as e:
        raise HTTPException(500, f"Error al obtener práctica: {str(e)}")


async def get_all_practices() -> List[Practice]:
    try:
        practices = await PracticeModel.get_all()
        result = []

        for practice in practices:
            practice_data = {
                "id": str(practice["_id"]),
                "title": practice.get("title", ""),
                "year": practice.get("year", 2000),
                "practice_type": practice.get("practice_type", "Informes de práctica institucional II"),
                "institution": practice.get("institution"),
                "author": practice.get("author"),
                "municipality": practice.get("municipality"),
                "document_path": practice.get("document_path", ""),
                "uploaded_at": practice.get("uploaded_at", datetime.utcnow())
            }

            try:
                validated_practice = Practice(**practice_data)
                result.append(validated_practice)
            except Exception as validation_error:
                print(
                    f"Error validando práctica {practice['_id']}: {validation_error}")
                continue

        return result
    except Exception as e:
        raise HTTPException(500, f"Error al obtener prácticas: {str(e)}")


async def get_practices_by_type(practice_type: str) -> List[Practice]:
    try:
        practices = await PracticeModel.get_by_type(practice_type)
        return [Practice(**practice, id=str(practice["_id"])) for practice in practices]
    except Exception as e:
        raise HTTPException(500, f"Error al obtener prácticas: {str(e)}")


async def update_practice(
    practice_id: str,
    title: Optional[str] = None,
    year: Optional[int] = None,
    practice_type: Optional[str] = None,
    institution: Optional[str] = None,
    author: Optional[str] = None,
    municipality: Optional[str] = None,
    file: Optional[UploadFile] = None
) -> Practice:
    try:
        practice = await PracticeModel.get_by_id(practice_id)
        if not practice:
            raise HTTPException(404, "Práctica no encontrada")

        update_data = {}
        old_file_path = practice.get("document_path")
        new_file_path = None

        if title:
            update_data["title"] = title
        if year:
            update_data["year"] = year
        if practice_type:
            update_data["practice_type"] = practice_type
        if institution:
            update_data["institution"] = institution
        if author:
            update_data["author"] = author
        if municipality:
            update_data["municipality"] = municipality

        if file:
            new_file_path = await save_uploaded_file(file)
            update_data["document_path"] = new_file_path

        if update_data:
            updated = await PracticeModel.update(practice_id, update_data)
            if not updated:
                if new_file_path:
                    delete_file(new_file_path)
                raise HTTPException(500, "Error al actualizar práctica")

            if file and old_file_path:
                delete_file(old_file_path)

        return await get_practice(practice_id)

    except HTTPException:
        raise
    except Exception as e:
        if 'new_file_path' in locals() and new_file_path:
            delete_file(new_file_path)
        raise HTTPException(500, f"Error al actualizar práctica: {str(e)}")


async def delete_practice(practice_id: str) -> dict:
    try:
        practice = await PracticeModel.get_by_id(practice_id)
        if not practice:
            raise HTTPException(404, "Práctica no encontrada")

        file_path = practice.get("document_path")
        if file_path:
            delete_file(file_path)

        deleted = await PracticeModel.delete(practice_id)
        if not deleted:
            raise HTTPException(500, "Error al eliminar práctica")

        return {"message": "Práctica eliminada correctamente", "id": practice_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error al eliminar práctica: {str(e)}")
# implementar filtros para mostrar practicas


async def get_practices_by_filters(
    title: Optional[str] = None,
    year: Optional[int] = None,
    municipality: Optional[str] = None,
    practice_type: Optional[str] = None,
    institution: Optional[str] = None,
    author: Optional[str] = None

) -> List[Practice]:
    filters = {}
    if title:
        filters["title"] = title
    if year:
        filters["year"] = year
    if municipality:
        filters["municipality"] = municipality
    if practice_type:
        filters["practice_type"] = practice_type
    if institution:
        filters["institution"] = institution
    if author:
        filters["author"] = author

    try:
        # Filtrar manualmente si PracticeModel.get_all no soporta filtros
        all_practices = await PracticeModel.get_all()
        filtered_practices = [
            practice for practice in all_practices
            if all(
                practice.get(key) == value
                for key, value in filters.items()
                if value is not None
            )
        ]
        return [Practice(**practice, id=str(practice["_id"])) for practice in filtered_practices]
    except Exception as e:
        raise HTTPException(500, f"Error al obtener prácticas: {str(e)}")
