from src.payment_service.commons import PaymentData, PaymentType
from src.payment_service.processors import (
    LocalPaymentProcessor,
    OfflinePaymentProcessor,
    PaymentProcessorProtocol,
    StripePaymentProcessor,
)


class PaymentProcessorFactory:
    @staticmethod
    def create_payment_processor(
        payment_data: PaymentData,
    ) -> PaymentProcessorProtocol:
        """Crea un procesador de pagos basado en el tipo de pago"""
        match payment_data.type:
            case PaymentType.OFFLINE:
                return OfflinePaymentProcessor()
            case PaymentType.ONLINE:
                match payment_data.currency:
                    case "MXN":
                        return StripePaymentProcessor()
                    case _:
                        return LocalPaymentProcessor()

            case _:
                raise ValueError("Tipo de pago no soportado")
