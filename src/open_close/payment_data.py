from pydantic import BaseModel


class ContactInfo(BaseModel):
    email: str | None = None
    phone: str | None = None


class CustomerData(BaseModel):
    name: str
    contact_info: ContactInfo


class PaymentData(BaseModel):
    amount: int
    source: str
