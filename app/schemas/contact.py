import re

from pydantic import BaseModel, model_validator

_EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class ContactRequest(BaseModel):
    name: str = ""
    email: str = ""
    message: str = ""

    @model_validator(mode="after")
    def _validate_fields(self) -> "ContactRequest":
        if not self.name or not self.email or not self.message:
            raise ValueError("All contact fields are required.")
        if not _EMAIL_PATTERN.match(self.email):
            raise ValueError("Please enter a valid email address.")
        return self


class ContactResponse(BaseModel):
    success: str
