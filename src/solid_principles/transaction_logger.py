from dataclasses import dataclass


@dataclass
class TransactionLogger:
    def log(self, customer_data, payment_data, charge):
        # Responsabilidad de Registro Logs
        with open("transactions.log", "a") as log_file:
            log_file.write(f"{customer_data['name']} paid {payment_data['amount']}\n")
            log_file.write(f"Payment status: {charge['status']}\n")
