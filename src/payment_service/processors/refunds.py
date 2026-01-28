from typing import Protocol

from src.payment_service.commons.payment_response import PaymentResponse


class RefundPaymentProtocol(Protocol):
    """
    Protocolo para gestionar reembolsos.

    Este protocolo define la interfaz para procesar devoluciones de dinero.
    Las implementaciones deben proporcionar un método `refund_payment` que toma
    el ID de una transacción y retorna un objeto PaymentResponse.
    """

    def refund_payment(self, transaction_id: str) -> PaymentResponse: ...
