from dataclasses import dataclass

from src.payment_service.commons.customer import CustomerData

from .notifier import NotifierProtocol


@dataclass
class PhoneNotifier(NotifierProtocol):
    sms_gateway: str

    def send_confirmation(self, customer_data: CustomerData):
        phone_number = customer_data.contact_info.phone
        if not phone_number:
            print("No phone number provided")
            return
        print(
            f"SMS send to {phone_number} via {self.sms_gateway}: Thank you for your payment."
        )
