#not using currently but can be used in future for dependency injection 
from fastapi import Header, HTTPException
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.auth import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.config import settings


def get_app_name():
    return "My Disease Prediction API"

API_KEY = settings.SECRET_KEY  # Replace with your actual API key


def verify_api_key(x_api_key: str | None = Header(default=None)):

    if x_api_key != API_KEY:

        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key")
    return x_api_key

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")




def get_current_user(token: str = Depends(oauth2_scheme)):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM])

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )

        return username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    




def get_current_admin(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.username == current_user).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found")

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required")

    return user