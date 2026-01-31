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

    def send_failure_notification(
        self, customer_data: CustomerData, error_message: str
    ):
        """Envía SMS de pago fallido"""
        phone_number = customer_data.contact_info.phone
        if not phone_number:
            print("Cannot send failure notification: no phone number")
            return

        print(f"📱 Failure SMS sent to {phone_number}")
        print(f"   ❌ Payment failed for {customer_data.name}")
        print(f"   🔴 Reason: {error_message}")
