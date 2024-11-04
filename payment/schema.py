from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class PaymentStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    INVALID_CARD = "invalid_card"
    FAILED = "failed"

class CardData(BaseModel):
    name: str
    number: str
    cvv: str
    expiry_date: str

class PaymentResponse(BaseModel):
    payment_id: str
    status: PaymentStatus
    amount: float
    currency: str
    timestamp: str
    description: Optional[str] = None
    email: EmailStr
    name: str
    error_message: Optional[str] = None
