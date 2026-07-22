from pydantic import BaseModel, ConfigDict
from datetime import date


class LoanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    loan_id: int
    copy_id: int
    user_id: int
    start_date: date
    due_date: date
    returned_date: date | None = None


class LoanCreate(BaseModel):
    book_id: int
    user_id: int
