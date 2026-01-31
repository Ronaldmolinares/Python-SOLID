from dataclasses import dataclass

from src.payment_service.commons import CustomerData

from .notifier import NotifierProtocol


@dataclass
class LogOnlyNotifier(NotifierProtocol):
    """Notificador que solo registra en logs (sin enviar email/SMS)."""

    def send_confirmation(self, customer_data: CustomerData) -> None:
        """Registra la confirmación en logs solamente."""
        print(f"📝 [LOG] Payment confirmation for {customer_data.name}")
        print("📝 [LOG] No contact info available, notification logged only")

    def send_failure_notification(
        self, customer_data: CustomerData, error_message: str
    ) -> None:
        """Registra pago fallido en logs"""
        print(f"📝 [LOG] ❌ Payment failure for {customer_data.name}")
        print(f"📝 [LOG] Error: {error_message}")
        print("📝 [LOG] No contact info available, notification logged only")
