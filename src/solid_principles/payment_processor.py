import os
from dataclasses import dataclass

import stripe
from dotenv import load_dotenv
from stripe import Charge

_ = load_dotenv()


@dataclass
class PaymentProcessor:
    def process_transaction(self, customer_data, payment_data) -> Charge:
        stripe.api_key = os.getenv("STRIPE_API_KEY")

        # Responsabilidad de Procesamiento de Pago
        try:
            charge = stripe.Charge.create(
                amount=payment_data["amount"],
                currency="usd",
                source=payment_data["source"],
                description="Charge for " + customer_data["name"],
            )
            print("Payment successful")

        except stripe.StripeError as e:
            print("Payment failed:", e)
            raise e

        return charge
