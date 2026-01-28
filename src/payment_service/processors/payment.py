from typing import Protocol

from src.payment_service.commons import (
    CustomerData,
    PaymentData,
    PaymentResponse,
)


class PaymentProcessorProtocol(Protocol):
    """
    Protocolo para procesar pagos únicos.

    Este protocolo define la interfaz para procesadores de pago. Las implementaciones
    deben proporcionar un método `process_transaction` que toma datos del cliente y
    datos de pago, y retorna un objeto PaymentResponse.
    """

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...
