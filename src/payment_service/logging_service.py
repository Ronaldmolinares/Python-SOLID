from dataclasses import dataclass

from src.payment_service.commons.customer import CustomerData
from src.payment_service.commons.payment_data import PaymentData
from src.payment_service.commons.payment_response import PaymentResponse
from src.payment_service.decorator_protocol import PaymentServiceDecoratorProtocol
from src.payment_service.service_protocol import PaymentServiceProtocol


@dataclass
class PaymentServiceLogging(PaymentServiceDecoratorProtocol):
    wrapped_service: PaymentServiceProtocol

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        print("Starting to process transaction")
        response = self.wrapped_service.process_transaction(customer_data, payment_data)
        print("Finished processing transaction")
        return response

    def process_refund(self, transaction_id: str) -> PaymentResponse:
        print(f"Start process refund using: {transaction_id}")
        response = self.wrapped_service.process_refund(transaction_id)
        print("Finish process refund")
        return response

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        print("Starting to process recurring payment")
        response = self.wrapped_service.setup_recurring(customer_data, payment_data)
        print("Finished processing recurring payment")
        return response
