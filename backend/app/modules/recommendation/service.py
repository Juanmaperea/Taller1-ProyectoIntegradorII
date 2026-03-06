from typing import List, Optional
from abc import ABC, abstractmethod
from datetime import datetime
from app.modules.recommendation.models import Recommendation
from app.modules.recommendation.schemas import RecommendationSchema, CreateRecommendationSchema
from app.core.exceptions import NotFoundError, ValidationError

class RecommendationService(ABC):
    """Abstract base class for recommendation service"""
    
    @abstractmethod
    def get_all_recommendations(self, skip: int = 0, limit: int = 10) -> List[RecommendationSchema]:
        pass
    
    @abstractmethod
    def get_recommendation_by_id(self, recommendation_id: int) -> RecommendationSchema:
        pass
    
    @abstractmethod
    def create_recommendation(self, data: CreateRecommendationSchema) -> RecommendationSchema:
        pass
    
    @abstractmethod
    def update_recommendation(self, recommendation_id: int, data: CreateRecommendationSchema) -> RecommendationSchema:
        pass
    
    @abstractmethod
    def delete_recommendation(self, recommendation_id: int) -> bool:
        pass


class RecommendationServiceImpl(RecommendationService):
    """Implementation of recommendation service"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def get_all_recommendations(self, skip: int = 0, limit: int = 10) -> List[RecommendationSchema]:
        recommendations = self.db.query(Recommendation).offset(skip).limit(limit).all()
        return [RecommendationSchema.from_orm(rec) for rec in recommendations]
    
    def get_recommendation_by_id(self, recommendation_id: int) -> RecommendationSchema:
        recommendation = self.db.query(Recommendation).filter(
            Recommendation.id == recommendation_id
        ).first()
        
        if not recommendation:
            raise NotFoundError(f"Recommendation with id {recommendation_id} not found")
        
        return RecommendationSchema.from_orm(recommendation)
    
    def create_recommendation(self, data: CreateRecommendationSchema) -> RecommendationSchema:
        new_recommendation = Recommendation(**data.dict())
        new_recommendation.created_at = datetime.utcnow()
        
        self.db.add(new_recommendation)
        self.db.commit()
        self.db.refresh(new_recommendation)
        
        return RecommendationSchema.from_orm(new_recommendation)
    
    def update_recommendation(self, recommendation_id: int, data: CreateRecommendationSchema) -> RecommendationSchema:
        recommendation = self.db.query(Recommendation).filter(
            Recommendation.id == recommendation_id
        ).first()
        
        if not recommendation:
            raise NotFoundError(f"Recommendation with id {recommendation_id} not found")
        
        for key, value in data.dict(exclude_unset=True).items():
            setattr(recommendation, key, value)
        
        recommendation.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(recommendation)
        
        return RecommendationSchema.from_orm(recommendation)
    
    def delete_recommendation(self, recommendation_id: int) -> bool:
        recommendation = self.db.query(Recommendation).filter(
            Recommendation.id == recommendation_id
        ).first()
        
        if not recommendation:
            raise NotFoundError(f"Recommendation with id {recommendation_id} not found")
        
        self.db.delete(recommendation)
        self.db.commit()
        
        return True