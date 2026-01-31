# from src.payment_service.commons import (
#     CustomerData,
#     customer,
# )
# from src.payment_service.commons.payment_data import PaymentData
# from src.payment_service.notifiers.default_notifier import LogOnlyNotifier
# from src.payment_service.notifiers.notifier import NotifierProtocol
# from src.payment_service.notifiers.sms import PhoneNotifier

# from .builder import PaymentServiceBuilder
# from .notifiers import EmailNotifier


# # ===== STRATEGY: Selección de Notificador =====
# def get_email_notifier() -> EmailNotifier:
#     """Retorna notificador por email."""
#     return EmailNotifier()


# def get_sms_notifier() -> PhoneNotifier:
#     """Retorna notificador por SMS."""
#     return PhoneNotifier(sms_gateway="SMS Gateway")


# def get_default_notifier() -> NotifierProtocol:
#     """Retorna notificador por defecto (cuando no hay email ni teléfono)."""
#     print("⚠️ Warning: No contact info, using default notifier (log only)")
#     return LogOnlyNotifier()


# def get_notifier_strategy(customer_data: CustomerData) -> NotifierProtocol:
#     """
#     Strategy Pattern: Selecciona el notificador apropiado según los datos del cliente.

#     Prioridad:
#     1. SMS si tiene teléfono
#     2. Email si tiene email
#     3. Notificador por defecto si no tiene nada
#     """
#     if customer_data.contact_info.phone:
#         print("📱 Using SMS Notifier")
#         return get_sms_notifier()

#     if customer_data.contact_info.email:
#         print("📧 Using Email Notifier")
#         return get_email_notifier()

#     print("📝 Using Default Notifier")
#     return get_default_notifier()


# if __name__ == "__main__":
#     customer_data = CustomerData(
#         name="Manuela Torres",
#         contact_info=customer.ContactInfo(email="manuela.torres@yahoo.com"),
#     )
#     payment_data = PaymentData(amount=120, source="tok_mastercard")
#     builder = PaymentServiceBuilder()

#     service = (
#         builder.set_logger()
#         .set_payment_validator()
#         .set_customer_validator()
#         .set_payment_processor(payment_data)
#         .set_notifier(customer_data)
#         .build()
#     )
from src.payment_service.commons import CustomerData
from src.payment_service.commons.contact import ContactInfo
from src.payment_service.commons.payment_data import PaymentData, PaymentType

from .builder import PaymentServiceBuilder

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("BUILDER PATTERN + STRATEGY PATTERN + FACTORY METHOD")
    print("=" * 70)

    # ===== TEST 1: Cliente con Email =====
    print("\n--- TEST 1: Cliente con Email ---")

    customer_data = CustomerData(
        name="Manuela Torres",
        contact_info=ContactInfo(email="manuela.torres@yahoo.com"),
    )

    payment_data = PaymentData(
        amount=12000,  # $120.00
        source="tok_mastercard",
        currency="MXN",
        type=PaymentType.ONLINE,
    )

    # ✅ CORRECTO: Pasa customer_data directamente
    # El builder aplicará el Strategy Pattern internamente
    service = (
        PaymentServiceBuilder()
        .set_payment_processor(payment_data)
        .set_notifier(customer_data)  # ✅ Pasa CustomerData, no NotifierProtocol
        .set_recurring_processor()
        .set_refund_processor()
        .set_logger()
        .set_customer_validator()
        .set_payment_validator()
        .build()
    )

    try:
        response = service.process_transaction(customer_data, payment_data)
        print(f"✅ Payment Status: {response.status}")
        print(f"   Amount: ${response.amount / 100:.2f} {payment_data.currency}")
        print(f"   Transaction ID: {response.transaction_id}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # ===== TEST 2: Cliente con Teléfono =====
    print("\n--- TEST 2: Cliente con Teléfono ---")

    customer_with_phone = CustomerData(
        name="Carlos Mendez",
        contact_info=ContactInfo(phone="5551234567"),
    )

    payment_data_usd = PaymentData(
        amount=5000, source="tok_visa", currency="USD", type=PaymentType.ONLINE
    )

    service2 = (
        PaymentServiceBuilder()
        .set_payment_processor(payment_data_usd)
        .set_notifier(customer_with_phone)  # ✅ Strategy seleccionará SMS
        .set_recurring_processor()
        .set_refund_processor()
        .set_logger()
        .set_customer_validator()
        .set_payment_validator()
        .build()
    )

    try:
        response = service2.process_transaction(customer_with_phone, payment_data_usd)
        print(f"✅ Payment Status: {response.status}")
        print(f"   Amount: ${response.amount / 100:.2f} {payment_data_usd.currency}")
        print(f"   Transaction ID: {response.transaction_id}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # ===== TEST 3: Cliente sin Contacto =====
    print("\n--- TEST 3: Cliente sin Contacto ---")

    customer_no_contact = CustomerData(
        name="Usuario Anónimo",
        contact_info=ContactInfo(),  # Sin email ni teléfono
    )

    payment_offline = PaymentData(
        amount=8000, source="", currency="MXN", type=PaymentType.OFFLINE
    )

    service3 = (
        PaymentServiceBuilder()
        .set_payment_processor(payment_offline)
        .set_notifier(customer_no_contact)  # ✅ Strategy seleccionará LogOnlyNotifier
        .set_recurring_processor()
        .set_refund_processor()
        .set_logger()
        .set_customer_validator()
        .set_payment_validator()
        .build()
    )

    try:
        response = service3.process_transaction(customer_no_contact, payment_offline)
        print(f"✅ Payment Status: {response.status}")
        print(f"   Amount: ${response.amount / 100:.2f} {payment_offline.currency}")
        print(f"   Transaction ID: {response.transaction_id}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 70)
    print("PRUEBAS COMPLETADAS")
    print("=" * 70)
