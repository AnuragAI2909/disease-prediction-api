from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models import User
from app.config import settings
from app.repositories.user_repository import get_user_by_username

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def authenticate_user(
    db: Session,
    username: str,
    password: str):

    user = get_user_by_username(db,username)

    if user is None:
        return None

    if not verify_password(password,user.password_hash):
        return None

    return user



def create_access_token(username: str):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_password(password: str):
    return pwd_context.hash(password)
def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )