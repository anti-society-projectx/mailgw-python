from pydantic import BaseModel, Field, ConfigDict


class Account(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    a_context: str = Field(alias="@context")
    a_id: str = Field(alias="@id")
    a_type: str = Field(alias="@type")
    id: str
    address: str
    quota: int
    used: int
    is_disabled: bool = Field(alias="isDisabled")
    is_delete: bool = Field(alias="isDeleted")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    retention_at: str = Field(alias="retentionAt")
