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

    def send_confirmation(self, customer_data: CustomerData):
        """Send a confirmation notification to the customer.

        :param customer_data: Data about the customer to notify.
        :type customer_data: CustomerData
        """
        ...


class EmailNotifier(Notifier):
    def send_confirmation(self, customer_data: CustomerData):
        msg = MIMEText("Thank you for your payment.")
        msg["Subject"] = "Payment Confirmation"
        msg["From"] = "no-reply@example.com"
        msg["To"] = customer_data.contact_info.email or ""

        print("Email sent to", customer_data.contact_info.email)


@dataclass
class PhoneNotifier(Notifier):
    sms_gateway: str

    def send_confirmation(self, customer_data: CustomerData):
        phone_number = customer_data.contact_info.phone
        print(
            f"send the sms using {self.sms_gateway}: SMS sent to {phone_number}: Thank you for your payment."
        )
