from src.payment_service.commons.request import Request
from src.payment_service.validators import PaymentDataValidator
from src.payment_service.validators.chain_handler import ChainHandler


class PaymentHandler(ChainHandler):
    def handle(self, request: Request):
        validator = PaymentDataValidator()
        try:
            validator.validate(request.payment_data)
            if self._next_handler:
                self._next_handler.handle(request)
        except Exception as e:
            print(f"PaymentHandler: Validation error - {e}")
            raise e
