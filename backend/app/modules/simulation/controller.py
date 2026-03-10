# modules/simulation/controller.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.simulation.schemas import SimulationRequest, SimulationResponse
from app.modules.simulation.service import run_simulation

router = APIRouter(prefix="/api/simulation", tags=["Simulation"])


@router.post("/run", response_model=SimulationResponse)
def simulate(
    request: SimulationRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):

    if request.percentage <= 0 or request.percentage > 100:
        raise HTTPException(
            status_code=400,
            detail="El porcentaje debe estar entre 0 y 100"
        )

    return run_simulation(
        request.category,
        request.percentage,
        user.id,
        db
    )