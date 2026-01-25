from .payment_data import ContactInfo, CustomerData, PaymentData
from .payment_service import PaymentService

if __name__ == "__main__":
    payment_processor = PaymentService()

    customer_data_with_email = CustomerData(
        name="Diego Tenjo", contact_info=ContactInfo(email="tenjoD@gmail.com")
    )
    customer_data_with_phone = CustomerData(
        name="Sergio Ruiz", contact_info=ContactInfo(phone="3215689741")
    )

    # Camino Feliz
    payment_data = PaymentData(amount=99, source="tok_visa_debit")

    payment_processor.process_transaction(customer_data_with_email, payment_data)
    payment_processor.process_transaction(customer_data_with_phone, payment_data)

    # Camino no tan feliz por usar tok_radarBlock
    # payment_data = {"amount": 150, "source": "tok_radarBlock", "cvv": 456}
    # payment_processor.process_transaction(customer_data_with_email, payment_data)
