from dataclasses import dataclass

from src.payment_service.commons.payment_data import PaymentData, PaymentType


@dataclass
class PaymentDataValidator:
    def validate(self, payment_data: PaymentData):
        if payment_data.amount <= 0:
            print("Invalid payment data: amount must be positive")
            raise ValueError("Invalid payment data: amount must be positive")
        if payment_data.type == PaymentType.ONLINE:
            if not payment_data.source:
                print("Invalid payment data: missing source")
                raise ValueError("Invalid payment data: missing source")
