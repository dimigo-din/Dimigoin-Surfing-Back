# surfing-back/app/cruds/auth_crud.py

from dataclasses import dataclass

import uuid

from sqlalchemy.orm import Session

from app.models.user_model import User, UserInterface
from app.models.refresh_token_model import RefreshToken, RefreshTokenInterface

@dataclass
class UserInfo:
    user_id: int
    role: str

def get_user_by_id(db: Session, user_id: int) -> UserInterface | None:
    return db.query(User).get(user_id)

def create_user(db: Session, user_id: int, user_email: str) -> None:
    new_user = User(user_id=user_id, role="STUDENT", user_email=user_email)
    db.add(new_user)
    db.commit()
    return

def create_refresh_token(db: Session, user_id: int) -> str:
    refresh_token = uuid.uuid4().hex
    new_refresh_token = RefreshToken(user_id=user_id, refresh_token=refresh_token)
    db.add(new_refresh_token)
    db.commit()
    return refresh_token

def delete_refresh_token(db: Session, refresh_token: str) -> bool:
    try:
        db.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token).delete()
        db.commit()
        return True
    except:
        return False

def get_user_info_by_refresh_token(db: Session, refresh_token: str) -> UserInfo | None:
    user_refresh_token: RefreshTokenInterface | None = db.query(RefreshToken).get(refresh_token)
    if user_refresh_token is None:
        return None
    user = get_user_by_id(db, user_refresh_token.user_id)
    if user is None:
        return None
    return UserInfo(user_id=user.user_id, role=user.role)