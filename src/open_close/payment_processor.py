import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

import stripe
from dotenv import load_dotenv
from stripe import Charge

from .payment_data import CustomerData, PaymentData

_ = load_dotenv()


class PaymentProcessor(ABC):
    @abstractmethod
    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> Charge: ...


@dataclass
class StripePaymentProcessor(PaymentProcessor):
    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> Charge:
        stripe.api_key = os.getenv("STRIPE_API_KEY")

        try:
            charge = stripe.Charge.create(
                amount=payment_data.amount,
                currency="usd",
                source=payment_data.source,
                description="Charge for " + customer_data.name,
            )
            print("Payment successful")

        except stripe.StripeError as e:
            print("Payment failed:", e)
            raise e

        return charge
