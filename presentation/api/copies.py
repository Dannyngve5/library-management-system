from fastapi import APIRouter

from config.dependencies import library_service
from presentation.schemas.copy_schema import CopyCreate, CopyResponse

router = APIRouter()


@router.post("/copies", status_code=204)
def create_copies(copy_data: CopyCreate) -> None:
    library_service.add_copies(
        book_id=copy_data.book_id,
        copies=copy_data.copies,
    )
