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
    status: str = Field(default='in_progress')
    a1: Optional[int] = Field(default=None)
    a2: Optional[int] = Field(default=None)
    a3: Optional[int] = Field(default=None)
    ag: Optional[int] = Field(default=None)
    g1: Optional[int] = Field(default=None)
    g2: Optional[int] = Field(default=None)
    g3: Optional[int] = Field(default=None)
    gg: Optional[int] = Field(default=None)
    i1: Optional[int] = Field(default=None)
    i2: Optional[int] = Field(default=None)
    i3: Optional[int] = Field(default=None)
    ia: Optional[int] = Field(default=None)
    ig: Optional[int] = Field(default=None)
    f1: Optional[int] = Field(default=None)
    f2: Optional[int] = Field(default=None)
    f3: Optional[int] = Field(default=None)
    fa: Optional[int] = Field(default=None)
    fg: Optional[int] = Field(default=None)
    r1: Optional[int] = Field(default=None)
    r2: Optional[int] = Field(default=None)
    r3: Optional[int] = Field(default=None)
    ra: Optional[int] = Field(default=None)
    rg: Optional[int] = Field(default=None)
    pri: Optional[int] = Field(default=None)
    prm: Optional[int] = Field(default=None)
    prf: Optional[int] = Field(default=None)
    prr: Optional[int] = Field(default=None)
    egkr: Optional[int] = Field(default=None)
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