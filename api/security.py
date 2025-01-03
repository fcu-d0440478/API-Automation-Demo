from passlib.context import CryptContext

# 配置密碼哈希算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 密碼加密函數
def hash_password(password: str) -> str:
    """使用 bcrypt 哈希加密密碼"""
    return pwd_context.hash(password)


# 密碼驗證函數
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證用戶輸入的密碼是否匹配存儲的哈希密碼"""
    return pwd_context.verify(plain_password, hashed_password)
