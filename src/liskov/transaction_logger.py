from dataclasses import dataclass

from .payment_data import CustomerData, PaymentData


@dataclass
class TransactionLogger:
    def log(self, customer_data: CustomerData, payment_data: PaymentData, charge):
        with open("transactions.log", "a") as log_file:
            log_file.write(f"{customer_data.name} paid {payment_data.amount}\n")
            log_file.write(f"Payment status: {charge['status']}\n")
