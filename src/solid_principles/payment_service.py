from dataclasses import dataclass, field

from stripe import Charge, StripeError

from .customer_validation import CustomerValidator
from .notifier import Notifier
from .payment_data_validation import PaymentDataValidator
from .payment_processor import PaymentProcessor
from .transaction_logger import TransactionLogger


@dataclass
class PaymentService:
    customer_validation: CustomerValidator = field(default_factory=CustomerValidator)
    payment_data_validation: PaymentDataValidator = field(
        default_factory=PaymentDataValidator
    )
    payment_processor: PaymentProcessor = field(default_factory=PaymentProcessor)
    notifier: Notifier = field(default_factory=Notifier)
    logger: TransactionLogger = field(default_factory=TransactionLogger)

    def process_transaction(self, customer_data, payment_data) -> Charge:
        try:
            self.customer_validation.validate_data(customer_data)
        except ValueError as e:
            raise e

        try:
            self.payment_data_validation.payment_validation(payment_data)
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


if __name__ == "__main__":
    payment_processor = PaymentService()

    customer_data_with_email = {
        "name": "Laura Molina",
        "contact_info": {"email": "laura@gmail.com"},
    }
    customer_data_with_phone = {
        "name": "Platzi Python",
        "contact_info": {"phone": "1234567890"},
    }

    # Camino Feliz
    payment_data = {"amount": 500, "source": "tok_mastercard", "cvv": 123}

    payment_processor.process_transaction(customer_data_with_email, payment_data)
    payment_processor.process_transaction(customer_data_with_phone, payment_data)

    # Camino no tan feliz por usar tok_radarBlock
    # payment_data = {"amount": 150, "source": "tok_radarBlock", "cvv": 456}
    # payment_processor.process_transaction(customer_data_with_email, payment_data)
