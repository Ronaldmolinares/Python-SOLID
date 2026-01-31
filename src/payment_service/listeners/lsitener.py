from typing_extensions import Protocol


class Listener[T](Protocol):
    def notify(self, event: T): ...
