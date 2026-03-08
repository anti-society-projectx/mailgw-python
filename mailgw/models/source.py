from pydantic import BaseModel, Field


class Source(BaseModel):
    a_context: str = Field(None, alias="@context")
    a_id: str = Field(alias="@id")
    a_type: str = Field(alias="@type")
    id: str
    download_url: str = Field(alias="downloadUrl")
    data: str
