from pydantic import BaseModel, ConfigDict


class CopyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    copy_id: int
    book_id: int
    available: bool


class CopyCreate(BaseModel):
    book_id: int
    copies: int
