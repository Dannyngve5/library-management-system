from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    name: str
    role: str


class UserCreate(BaseModel):
    name: str
    role: str


class UserPatch(BaseModel):
    name: str | None = None
    role: str | None = None
