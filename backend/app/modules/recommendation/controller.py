# modules/recommendations/controller.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.recommendation.service import generate_recommendations
from app.modules.recommendation.schemas import RecommendationResponse

router = APIRouter(
    prefix="/api/recommendation",
    tags=["Recommendation"]
)


@router.post(
    "/generate",
    response_model=RecommendationResponse,
    status_code=200
)
def recommend(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    try:
        return generate_recommendations(
            db,
            current_user.id
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error generando recomendaciones"
        )