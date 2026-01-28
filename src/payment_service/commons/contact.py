from pydantic import BaseModel


class ContactInfo(BaseModel):
    email: str | None = None
    phone: str | None = None
