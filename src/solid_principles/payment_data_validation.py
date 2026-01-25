from dataclasses import dataclass


@dataclass
class PaymentDataValidator:
    def payment_validation(self, payment_data):
        if not payment_data.get("source"):
            raise ValueError("Invalid payment data")
