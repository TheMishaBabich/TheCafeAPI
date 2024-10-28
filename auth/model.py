from datetime import datetime

from sqlalchemy import DateTime
import sqlalchemy.orm as so

from db import Base


class User(Base):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str]
    email: so.Mapped[str]
    password: so.Mapped[str]
    created_date: so.Mapped[datetime] = so.mapped_column(DateTime(timezone=True), default=datetime.now)

