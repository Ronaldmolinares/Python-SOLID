import os
from dataclasses import dataclass
from typing import Protocol

import stripe
from dotenv import load_dotenv
from stripe import Charge

from .payment_data import CustomerData, PaymentData

_ = load_dotenv()


class PaymentProcessor(Protocol):
    """
    Protocol for processing payments.

    This protocol defines the interface for payment processors. Implementations
    should provide a method `process_transaction` that takes customer data and payment data,
    and returns a Stripe Charge object.
    """

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> Charge:
        """Process a payment.

        :param customer_data: Data about the customer making the payment.
        :type customer_data: CustomerData
        :param payment_data: Data about the payment to process.
        :type payment_data: PaymentData
        :return: A Stripe Charge object representing the processed payment.
        :rtype: Charge
        """
        ...


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
