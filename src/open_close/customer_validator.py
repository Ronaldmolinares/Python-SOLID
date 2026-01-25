from dataclasses import dataclass

from .payment_data import CustomerData


@dataclass
class CustomerValidator:
    def validate_data(self, customer_data: CustomerData):
        if not customer_data.name:
            raise ValueError("Invalid customer data: missing name")

        if not customer_data.contact_info:
            raise ValueError("Invalid customer data: missing contact info")

        if not (customer_data.contact_info.email or customer_data.contact_info.phone):
            raise ValueError("Invalid customer data: missing email and phone")
