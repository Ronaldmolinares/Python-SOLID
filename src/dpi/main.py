from src.dpi.customer_validator import CustomerValidator, PaymentDataValidator
from src.dpi.notifier import EmailNotifier, PhoneNotifier
from src.dpi.payment_data import ContactInfo, CustomerData, PaymentData
from src.dpi.payment_processor import (
    OfflinePaymentProcessor,
    StripePaymentProcessor,
)
from src.dpi.payment_service import PaymentService
from src.dpi.transaction_logger import TransactionLogger

if __name__ == "__main__":
    # Configurar dependencias
    stripe_processor = StripePaymentProcessor()
    offline_processor = OfflinePaymentProcessor()
    email_notifier = EmailNotifier()
    sms_notifier = PhoneNotifier(sms_gateway="CustomerGateway")
    customer_validator = CustomerValidator()
    payment_validator = PaymentDataValidator()
    logger = TransactionLogger()

    # Servicio completo con Stripe (soporta todo)
    payment_service = PaymentService(
        payment_processor=stripe_processor,
        notifier=email_notifier,
        customer_validator=customer_validator,
        payment_validator=payment_validator,
        logger=logger,
        recurring_processor=stripe_processor,
        refund_processor=stripe_processor,
    )

    # Servicio básico con pagos offline (solo pagos)
    second_service = PaymentService(
        payment_processor=offline_processor,
        notifier=sms_notifier,
        customer_validator=customer_validator,
        payment_validator=payment_validator,
        logger=logger,
    )

    # ===== DATOS DE PRUEBA =====
    customer_with_email = CustomerData(
        name="Alice Johnson",
        contact_info=ContactInfo(email="alice@example.com"),
    )

    customer_with_phone = CustomerData(
        name="Bob Smith",
        contact_info=ContactInfo(phone="1234567890"),
    )

    payment_data = PaymentData(amount=5000, source="tok_visa")
    recurring_payment_data = PaymentData(
        amount=2999, source="pm_card_visa"
    )  # Para suscripciones

    # ===== TEST 1: PAGO ÚNICO CON STRIPE =====
    print("\n" + "=" * 60)
    print("TEST 1: Pago único con Stripe")
    print("=" * 60)
    try:
        response = payment_service.process_transaction(
            customer_with_email, payment_data
        )
        print(f"Status: {response.status}")
        print(f"   Amount: ${response.amount / 100:.2f}")
        print(f"   Transaction ID: {response.transaction_id}")
        transaction_id = response.transaction_id  # Guardar para reembolso
    except Exception as e:
        print(f"Error: {e}")

    # ===== TEST 2: REEMBOLSO =====
    print("\n" + "=" * 60)
    print("TEST 2: Reembolso de pago anterior")
    print("=" * 60)
    try:
        if transaction_id:
            refund_response = payment_service.process_refund(transaction_id)
            print(f"Refund Status: {refund_response.status}")
            print(f"   Amount: ${refund_response.amount / 100:.2f}")
            print(f"   Refund ID: {refund_response.transaction_id}")
    except Exception as e:
        print(f"Error: {e}")

    # ===== TEST 3: PAGO RECURRENTE (SUSCRIPCIÓN) =====
    print("\n" + "=" * 60)
    print("TEST 3: Configurar pago recurrente (suscripción)")
    print("=" * 60)
    try:
        recurring_response = payment_service.setup_recurring(
            customer_with_email, recurring_payment_data
        )
        print(f"Subscription Status: {recurring_response.status}")
        print(f"   Amount: ${recurring_response.amount / 100:.2f}")
        print(f"   Subscription ID: {recurring_response.transaction_id}")
    except Exception as e:
        print(f"Error: {e}")

    # ===== TEST 4: PAGO OFFLINE =====
    print("\n" + "=" * 60)
    print("TEST 4: Pago offline (servicio básico)")
    print("=" * 60)
    try:
        offline_response = second_service.process_transaction(
            customer_with_phone, payment_data
        )
        print(f"Status: {offline_response.status}")
        print(f"   Amount: ${offline_response.amount / 100:.2f}")
        print(f"   Transaction ID: {offline_response.transaction_id}")
    except Exception as e:
        print(f"Error: {e}")

    # ===== TEST 5: INTENTAR REEMBOLSO CON PROCESADOR OFFLINE (DEBE FALLAR) =====
    print("\n" + "=" * 60)
    print("TEST 5: Intentar reembolso con procesador offline (debe fallar)")
    print("=" * 60)
    try:
        second_service.process_refund("fake_transaction_id")
    except NotImplementedError as e:
        print(f"Error esperado: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    # ===== TEST 6: INTENTAR RECURRENCIA CON PROCESADOR OFFLINE (DEBE FALLAR) =====
    print("\n" + "=" * 60)
    print("TEST 6: Intentar recurrencia con procesador offline (debe fallar)")
    print("=" * 60)
    try:
        second_service.setup_recurring(customer_with_phone, payment_data)
    except NotImplementedError as e:
        print(f"Error esperado: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    print("\n" + "=" * 60)
    print("PRUEBAS COMPLETADAS")
    print("=" * 60)
