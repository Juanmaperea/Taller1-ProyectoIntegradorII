# modules/simulation/service.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.expense import Expense
from app.modules.simulation.schemas import (
    SimulationResponse,
    CategoryProjection
)


def run_simulation(category: str, percentage: float, user_id: int, db: Session) -> SimulationResponse:

    # Total general del usuario
    original_total = (
        db.query(func.sum(Expense.amount))
        .filter(Expense.user_id == user_id)
        .scalar()
    ) or 0

    # Totales por categoría del usuario
    category_data = (
        db.query(Expense.category, func.sum(Expense.amount))
        .filter(Expense.user_id == user_id)
        .group_by(Expense.category)
        .all()
    )

    projections = []
    projected_total = 0

    for cat, total in category_data:

        total = float(total)

        if cat == category:
            reduced_amount = total * (percentage / 100)
            new_total = total - reduced_amount
        else:
            new_total = total

        projected_total += new_total

        projections.append(
            CategoryProjection(
                category=cat or "Sin categoría",
                original_total=total,
                projected_total=new_total
            )
        )

    estimated_savings = original_total - projected_total

    return SimulationResponse(
        original_total_expenses=float(original_total),
        projected_total_expenses=float(projected_total),
        estimated_savings=float(estimated_savings),
        category_projection=projections
    )