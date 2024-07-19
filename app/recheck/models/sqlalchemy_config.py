import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import case, update

# 資料庫連接設定
DB_CONNECTION = ''
DB_HOST = os.environ.get('FRIBOOKER_DB_HOST')
DB_PORT = os.environ.get('FRIBOOKER_DB_PORT')
DB_DATABASE = os.environ.get('FRIBOOKER_DB_DATABASE')
DB_USERNAME = os.environ.get('FRIBOOKER_DB_USERNAME')
DB_PASSWORD = os.environ.get('FRIBOOKER_DB_PASSWORD')

print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")
print(f"DB_DATABASE: {DB_DATABASE}")
print(f"DB_PASSWORD: {DB_PASSWORD}")
input("Press Enter to continue... Start...")

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
