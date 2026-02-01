from src.payment_service.commons.payment_data import PaymentType
from src.payment_service.commons.request import Request
from src.payment_service.validators.chain_handler import ChainHandler
from src.payment_service.validators.customer import CustomerValidator


class CustomerHandler(ChainHandler):
    def handle(self, request: Request):
        validator = CustomerValidator()
        try:
            # Para pagos OFFLINE, no se requiere información de contacto
            require_contact = request.payment_data.type != PaymentType.OFFLINE
            validator.validate_data(
                request.customer_data, require_contact=require_contact
            )
            if self._next_handler:
                self._next_handler.handle(request)
        except Exception as e:
            print(f"CustomerHandler: Validation error - {e}")
            raise e
