from pydantic import BaseModel, Field


class From(BaseModel):
    address: str
    name: str


class To(BaseModel):
    address: str
    name: str


class Message(BaseModel):
    a_id: str = Field(alias="@id")
    a_type: str = Field(alias="@type")
    id: str
    account_id: str = Field(alias="accountId")
    msg_id: str = Field("msgid")
    _from: From
    to: list[To]
    subject: str
    intro: str | None = None
    seen: bool
    id_deleted: bool = Field(alias="isDeleted")
    has_attachments: bool = Field("hasAttachments")
    size: int
    download_url: str = Field("downloadUrl")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")


class Messages(BaseModel):
    a_context: str = Field(None, alias="@context")
    a_id: str = Field(alias="@id")
    a_type: str = Field(alias="@type")
    messages: list[Message] = Field(alias="hydra:member")
    total_items: int = Field(alias="hydra:totalItems")


class ReadMessage(Message):
    cc: list
    bcc: list
    flagged: bool
    verifications: list
    retention: bool
    text: str
    html: list[str]

