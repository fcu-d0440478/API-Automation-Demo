from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    password: str  # 明文密碼僅用於示範，實際應使用哈希


class UserLogin(BaseModel):
    username: str
    password: str
