from typing import Protocol

from .payment_data import CustomerData, PaymentData, PaymentResponse


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


class RefundPaymentProtocol(Protocol):
    """
    Protocolo para gestionar reembolsos.

    Este protocolo define la interfaz para procesar devoluciones de dinero.
    Las implementaciones deben proporcionar un método `refund_payment` que toma
    el ID de una transacción y retorna un objeto PaymentResponse.
    """

    def refund_payment(self, transaction_id: str) -> PaymentResponse: ...


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
