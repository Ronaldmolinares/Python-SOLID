from typing import Self

from src.payment_service.commons import CustomerData, PaymentData
from src.payment_service.factory import PaymentProcessorFactory
from src.payment_service.notifiers import EmailNotifier, PhoneNotifier
from src.payment_service.notifiers.default_notifier import LogOnlyNotifier
from src.payment_service.processors import PaymentProcessorProtocol
from src.payment_service.validators.customer import CustomerValidator
from src.payment_service.validators.payment import PaymentDataValidator

from .loggers import TransactionLogger
from .notifiers import NotifierProtocol
from .service import PaymentService


class PaymentServiceBuilder:
    payment_processor: PaymentProcessorProtocol | None = None
    notifier: NotifierProtocol | None = None
    customer_validator: CustomerValidator | None = None
    payment_validator: PaymentDataValidator | None = None
    logger: TransactionLogger | None = None
    recurring_processor: PaymentProcessorProtocol | None = None
    refund_processor: PaymentProcessorProtocol | None = None

    def set_logger(self) -> Self:
        self.logger = TransactionLogger()
        return self

    def set_payment_validator(self) -> Self:
        self.payment_validator = PaymentDataValidator()
        return self

    def set_customer_validator(self) -> Self:
        self.customer_validator = CustomerValidator()
        return self

    def set_payment_processor(self, payment_data: PaymentData) -> Self:
        """Crea el procesador de pagos principal."""
        self.payment_processor = PaymentProcessorFactory.create_payment_processor(
            payment_data
        )
        return self

    def set_notifier(self, customer_data: CustomerData) -> Self:
        """Strategy Pattern: Selecciona notificador según contacto."""
        if customer_data.contact_info.email:
            self.notifier = EmailNotifier()
        elif customer_data.contact_info.phone:
            self.notifier = PhoneNotifier(sms_gateway="Twilio")
        else:
            self.notifier = LogOnlyNotifier()
        return self

    def set_recurring_processor(self) -> Self:
        """
        Configura el procesador de pagos recurrentes.

        Reutiliza el payment_processor si tiene el método setup_recurring_payment.
        """
        if not self.payment_processor:
            print("Error: Llamar set_payment_processor() primero")
            return self

        # Verificar si el procesador tiene el método
        if hasattr(self.payment_processor, "setup_recurring_payment"):
            self.recurring_processor = self.payment_processor  # Reutiliza el mismo
            print("Recurring payments: Soportado")
        else:
            self.recurring_processor = None
            print("Recurring payments: No soportado")

        return self

    def set_refund_processor(self) -> Self:
        """
        Configura el procesador de reembolsos.

        Reutiliza el payment_processor si tiene el método refund_payment.
        """
        if not self.payment_processor:
            print("Error: Llamar set_payment_processor() primero")
            return self

        # Verificar si el procesador tiene el método
        if hasattr(self.payment_processor, "refund_payment"):
            self.refund_processor = self.payment_processor  # Reutiliza el mismo
            print("Refunds: Soportado")
        else:
            self.refund_processor = None
            print("Refunds: No soportado")

        return self

    def build(self):
        if not all(
            [
                self.payment_processor,
                self.notifier,
                self.logger,
                self.customer_validator,
                self.payment_validator,
            ]
        ):
            missing = [
                name
                for name, value in [
                    ("payment_processor", self.payment_processor),
                    ("notifier", self.notifier),
                    ("logger", self.logger),
                    ("customer_validator", self.customer_validator),
                    ("payment_validator", self.payment_validator),
                ]
                if value is None
            ]
            raise ValueError(f"Faltan componentes en el builder: {', '.join(missing)}")

        return PaymentService(
            payment_processor=self.payment_processor,
            notifier=self.notifier,
            logger=self.logger,
            customer_validator=self.customer_validator,
            payment_validator=self.payment_validator,
            recurring_processor=self.recurring_processor,
            refund_processor=self.refund_processor,
        )
