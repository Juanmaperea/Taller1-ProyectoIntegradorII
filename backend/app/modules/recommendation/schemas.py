from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class RecommendationBase(BaseModel):
    """Base schema for expense recommendations"""
    category: str = Field(..., description="Expense category")
    amount: float = Field(..., gt=0, description="Amount spent")
    description: str = Field(..., description="Expense description")
    date: datetime = Field(default_factory=datetime.now, description="Date of expense")


class RecommendationCreate(RecommendationBase):
    """Schema for creating new recommendations"""
    pass


class RecommendationResponse(RecommendationBase):
    """Schema for recommendation responses"""
    id: int
    llm_insight: str = Field(description="LLM-generated insight about the expense")
    recommendation: str = Field(description="Recommendation to improve spending")
    risk_level: str = Field(description="Risk level: low, medium, high")
    
    class Config:
        from_attributes = True


class BudgetAnalysis(BaseModel):
    """Schema for overall budget analysis"""
    total_spending: float
    by_category: dict[str, float]
    average_transaction: float
    llm_summary: str = Field(description="LLM-generated budget summary")
    key_recommendations: List[str] = Field(description="List of key recommendations")


class ExpenseSummary(BaseModel):
    """Schema for expense summary with recommendations"""
    period: str
    recommendations: List[RecommendationResponse]
    analysis: BudgetAnalysis