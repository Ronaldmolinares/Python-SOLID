from dataclasses import dataclass, field

from src.seg_interfaces.protocolos import (
    PaymentProcessorProtocol,
    RecurringPaymentProtocol,
    RefundPaymentProtocol,
)

from .customer_validator import CustomerValidator, PaymentDataValidator
from .notifier import Notifier
from .payment_data import CustomerData, PaymentData, PaymentResponse
from .transaction_logger import TransactionLogger


@dataclass
class PaymentService:
    payment_processor: PaymentProcessorProtocol
    notifier: Notifier
    customer_validator: CustomerValidator = field(default_factory=CustomerValidator)
    payment_validator: PaymentDataValidator = field(
        default_factory=PaymentDataValidator
    )
    recurring_processor: RecurringPaymentProtocol | None = None
    refund_processor: RefundPaymentProtocol | None = None
    logger: TransactionLogger = field(default_factory=TransactionLogger)

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        self.customer_validator.validate_data(customer_data)
        self.payment_validator.validate(payment_data)
        payment_response = self.payment_processor.process_transaction(
            customer_data, payment_data
        )
        self.notifier.send_confirmation(customer_data)
        self.logger.log(customer_data, payment_data, payment_response)
        return payment_response

    def process_refund(self, transaction_id: str):
        if not self.refund_processor:
            raise Exception("this processor does not support refunds")
        refund_response = self.refund_processor.refund_payment(transaction_id)
        self.logger.log_refund(transaction_id, refund_response)
        return refund_response

    def setup_recurring(self, customer_data: CustomerData, payment_data: PaymentData):
        if not self.recurring_processor:
            raise Exception("this processor does not support recurring")
        recurring_response = self.recurring_processor.setup_recurring_payment(
            customer_data, payment_data
        )
        self.logger.log(customer_data, payment_data, recurring_response)
        return recurring_response
