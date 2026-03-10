from fastapi import FastAPI
from app.core.database import engine, Base
from app.modules.auth.controller import router as auth_router
from app.modules.ingestion.controller import router as ingestion_router
from app.modules.analysis.controller import router as analysis_router
from app.modules.simulation.controller import router as simulation_router
from app.modules.recommendation.controller import router as recommendation_router
from app.modules.metrics.controller import router as metrics_router

from app.models.metric import Metric
from app.models.user import User

app = FastAPI(title="Gestor Inteligente de Gastos")

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(ingestion_router)
app.include_router(analysis_router)
app.include_router(simulation_router)
app.include_router(recommendation_router)
app.include_router(metrics_router)


@app.get("/")
def health_check():
    return {"status": "Backend funcionando correctamente"}