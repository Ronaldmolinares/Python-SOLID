from dataclasses import dataclass

from src.payment_service.commons.customer import CustomerData


@dataclass
class CustomerValidator:
    def validate_data(self, customer_data: CustomerData, require_contact: bool = True):
        if not customer_data.name:
            raise ValueError("Invalid customer data: missing name")

        if not customer_data.contact_info:
            raise ValueError("Invalid customer data: missing contact info")

        if require_contact:
            if not (
                customer_data.contact_info.email or customer_data.contact_info.phone
            ):
                raise ValueError("Invalid customer data: missing email and phone")
