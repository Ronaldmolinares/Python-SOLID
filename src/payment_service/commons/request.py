from pydantic import BaseModel

from src.payment_service.commons import CustomerData, PaymentData


class Request(BaseModel):
    customer_data: CustomerData
    payment_data: PaymentData
