import datetime
import os

from sqlalchemy import DateTime, Integer, String, func, Text, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")

PG_DSN = (
    f"postgresql+asyncpg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class User(Base):

    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now())


    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "registration_time": int(self.registration_time.timestamp()),
        }


class Advertisement(Base):
    __tablename__ = "advertisements"

    id = mapped_column(Integer, primary_key=True)
    heading = mapped_column(String(20), nullable=False)
    description = mapped_column(Text)
    date_of_creation = mapped_column(DateTime, server_default=func.now())
    user_id = mapped_column(Integer, ForeignKey("app_users.id", ondelete="CASCADE"))
    user = relationship("User", backref="advertisements")



    @property
    def json(self):

        return {
            "id": self.id,
            "heading": self.heading,
            "description": self.description,
            "date_of_creation": self.date_of_creation,
            "user_id": self.user_id,
        }

