from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from api.models.user import User, UserLogin, UserDB
from api.database import get_db
from api.database import SessionLocal
from api.security import hash_password, verify_password

SECRET_KEY = "your-secret-key"  # 請替換為更安全的密鑰
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# 創建 JWT Token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 註冊用戶
@router.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password)
    new_user = UserDB(
        username=user.username, email=user.email, password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}


# 用戶登入
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="User does not exist")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

        # 查詢資料庫以獲取完整的用戶資料
        db = SessionLocal()
        user = db.query(UserDB).filter(UserDB.username == username).first()
        db.close()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return {"username": user.username, "email": user.email}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
