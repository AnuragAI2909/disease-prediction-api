from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_current_admin

from app.database import get_db
from app.models import User
from app.schemas import UserResponse, RegisterRequest,UserUpdate,UserPatch
from app.auth import hash_password

router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db), get_current_admin=Depends(get_current_admin)):
    return db.query(User).all()



@router.post(
    "/users",
    response_model=UserResponse)
def create_user(
    user_data: RegisterRequest,
    db: Session = Depends(get_db),
    get_current_admin=Depends(get_current_admin)):

    existing_user = db.query(User).filter(
        User.username == user_data.username).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists")

    hashed_password = hash_password(
        user_data.password)

    new_user = User(
        username=user_data.username,
        password_hash=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put(
    "/users/{user_id}",
    response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.username = user_data.username

    user.password_hash = hash_password(
        user_data.password
    )

    db.commit()
    db.refresh(user)

    return user




@router.patch(
    "/users/{user_id}",
    response_model=UserResponse)
def patch_user(
    user_id: int,
    user_data: UserPatch,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user_data.username is not None:
        user.username = user_data.username

    if user_data.password is not None:
        user.password_hash = hash_password(
            user_data.password
        )

    db.commit()
    db.refresh(user)

    return user




@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}