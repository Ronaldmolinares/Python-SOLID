from typing import Protocol

from src.payment_service.commons.customer import CustomerData
from src.payment_service.commons.payment_data import PaymentData
from src.payment_service.commons.payment_response import PaymentResponse
from src.payment_service.listeners.manager import ListenerManager
from src.payment_service.loggers.transaction_logger import TransactionLogger
from src.payment_service.notifiers.notifier import NotifierProtocol
from src.payment_service.processors.payment import PaymentProcessorProtocol
from src.payment_service.processors.recurring import RecurringPaymentProtocol
from src.payment_service.processors.refunds import RefundPaymentProtocol
from src.payment_service.validators import ChainHandler


# paso 1, definir una interfaz para el servicio de pagos
class PaymentServiceProtocol(Protocol):
    payment_processor: PaymentProcessorProtocol
    notifier: NotifierProtocol
    validator: ChainHandler
    logger: TransactionLogger
    listener: ListenerManager
    recurring_processor: RecurringPaymentProtocol | None = None
    refund_processor: RefundPaymentProtocol | None = None

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...

    def process_refund(self, transaction_id: str) -> PaymentResponse: ...

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse: ...
