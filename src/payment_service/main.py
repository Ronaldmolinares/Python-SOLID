from src.payment_service.commons import (
    ContactInfo,
    CustomerData,
    PaymentData,
)
from src.payment_service.validators.customer import CustomerValidator
from src.payment_service.validators.payment import PaymentDataValidator

from .loggers import TransactionLogger
from .notifiers import EmailNotifier
from .processors import StripePaymentProcessor
from .service import PaymentService

if __name__ == "__main__":
    stripe_payment_processor = StripePaymentProcessor()
    email_notifier = EmailNotifier()
    customer_validator = CustomerValidator()
    payment_data_validator = PaymentDataValidator()
    logger = TransactionLogger()

    service = PaymentService(
        payment_processor=stripe_payment_processor,
        notifier=email_notifier,
        logger=logger,
        customer_validator=customer_validator,
        payment_validator=payment_data_validator,
    )

    # Datos de prueba
    customer_data = CustomerData(
        name="John Doe", contact_info=ContactInfo(email="john@example.com")
    )

    payment_data = PaymentData(amount=5000, source="tok_visa")

    # Procesar transacción
    try:
        response = service.process_transaction(customer_data, payment_data)
        print(f"✅ Payment Status: {response.status}")
        print(f"   Amount: ${response.amount / 100:.2f}")
        print(f"   Transaction ID: {response.transaction_id}")
    except Exception as e:
        print(f"❌ Error: {e}")
