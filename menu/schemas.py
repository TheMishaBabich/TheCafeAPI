
from pydantic import BaseModel, ConfigDict
from typing import List

class DishResponse(BaseModel):
    id: int
    category: str
    title: str
    description: str
    price: float

    model_config = ConfigDict(from_attributes=True)