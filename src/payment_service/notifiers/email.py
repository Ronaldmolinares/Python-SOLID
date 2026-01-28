from email.mime.text import MIMEText

from src.payment_service.commons.customer import CustomerData
from src.payment_service.notifiers.notifier import NotifierProtocol


class EmailNotifier(NotifierProtocol):
    def send_confirmation(self, customer_data: CustomerData):
        if not customer_data.contact_info.email:
            raise ValueError("Email address is requiered to send an email")

        msg = MIMEText("Thank you for your payment.")
        msg["Subject"] = "Payment Confirmation"
        msg["From"] = "no-reply@example.com"
        msg["To"] = customer_data.contact_info.email

        print("Email sent to", customer_data.contact_info.email)
