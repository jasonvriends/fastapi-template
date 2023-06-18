import uuid
from datetime import datetime
from typing import List, Optional
from zoneinfo import ZoneInfo

import motor.motor_asyncio
from beanie import Document, Indexed
from pydantic import BaseModel, validator


class Cat(Document):
    name: str
    description: str
    user_id: Optional[uuid.UUID] = None
    created_on: datetime

    class Config:
        schema_extra = {
            "example": {
                "name": "Garfield",
                "description": "A cat who loves to eat.",
                "created_on": datetime.now(),
            }
        }

    class Settings:
        name = "cats"
