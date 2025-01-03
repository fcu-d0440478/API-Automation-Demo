from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String
from api.database import Base


class User(BaseModel):
    username: str
    email: EmailStr
    password: str  # 明文密碼僅用於示範，實際應使用哈希


class UserLogin(BaseModel):
    username: str
    password: str


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
