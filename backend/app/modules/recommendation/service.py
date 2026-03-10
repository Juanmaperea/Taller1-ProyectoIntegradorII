# modules/recommendations/service.py

from sqlalchemy.orm import Session
from app.modules.analysis.service import calculate_summary
from app.modules.recommendation.prompt_builder import build_prompt
from app.modules.recommendation.llm_service import call_gemini
from app.utils.json_validator import validate_json_response
from app.utils.financial_validator import validate_projected_savings
from app.modules.metrics.service import log_usage
from app.modules.recommendation.schemas import RecommendationResponse


def generate_recommendations(db: Session, user_id: int):

    # 1. Obtener análisis financiero del usuario
    summary = calculate_summary(db, user_id)

    summary_dict = summary.model_dump()  # pydantic v2

    real_total = summary.total_expenses

    # 2. Construir prompt
    prompt = build_prompt(summary_dict)

    # 3. Llamar al modelo IA
    response = call_gemini(prompt)

    text_output = response.text

    if not text_output:
        raise ValueError("La IA no devolvió respuesta")

    # 4. Validar JSON
    validated = validate_json_response(text_output)

    # 5. Mitigar alucinaciones numéricas
    validated = validate_projected_savings(validated, real_total)

    # 6. Registrar uso de tokens
    tokens_used = getattr(response.usage_metadata, "total_token_count", 0)

    log_usage(
        db,
        tokens_used,
        operation="recommendation_generation"
    )

    return RecommendationResponse(**validated)