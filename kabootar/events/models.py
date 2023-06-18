"""
Models for events
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

class Event(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }