from sqlmodel import SQLModel, Field, Relationship, Column, func, DateTime
from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import re

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, min_length=5, max_length=255)
    password: str = Field(min_length=8)
    name: str = Field(min_length=2)
    hashed_name: str = Field(min_length=32)
    created_at: datetime = Field(sa_column=Column(DateTime, default=func.now()))
    is_admin: bool = Field(default=False)
    status: int = Field(default=1)
    transactions: Optional[List["Transaction"]] = Relationship(
        back_populates="creator",
    )
    predictions: Optional[List["Prediction"]] = Relationship(
        back_populates="creator",
    )
    balance: Optional["Balance"] = Relationship(
        back_populates="creator",
    )

    
    def validate_email(self) -> bool:
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not pattern.match(self.email):
            raise ValueError("Invalid email format")
        return True

    @property
    def tranaction_count(self) -> int:
        """Number of events associated with user"""
        return len(self.tranaction)

    class Config:
        """Model configuration"""
        validate_assignment = True
        arbitrary_types_allowed = True

class UserSignup(BaseModel):
    name: str 
    email: str
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "user@example.com",
                "password": "strongpassword123",
            }
        }
class DeleteUser(BaseModel):
    id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
            }
        }

class TokenResponse(BaseModel): 
    access_token: str 
    token_type: str