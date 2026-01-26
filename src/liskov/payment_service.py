from dataclasses import dataclass, field

from stripe import Charge, StripeError

from .customer_validator import CustomerValidator
from .notifier import EmailNotifier, Notifier
from .payment_data import CustomerData, PaymentData
from .payment_processor import PaymentProcessor, StripePaymentProcessor
from .transaction_logger import TransactionLogger


@dataclass
class PaymentService:
    customer_validator: CustomerValidator = field(default_factory=CustomerValidator)
    payment_processor: PaymentProcessor = field(default_factory=StripePaymentProcessor)
    notifier: Notifier = field(default_factory=EmailNotifier)
    logger = TransactionLogger()

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> Charge:
        try:
            self.customer_validator.validate_data(customer_data)
        except ValueError as e:
            raise e

        try:
            charge = self.payment_processor.process_transaction(
                customer_data, payment_data
            )
            self.notifier.send_confirmation(customer_data)
            self.logger.log(customer_data, payment_data, charge)

            return charge

        except StripeError as e:
            raise e
