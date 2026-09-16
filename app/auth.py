from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models import User
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


fake_user = {
    "username": "anurag",
    "password": "$2b$12$8y5B8iZWKLmkLGXBXWwe0Osrjzr6BOd.wTkOEvpSc7s9O.xnH3HMi"
}


def authenticate_user(
    db: Session,
    username: str,
    password: str):

    user = db.query(User).filter(User.username == username).first()

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