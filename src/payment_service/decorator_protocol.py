from typing import Protocol

from src.payment_service.commons.customer import CustomerData
from src.payment_service.commons.payment_data import PaymentData
from src.payment_service.commons.payment_response import PaymentResponse
from src.payment_service.service_protocol import PaymentServiceProtocol


# paso 5, envolver los objetos base de PaymentService con decoradores
# paso 3, definir la interfaz para los decoradores
class PaymentServiceDecoratorProtocol(Protocol):
    wrapped_service: PaymentServiceProtocol

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...

    def process_refund(self, transaction_id: str) -> PaymentResponse: ...

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...
