from pydantic import BaseModel

from src.payment_service.commons.contact import ContactInfo


class CustomerData(BaseModel):
    name: str
    contact_info: ContactInfo
    customer_id: str | None = None
