from pydantic import BaseModel


class ContactInfo(BaseModel):
    email: str | None = None
    phone: str | None = None


class CustomerData(BaseModel):
    name: str
    contact_info: ContactInfo
    customer_id: str | None = None


class PaymentData(BaseModel):
    amount: int
    source: str


class PaymentResponse(BaseModel):
    """Se implementa para estandarizar la respuesta de diferentes pasarelas"""

    status: str
    amount: int
    transaction_id: str | None = None
    message: str | None = None
