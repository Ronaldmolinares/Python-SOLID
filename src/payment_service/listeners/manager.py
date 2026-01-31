from dataclasses import dataclass, field

from src.payment_service.listeners.lsitener import Listener


@dataclass
class ListenerManager[T]:
    listeners: list[Listener] = field(default_factory=list)

    def suscribe(self, listener: Listener) -> None:
        self.listeners.append(listener)

    def unsuscribe(self, listener: Listener) -> None:
        self.listeners.remove(listener)

    def notify(self, event: T) -> None:
        for listener in self.listeners:
            listener.notify(event)
