from dataclasses import dataclass
from typing import Self

from stripe import StripeError

from src.payment_service.commons import (
    CustomerData,
    PaymentData,
    PaymentResponse,
    Request,
)
from src.payment_service.factory import PaymentProcessorFactory
from src.payment_service.listeners.manager import ListenerManager
from src.payment_service.processors import (
    PaymentProcessorProtocol,
    RecurringPaymentProtocol,
    RefundPaymentProtocol,
)
from src.payment_service.validators import ChainHandler

from .loggers import TransactionLogger
from .notifiers import NotifierProtocol
from .service_protocol import PaymentServiceProtocol


@dataclass
# paso 2, implementar la clase concreta del servicio de pagos
class PaymentService(PaymentServiceProtocol):
    payment_processor: PaymentProcessorProtocol
    notifier: NotifierProtocol
    validator: ChainHandler
    logger: TransactionLogger
    listener: ListenerManager
    recurring_processor: RecurringPaymentProtocol | None = None
    refund_processor: RefundPaymentProtocol | None = None

    @classmethod
    def create_with_payment_processor(cls, payment_data: PaymentData, **kwargs) -> Self:
        try:
            processor = PaymentProcessorFactory.create_payment_processor(payment_data)
            return cls(payment_processor=processor, **kwargs)
        except ValueError as e:
            print("Error creating payment processor:")
            raise e

    def set_notifier(self, notifier: NotifierProtocol) -> None:
        print("Changing notifier")
        """Establece el sistema de notificaciones"""
        self.notifier = notifier

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        """Procesa un pago único"""

        # require_contact = not isinstance(self.notifier, LogOnlyNotifier)

        try:
            request = Request(customer_data=customer_data, payment_data=payment_data)
            self.validator.handle(request=request)
        except Exception as e:
            print(f"Fallo en las validaciones: {e}")
            raise e

        try:
            payment_response = self.payment_processor.process_transaction(
                customer_data, payment_data
            )
            self.listener.notify(
                f"Pago exitoso: {payment_response}\n{payment_response.transaction_id}"
            )
            if payment_response.status == "succeeded":
                self.notifier.send_confirmation(customer_data)
            else:
                # Notificar internamente (listeners)
                self.listener.notify(
                    f"Error en el pago - Motivo: {payment_response.message}"
                )

                # Notificar al CLIENTE del fallo
                self.notifier.send_failure_notification(
                    customer_data, str(payment_response.message)
                )

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
            request = Request(customer_data=customer_data, payment_data=payment_data)
            self.validator.handle(request=request)
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
