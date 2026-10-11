from pydantic import BaseModel, ConfigDict, Field, model_validator


class ChatRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_message: str = Field(default="", alias="userMessage")

    @model_validator(mode="after")
    def _require_message(self) -> "ChatRequest":
        self.user_message = self.user_message.strip()
        if not self.user_message:
            raise ValueError("Message content cannot be blank.")
        return self


class ChatResponse(BaseModel):
    reply: str
