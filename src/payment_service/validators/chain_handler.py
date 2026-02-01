from abc import ABC, abstractmethod
from dataclasses import dataclass

# from typing import Self
from src.payment_service.commons.request import Request


@dataclass
class ChainHandler(ABC):
    _next_handler: "ChainHandler | None" = None

    def set_next(self, handler: "ChainHandler") -> "ChainHandler":
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: Request):
        pass
