from fastapi import APIRouter

from config.dependencies import user_service

from presentation.schemas.user_schema import UserResponse, UserCreate, UserPatch

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user(user_data: UserCreate) -> UserResponse:
    return user_service.add_user(name=user_data.name, role=user_data.role)


@router.get("/users/", response_model=list[UserResponse])
def get_users() -> list[UserResponse]:
    return user_service.find_all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int) -> UserResponse:
    return user_service.find_by_id(user_id)


@router.get("/users/role/{role}", response_model=list[UserResponse])
def get_users_by_role(role: str) -> list[UserResponse]:
    return user_service.find_by_role(role)


@router.patch("/users/{user_id}", response_model=UserResponse)
def patch_user(user_id: int, user_data: UserPatch) -> UserResponse:
    return user_service.patch(user_id=user_id, name=user_data.name, role=user_data.role)


@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int) -> None:
    user_service.delete(user_id)
