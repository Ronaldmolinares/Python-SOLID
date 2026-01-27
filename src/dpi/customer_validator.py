from dataclasses import dataclass

from .payment_data import CustomerData, PaymentData


@dataclass
class CustomerValidator:
    def validate_data(self, customer_data: CustomerData):
        if not customer_data.name:
            raise ValueError("Invalid customer data: missing name")

        if not customer_data.contact_info:
            raise ValueError("Invalid customer data: missing contact info")

        if not (customer_data.contact_info.email or customer_data.contact_info.phone):
            raise ValueError("Invalid customer data: missing email and phone")


@dataclass
class PaymentDataValidator:
    def validate(self, payment_data: PaymentData):
        if not payment_data.source:
            print("Invalid payment data: missing source")
            raise ValueError("Invalid payment data: missing source")
        if payment_data.amount <= 0:
            print("Invalid payment data: amount must be positive")
            raise ValueError("Invalid payment data: amount must be positive")
