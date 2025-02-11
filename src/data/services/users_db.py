import secrets
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserSchema

def is_user_valid(session: Session, token: str) -> bool:
    user = session.query(User).filter(User.token == token).first()
    if not user:
        return False
    return True

def get_user_id(session: Session, token: str) -> int:
    user = session.query(User).filter(User.token == token).first()
    return user.id

def create_user(session: Session, name: str) -> str:
    token = f'Bearer {secrets.token_urlsafe(16)}'
    session.add(User(name=name, token=token, is_premium=True, created_at=datetime.now()))
    session.commit()

    return token

def modificate_user(session: Session, id: int, is_premium: bool) -> None:
    session.query(User).filter(User.id == id).update({
        "is_premium": is_premium
    })
    session.commit()

def change_user_name(session: Session, id: int, name: str) -> None:
    session.query(User).filter(User.id == id).update({
        "name": name
    })
    session.commit()

def delete_user(session: Session, id: int) -> None:
    session.query(User).filter(User.id == id).delete()
    session.commit()

def get_users(session: Session) -> list:
    models = session.query(User).all()
    return UserSchema().dump(models, many=True)

def get_user(session: Session, id: int) -> dict:
    model = session.query(User).filter(User.id == id).first()
    return UserSchema().dump(model)