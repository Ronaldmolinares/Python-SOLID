from .notifier import PhoneNotifier
from .payment_data import ContactInfo, CustomerData, PaymentData
from .payment_service import PaymentService

if __name__ == "__main__":
    sms_notifier = PhoneNotifier(sms_gateway="This is a sms mock gateway")
    payment_service = PaymentService()
    payment_service_sms_notifier = PaymentService(notifier=sms_notifier)

    customer_data_with_email = CustomerData(
        name="John Doe", contact_info=ContactInfo(email="john@example.com")
    )
    customer_data_with_phone = CustomerData(
        name="John Doe", contact_info=ContactInfo(phone="1234567890")
    )

    payment_data = PaymentData(amount=100, source="tok_visa")

    payment_service_sms_notifier.process_transaction(
        customer_data_with_email, payment_data
    )
    payment_service.process_transaction(customer_data_with_phone, payment_data)

    try:
        error_payment_data = PaymentData(amount=100, source="tok_radarBlock")
        payment_service.process_transaction(
            customer_data_with_email, error_payment_data
        )
    except Exception as e:
        print(f"Payment failed and PaymentProcessor raised an exception: {e}")
