from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.repositories.user_repository import (
    get_user_by_username,
    get_user_by_id,
    get_all_users,
    create_user,
    update_user,
    delete_user
)


def register_user(
    db: Session,
    username: str,
    password: str
):
    existing_user = get_user_by_username(
        db,
        username
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    password_hash = hash_password(password)

    return create_user(
        db,
        username,
        password_hash
    )


def list_users(
    db: Session
):
    return get_all_users(db)


def update_existing_user(
    db: Session,
    user_id: int,
    username: str | None = None,
    password: str | None = None
):
    user = get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if username is not None:

        existing_user = get_user_by_username(
            db,
            username
        )

        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

    password_hash = None

    if password is not None:
        password_hash = hash_password(password)

    return update_user(
        db,
        user,
        username,
        password_hash
    )


def delete_existing_user(
    db: Session,
    user_id: int
):
    user = get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    delete_user(
        db,
        user
    )

    return {
        "message": "User deleted successfully"
    }