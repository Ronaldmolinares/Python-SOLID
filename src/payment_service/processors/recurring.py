from typing import Protocol

from src.payment_service.commons import CustomerData, PaymentData, PaymentResponse


class RecurringPaymentProtocol(Protocol):
    """
    Protocolo para configurar pagos recurrentes.

    Este protocolo define la interfaz para programar cobros automáticos periódicos
    (suscripciones). Las implementaciones deben proporcionar un método
    `setup_recurring_payment` que configura la suscripción y retorna un PaymentResponse.
    """

    def setup_recurring_payment(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...
