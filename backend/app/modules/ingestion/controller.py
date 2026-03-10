# modules/ingestion/controller.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.ingestion.service import process_excel
from app.modules.ingestion.schemas import UploadResponse
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/api/ingestion",
    tags=["Ingestion"]
)


@router.post("/upload", response_model=UploadResponse)
def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten archivos .xlsx"
        )

    try:
        records = process_excel(
            file.file,
            db,
            current_user.id
        )

        return UploadResponse(
            message="Archivo procesado correctamente",
            records_inserted=records
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )