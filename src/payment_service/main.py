from src.payment_service.commons import (
    ContactInfo,
    CustomerData,
    PaymentData,
)
from src.payment_service.notifiers.default_notifier import LogOnlyNotifier
from src.payment_service.notifiers.notifier import NotifierProtocol
from src.payment_service.notifiers.sms import PhoneNotifier
from src.payment_service.processors.payment import PaymentProcessorProtocol
from src.payment_service.validators.customer import CustomerValidator
from src.payment_service.validators.payment import PaymentDataValidator

from .loggers import TransactionLogger
from .notifiers import EmailNotifier
from .processors import LocalPaymentProcessor, StripePaymentProcessor
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


# ===== STRATEGY: Selección de Procesador de Pagos =====
def get_stripe_processor() -> StripePaymentProcessor:
    """Retorna procesador de Stripe (para producción)."""
    return StripePaymentProcessor()


def get_local_processor() -> LocalPaymentProcessor:
    """Retorna procesador local (para pruebas)."""
    return LocalPaymentProcessor()


def get_payment_processor_strategy(
    payment_type: str, is_test_mode: bool = False
) -> PaymentProcessorProtocol:
    """
    Strategy Pattern: Selecciona el procesador de pagos apropiado.

    Args:
        payment_type: Tipo de pago ("online", "local", "test")
        is_test_mode: Si está en modo de prueba

    Returns:
        PaymentProcessorProtocol: Procesador seleccionado
    """
    if is_test_mode or payment_type == "local":
        print("🔧 Using Local Payment Processor (Test Mode)")
        return get_local_processor()

    if payment_type == "online":
        print("💳 Using Stripe Payment Processor (Production)")
        return get_stripe_processor()

    # Por defecto usa local para seguridad
    print("⚠️ Unknown payment type, defaulting to Local Processor")
    return get_local_processor()


if __name__ == "__main__":
    # ===== CONFIGURACIÓN =====
    customer_validator = CustomerValidator()
    payment_data_validator = PaymentDataValidator()
    logger = TransactionLogger()

    # ===== TEST 1: Cliente con EMAIL + Stripe =====
    print("\n" + "=" * 60)
    print("TEST 1: Cliente con Email + Stripe Processor")
    print("=" * 60)

    customer_with_email = CustomerData(
        name="John Doe", contact_info=ContactInfo(email="john@example.com")
    )

    payment_data = PaymentData(amount=5000, source="tok_visa")

    # Strategy: Seleccionar procesador y notificador
    processor = get_payment_processor_strategy("online", is_test_mode=False)
    notifier = get_notifier_strategy(customer_with_email)

    service = PaymentService(
        payment_processor=processor,
        notifier=notifier,
        logger=logger,
        customer_validator=customer_validator,
        payment_validator=payment_data_validator,
    )

    try:
        response = service.process_transaction(customer_with_email, payment_data)
        print(f"✅ Payment Status: {response.status}")
        print(f"   Amount: ${response.amount / 100:.2f}")
        print(f"   Transaction ID: {response.transaction_id}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # ===== TEST 2: Cliente con TELÉFONO + Local Processor =====
    print("\n" + "=" * 60)
    print("TEST 2: Cliente con Teléfono + Local Processor")
    print("=" * 60)

    customer_with_phone = CustomerData(
        name="Jane Smith", contact_info=ContactInfo(phone="1234567890")
    )

    # Strategy: Cambiar a procesador local y notificador SMS
    processor = get_payment_processor_strategy("local", is_test_mode=True)
    notifier = get_notifier_strategy(customer_with_phone)

    service = PaymentService(
        payment_processor=processor,
        notifier=notifier,
        logger=logger,
        customer_validator=customer_validator,
        payment_validator=payment_data_validator,
    )

    try:
        response = service.process_transaction(customer_with_phone, payment_data)
        print(f"✅ Payment Status: {response.status}")
        print(f"   Amount: ${response.amount / 100:.2f}")
        print(f"   Transaction ID: {response.transaction_id}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # ===== TEST 3: Cliente SIN CONTACTO =====
    print("\n" + "=" * 60)
    print("TEST 3: Cliente sin información de contacto")
    print("=" * 60)

    customer_no_contact = CustomerData(
        name="Anonymous User",
        contact_info=ContactInfo(),  # Sin email ni teléfono
    )

    # Strategy: Usar notificador por defecto
    processor = get_payment_processor_strategy("local", is_test_mode=True)
    notifier = get_notifier_strategy(customer_no_contact)

    service = PaymentService(
        payment_processor=processor,
        notifier=notifier,
        logger=logger,
        customer_validator=customer_validator,
        payment_validator=payment_data_validator,
    )

    try:
        response = service.process_transaction(customer_no_contact, payment_data)
        print(f"✅ Payment Status: {response.status}")
        print(f"   Amount: ${response.amount / 100:.2f}")
        print(f"   Transaction ID: {response.transaction_id}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # ===== TEST 4: Cambiar estrategia dinámicamente =====
    print("\n" + "=" * 60)
    print("TEST 4: Cambiar estrategia en tiempo de ejecución")
    print("=" * 60)

    # Cambiar el notificador dinámicamente
    new_notifier = get_email_notifier()
    service.set_notifier(new_notifier)
    print("📧 Notifier changed to Email")

    try:
        response = service.process_transaction(customer_with_email, payment_data)
        print(f"✅ Payment Status: {response.status}")
    except Exception as e:
        print(f"❌ Error: {e}")
