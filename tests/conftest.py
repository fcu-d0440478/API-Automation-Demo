import pytest
from api.database import Base, engine, SessionLocal
from api.models.user import UserDB
from api.security import hash_password


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # 清理並初始化資料庫
    Base.metadata.drop_all(bind=engine)  # 清除所有表
    Base.metadata.create_all(bind=engine)  # 創建表

    # 如果需要，可以插入測試數據
    db = SessionLocal()
    db.add_all(
        [
            UserDB(
                username="testuser",
                email="test2@example.com",
                password=hash_password("testpassword"),
            ),
        ]
    )
    db.commit()
    db.close()
