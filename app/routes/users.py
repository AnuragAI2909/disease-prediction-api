from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    RegisterRequest,
    UserResponse,
    UserUpdate,
    UserPatch
)

from app.dependencies import (
    get_current_user,
    get_current_admin
)

from app.services.user_service import (
    register_user,
    list_users,
    update_existing_user,
    delete_existing_user
)


router = APIRouter()


@router.get(
    "/users",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return list_users(db)


@router.post(
    "/users",
    response_model=UserResponse
)
def create_user(
    user_data: RegisterRequest,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return register_user(
        db,
        user_data.username,
        user_data.password
    )


@router.put(
    "/users/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return update_existing_user(
        db,
        user_id,
        user_data.username,
        user_data.password
    )


@router.patch(
    "/users/{user_id}",
    response_model=UserResponse
)
def patch_user(
    user_id: int,
    user_data: UserPatch,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return update_existing_user(
        db,
        user_id,
        user_data.username,
        user_data.password
    )


@router.delete(
    "/users/{user_id}"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return delete_existing_user(
        db,
        user_id
    )