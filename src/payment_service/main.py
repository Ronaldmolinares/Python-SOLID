from src.payment_service.commons import (
    ContactInfo,
    CustomerData,
    PaymentData,
    PaymentType,
)
from src.payment_service.notifiers.default_notifier import LogOnlyNotifier
from src.payment_service.notifiers.notifier import NotifierProtocol
from src.payment_service.notifiers.sms import PhoneNotifier
from src.payment_service.validators.customer import CustomerValidator
from src.payment_service.validators.payment import PaymentDataValidator

from .loggers import TransactionLogger
from .logging_service import PaymentServiceLogging
from .notifiers import EmailNotifier
from .service import PaymentService


# ===== STRATEGY: Selección de Notificador =====
def get_email_notifier() -> EmailNotifier:
    """Retorna notificador por email."""
    return EmailNotifier()


def get_sms_notifier() -> PhoneNotifier:
    """Retorna notificador por SMS."""
    return PhoneNotifier(sms_gateway="SMS Gateway")


def get_default_notifier() -> NotifierProtocol:
    """Retorna notificador por defecto (cuando no hay email ni teléfono)."""
    print("⚠️ Warning: No contact info, using default notifier (log only)")
    return LogOnlyNotifier()


def get_notifier_strategy(customer_data: CustomerData) -> NotifierProtocol:
    """
    Strategy Pattern: Selecciona el notificador apropiado según los datos del cliente.

    Prioridad:
    1. SMS si tiene teléfono
    2. Email si tiene email
    3. Notificador por defecto si no tiene nada
    """
    if customer_data.contact_info.phone:
        print("📱 Using SMS Notifier")
        return get_sms_notifier()

    if customer_data.contact_info.email:
        print("📧 Using Email Notifier")
        return get_email_notifier()

    print("📝 Using Default Notifier")
    return get_default_notifier()


# ===== FACTORY METHOD PATTERN: Creación de Servicios =====
def create_payment_service():
    pass


# payment_data = PaymentData(amount=100, currency="MXN", source="tok_visa")

# service = PaymentService.create_with_payment_processor(
#     payment_data=payment_data,
#     notifier=LogOnlyNotifier(),
#     customer_validator=CustomerValidator(),
#     payment_validator=PaymentDataValidator(),
#     logger=TransactionLogger(),
# )

# logging_service = PaymentServiceLogging(wrapped_service=service)

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("STRATEGY PATTERN + FACTORY METHOD PATTERN")
    print("=" * 70)

    # ===== TEST 1: Pago ONLINE con MXN (Stripe) + Email =====
    print("\n" + "=" * 70)
    print("TEST 1: Pago ONLINE con MXN (Stripe) - Cliente con Email")
    print("=" * 70)

    customer_with_email = CustomerData(
        name="Alice Johnson", contact_info=ContactInfo(email="alice@example.com")
    )

    payment_online_mxn = PaymentData(
        amount=5000,  # $50.00 MXN
        currency="MXN",
        source="tok_visa",
    )

    # STRATEGY: Selecciona notificador
    notifier1 = get_notifier_strategy(customer_with_email)

    # FACTORY: Crea servicio con procesador apropiado
    service1 = PaymentService.create_with_payment_processor(
        payment_data=payment_online_mxn,
        notifier=notifier1,
        customer_validator=CustomerValidator(),
        payment_validator=PaymentDataValidator(),
        logger=TransactionLogger(),
    )

    decorator_service = PaymentServiceLogging(wrapped_service=service1)

    try:
        response = decorator_service.process_transaction(
            customer_with_email, payment_online_mxn
        )
        print(f"✅ Payment Status: {response.status}")
        print(f"   Amount: ${response.amount / 100:.2f} {payment_online_mxn.currency}")
        print(f"   Transaction ID: {response.transaction_id}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # ===== TEST 2: Pago ONLINE con USD (Local) + SMS =====
    print("\n" + "=" * 70)
    print("TEST 2: Pago ONLINE con USD (Local) - Cliente con Teléfono")
    print("=" * 70)

    customer_with_phone = CustomerData(
        name="Bob Smith", contact_info=ContactInfo(phone="1234567890")
    )

    payment_online_usd = PaymentData(
        amount=3000,  # $30.00 USD
        currency="USD",
        source="tok_mastercard",
    )

    # STRATEGY: Selecciona SMS notifier
    notifier2 = get_notifier_strategy(customer_with_phone)

    # FACTORY: Crea servicio (usará LocalPaymentProcessor por USD)
    service2 = PaymentService.create_with_payment_processor(
        payment_data=payment_online_usd,
        notifier=notifier2,
        customer_validator=CustomerValidator(),
        payment_validator=PaymentDataValidator(),
        logger=TransactionLogger(),
    )

    try:
        decorator_service = PaymentServiceLogging(wrapped_service=service2)
        response = decorator_service.process_transaction(
            customer_with_phone, payment_online_usd
        )
        print(f"✅ Payment Status: {response.status}")
        print(f"   Amount: ${response.amount / 100:.2f} {payment_online_usd.currency}")
        print(f"   Transaction ID: {response.transaction_id}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # ===== TEST 3: Pago OFFLINE + Sin Contacto =====
    print("\n" + "=" * 70)
    print("TEST 3: Pago OFFLINE - Cliente sin información de contacto")
    print("=" * 70)

    customer_no_contact = CustomerData(
        name="Charlie Anonymous", contact_info=ContactInfo()
    )

    payment_offline = PaymentData(
        amount=10000,  # $100.00
        currency="MXN",
        source="OFFLINE",
        type=PaymentType.OFFLINE,
    )

    # STRATEGY: Selecciona LogOnlyNotifier
    notifier3 = get_notifier_strategy(customer_no_contact)

    # FACTORY: Crea servicio (usará OfflinePaymentProcessor)
    service3 = PaymentService.create_with_payment_processor(
        payment_data=payment_offline,
        notifier=notifier3,
        customer_validator=CustomerValidator(),
        payment_validator=PaymentDataValidator(),
        logger=TransactionLogger(),
    )

    try:
        response = service3.process_transaction(customer_no_contact, payment_offline)
        print(f"✅ Payment Status: {response.status}")
        print(f"   Amount: ${response.amount / 100:.2f} {payment_offline.currency}")
        print(f"   Transaction ID: {response.transaction_id}")
    except Exception as e:
        print(f"❌ Error: {e}")
