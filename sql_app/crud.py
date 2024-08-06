from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(email=user.email, spotify_id=user.spotify_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_history(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.History).offset(skip).limit(limit).all()


def create_user_history(db: Session, history: schemas.HistoryCreate, user_id: int):
    db_history = models.History(**history.model_dump(), owner_id=user_id)
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history
