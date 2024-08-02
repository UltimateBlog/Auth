from sqlalchemy.orm import declarative_base

from sqlalchemy import Column, Integer, String, BigInteger, Boolean

from db.cruds import BaseCRUD
from utils.date_time import current_timestamp

Base = declarative_base()


class Blogger(Base, BaseCRUD):
    __tablename__ = "blooger"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=True)
    firstname = Column(String(30))
    lastname = Column(String(30))
    email = Column(String(150))

    create_date = Column(BigInteger, default=current_timestamp)
    active = Column(Boolean, default=True)

    def __repr__(self):
        return f"Blogger(id={self.id!r}, firstname='{self.firstname!r}, lastname='{self.lastname!r})"
