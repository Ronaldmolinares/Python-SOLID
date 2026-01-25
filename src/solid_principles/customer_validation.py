from dataclasses import dataclass


@dataclass
class CustomerValidator:
    def validate_data(self, customer_data) -> None:
        """Valida los datos del cliente. Lanza ValueError si son inválidos."""
        if not customer_data.get("name"):
            raise ValueError("Invalid customer data: missing name")

        if not customer_data.get("contact_info"):
            raise ValueError("Invalid customer data: missing contact info")
