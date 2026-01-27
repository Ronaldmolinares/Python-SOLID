from dataclasses import dataclass
from email.mime.text import MIMEText
from typing import Protocol

from .payment_data import CustomerData


class Notifier(Protocol):
    """
    Protocol for sending notifications.

    This protocol defines the interface for notifiers. Implementations
    should provide a method `send_confirmation` that sends a confirmation
    to the customer.
    """

    def send_confirmation(self, customer_data: CustomerData): ...


class EmailNotifier(Notifier):
    def send_confirmation(self, customer_data: CustomerData):
        if not customer_data.contact_info.email:
            raise ValueError("Email address is requiered to send an email")

        msg = MIMEText("Thank you for your payment.")
        msg["Subject"] = "Payment Confirmation"
        msg["From"] = "no-reply@example.com"
        msg["To"] = customer_data.contact_info.email

        print("Email sent to", customer_data.contact_info.email)


@dataclass
class PhoneNotifier(Notifier):
    sms_gateway: str

    def send_confirmation(self, customer_data: CustomerData):
        phone_number = customer_data.contact_info.phone
        if not phone_number:
            print("No phone number provided")
            return
        print(
            f"SMS send to {phone_number} via {self.sms_gateway}: Thank you for your payment."
        )
