from dataclasses import dataclass

from stripe import StripeError

from .customer_validator import CustomerValidator, PaymentDataValidator
from .notifier import Notifier
from .payment_data import CustomerData, PaymentData, PaymentResponse
from .protocolos import (
    PaymentProcessorProtocol,
    RecurringPaymentProtocol,
    RefundPaymentProtocol,
)
from .transaction_logger import TransactionLogger


@dataclass
class PaymentService:
    payment_processor: PaymentProcessorProtocol
    notifier: Notifier
    customer_validator: CustomerValidator
    payment_validator: PaymentDataValidator
    logger: TransactionLogger
    recurring_processor: RecurringPaymentProtocol | None = None
    refund_processor: RefundPaymentProtocol | None = None

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        """Procesa un pago único"""
        try:
            self.customer_validator.validate_data(customer_data)
            self.payment_validator.validate(payment_data)
        except ValueError as e:
            raise e

        try:
            payment_response = self.payment_processor.process_transaction(
                customer_data, payment_data
            )
            self.notifier.send_confirmation(customer_data)
            self.logger.log(customer_data, payment_data, payment_response)
            return payment_response

        except StripeError as e:
            raise e

    def process_refund(self, transaction_id: str) -> PaymentResponse:
        """Procesa un reembolso de un pago previo"""
        if not self.refund_processor:
            raise NotImplementedError("Refunds not supported by this processor")

        try:
            refund_response = self.refund_processor.refund_payment(transaction_id)
            self.logger.log_refund(transaction_id, refund_response)
            return refund_response

        except StripeError as e:
            raise e

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        """Configura un pago recurrente (suscripción)"""
        if not self.recurring_processor:
            raise NotImplementedError(
                "Recurring payments not supported by this processor"
            )

        try:
            self.customer_validator.validate_data(customer_data)
            self.payment_validator.validate(payment_data)
        except ValueError as e:
            raise e

        try:
            recurring_response = self.recurring_processor.setup_recurring_payment(
                customer_data, payment_data
            )
            self.notifier.send_confirmation(customer_data)
            self.logger.log(customer_data, payment_data, recurring_response)
            return recurring_response

        except StripeError as e:
            raise e
