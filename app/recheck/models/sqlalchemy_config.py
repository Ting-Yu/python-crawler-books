from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# 資料庫連接設定
DB_CONNECTION = ''
DB_HOST = ''
DB_PORT = ''
DB_DATABASE = ''
DB_USERNAME = ''
DB_PASSWORD = ''

# 建立資料庫連線
engine = create_engine(f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}')

# 建立溝通方式
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立繼承
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
