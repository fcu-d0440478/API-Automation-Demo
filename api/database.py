import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 獲取環境變數中的資料庫 URL
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://myuser:mypassword@postgres:5432/mydb"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# 提供資料庫會話
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
