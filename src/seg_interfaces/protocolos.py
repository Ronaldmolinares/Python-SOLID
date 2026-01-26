from typing import Protocol

from .payment_data import CustomerData, PaymentData, PaymentResponse


class PaymentProcessorProtocol(Protocol):
    """
    Protocol for processing payments.

    This protocol defines the interface for payment processors. Implementations
    should provide a method `process_transaction` that takes customer data and payment data,
    and returns a Stripe Charge object.
    """

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...


class RefundPaymentProtocol(Protocol):
    """Gestiona devoluciones de dinero"""

    def refund_payment(self, transaction_id: str) -> PaymentResponse: ...


class RecurringPaymentProtocol(Protocol):
    """Se encarga de programar cobros automáticos periódicos."""

    def setup_recurring_payment(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...
