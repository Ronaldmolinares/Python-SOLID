from pydantic import BaseModel


class PaymentResponse(BaseModel):
    """Se implementa para estandarizar la respuesta de diferentes pasarelas"""

    status: str
    amount: int
    transaction_id: str | None = None
    message: str | None = None
