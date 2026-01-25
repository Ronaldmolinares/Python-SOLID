from dataclasses import dataclass
from email.mime.text import MIMEText

dataclass


class Notifier:
    def send_confirmation(self, customer_data):
        # Responsabilidad de Enviar Notificación
        if "email" in customer_data["contact_info"]:
            msg = MIMEText("Thank you for your payment.")
            msg["Subject"] = "Payment Confirmation"
            msg["From"] = "no-reply@example.com"
            msg["To"] = customer_data["contact_info"]["email"]

            print("Email sent to", customer_data["contact_info"]["email"])

        elif "phone" in customer_data["contact_info"]:
            phone_number = customer_data["contact_info"]["phone"]
            sms_gateway = "the custom SMS Gateway"
            print(
                f"send the sms using {sms_gateway}: SMS sent to {phone_number}: Thank you for your payment."
            )
