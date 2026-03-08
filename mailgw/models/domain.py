from pydantic import BaseModel, Field

class HydraMember(BaseModel):
    a_id: str = Field(alias="@id")
    a_type: str = Field(alias="@type")
    domain: str
    is_active: bool = Field(alias="isActive")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")

class Domain(BaseModel):
    a_context: str = Field(None, alias="@context")
    a_id: str = Field(alias="@id")
    a_type: str = Field(alias="@type")
    hydra_member: list[HydraMember] | None = Field(None, alias="hydra:member")
    hydra_total_items: int | None = Field(None, alias="hydra:totalItems")
