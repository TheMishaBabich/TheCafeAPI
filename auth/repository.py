from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from . import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_user(self, user: User) -> User:
        self.db.add(user)
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def save(self, instance: User) -> User:
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance