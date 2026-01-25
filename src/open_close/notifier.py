from abc import ABC, abstractmethod
from dataclasses import dataclass
from email.mime.text import MIMEText

from .payment_data import CustomerData

dataclass


class Notifier(ABC):
    @abstractmethod
    def send_confirmation(self, customer_data: CustomerData): ...


class EmailNotifier(Notifier):
    def send_confirmation(self, customer_data: CustomerData):
        msg = MIMEText("Thank you for your payment.")
        msg["Subject"] = "Payment Confirmation"
        msg["From"] = "no-reply@example.com"
        msg["To"] = customer_data.contact_info.email or ""

        print("Email sent to", customer_data.contact_info.email)


class PhoneNotifier(Notifier):
    def send_confirmation(self, customer_data: CustomerData):
        phone_number = customer_data.contact_info.phone
        sms_gateway = "the custom SMS Gateway"
        print(
            f"send the sms using {sms_gateway}: SMS sent to {phone_number}: Thank you for your payment."
        )
