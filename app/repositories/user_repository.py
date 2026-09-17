from sqlalchemy.orm import Session

from app.models import User


def get_user_by_username(
    db: Session,
    username: str
):
    return db.query(User).filter(
        User.username == username
    ).first()


def get_user_by_id(
    db: Session,
    user_id: int
):
    return db.query(User).filter(
        User.id == user_id
    ).first()


def get_all_users(
    db: Session
):
    return db.query(User).all()


def create_user(
    db: Session,
    username: str,
    password_hash: str
):
    user = User(
        username=username,
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(
    db: Session,
    user: User,
    username: str | None = None,
    password_hash: str | None = None
):
    if username is not None:
        user.username = username

    if password_hash is not None:
        user.password_hash = password_hash

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User
):
    db.delete(user)
    db.commit()