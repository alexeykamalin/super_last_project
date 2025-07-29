from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship, Column, func, DateTime
from typing import Optional, List, TYPE_CHECKING

class Prediction(SQLModel, table=True):
    """
    Класс для представления предсказаний.
    
    Attributes:
        id (int): Уникальный идентификатор предсказания
        result (str): Результат предсказания (пока не очень понимаю, какой будет результат, поэтому пока строка :) )
        user (User): Создатель предсказания
        date (str): Дата предсказания
    """
    result: Optional[str] = Field(default=None)
    status: str
    image: str
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(sa_column=Column(DateTime, default=func.now()))
    creator: Optional['User']= Relationship(
        back_populates="predictions"
    )

    
class PredictionUpdate(BaseModel):
    status: str 
    id: int
    result: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": 'in_progress',
                "id": 1,
            }
        }