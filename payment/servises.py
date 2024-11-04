import random
import uuid
from datetime import datetime

from fastapi import HTTPException
from paypalrestsdk.openid_connect import client_id
from sqlalchemy.testing.plugin.plugin_base import config

from config import SECRET_PAYMENT, CLIENT_ID_PAYMENT
from payment import repository
from payment.schema import PaymentResponse, PaymentStatus, CardData
from payment.utils import validate_card_data
from repository import PaymentRepository


class MokePaymentService:
    def __init__(self, repository):
        self.repository = repository
        self.payments = {}

    def process_payment_result(self) -> tuple[PaymentStatus, str]:
        random_number = random.random() * 100

        if random_number < 80:
            return PaymentStatus.SUCCESS, "Payment successful"
        elif random_number < 90:
            return PaymentStatus.INSUFFICIENT_FUNDS, "Insufficient funds on the card"
        else:
            return PaymentStatus.INVALID_CARD, "Invalid card data"

    async def create_payment(self, amount: float, email: str, name: str, description: str = None) -> PaymentResponse:
        payment_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        payment = PaymentResponse(
            payment_id=payment_id,
            status=PaymentStatus.PENDING,
            amount=amount,
            currency="UAH",
            timestamp=timestamp,
            description=description,
            email=email,
            name=name
        )

        self.payments[payment_id] = payment
        return payment

    async def process_card_payment(
        self,
        payment_id: str,
        card_data: CardData
    ) -> PaymentResponse:
        payment = self.payments.get(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found!")

        is_valid, error_message = validate_card_data(card_data)
        if not is_valid:
            payment.status = PaymentStatus.INVALID_CARD
            payment.error_message = error_message
            return payment

        status, message = self.process_payment_result()
        payment.status = status
        payment.error_message = None if status == PaymentStatus.SUCCESS else message

        await self.repository.update_payment(
            payment_id=payment_id,
            status=status.value,
            error_message=payment.error_message
        )

        return payment