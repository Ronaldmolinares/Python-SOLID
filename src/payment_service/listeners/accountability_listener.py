from src.payment_service.listeners.lsitener import Listener


class AccountabilityListener[T](Listener):
    def notify(self, event: T) -> None:
        print(f"[Accountability] Event received: {event}")
