import uuid
from dataclasses import dataclass

from src.payment_service.commons import CustomerData, PaymentData, PaymentResponse

from .payment import PaymentProcessorProtocol
from .recurring import RecurringPaymentProtocol
from .refunds import RefundPaymentProtocol


@dataclass
class LocalPaymentProcessor(
    PaymentProcessorProtocol, RecurringPaymentProtocol, RefundPaymentProtocol
):
    """
    Procesador de pagos local para pruebas.

    Implementa los tres protocolos (payment, recurring, refund) con lógica
    simplificada sin integración a pasarelas reales.
    """

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        """Simula un pago único exitoso."""
        print(f"Processing local payment for {customer_data.name}")

        return PaymentResponse(
            status="succeeded",
            amount=payment_data.amount,
            transaction_id=f"LOCAL-{uuid.uuid4().hex[:12].upper()}",
            message="Local payment processed successfully",
        )

    def setup_recurring_payment(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        """Simula la configuración de un pago recurrente."""
        print(f"Setting up recurring payment for {customer_data.name}")

        return PaymentResponse(
            status="active",
            amount=payment_data.amount,
            transaction_id=f"LOCAL-SUB-{uuid.uuid4().hex[:12].upper()}",
            message="Recurring payment setup successfully",
        )

    def refund_payment(self, transaction_id: str) -> PaymentResponse:
        """Simula un reembolso exitoso."""
        print(f"Processing refund for transaction {transaction_id}")

        return PaymentResponse(
            status="refunded",
            amount=0,  # En un caso real, obtendrías el monto de una base de datos
            transaction_id=f"LOCAL-REFUND-{uuid.uuid4().hex[:12].upper()}",
            message="Refund processed successfully",
        )
