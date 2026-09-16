from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import LoginRequest, TokenResponse
from app.auth import authenticate_user, create_access_token
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import RegisterRequest, TokenResponse
from app.auth import (authenticate_user,create_access_token,hash_password)

router = APIRouter()




@router.post("/register")
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(
        user_data.password
    )

    new_user = User(
        username=user_data.username,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "username": new_user.username
    }






@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = authenticate_user( db,
        form_data.username,
        form_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    token = create_access_token(
        form_data.username
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }