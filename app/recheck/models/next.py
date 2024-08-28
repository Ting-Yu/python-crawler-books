from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Text, Date, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_pagination import paginate
from sqlalchemy.orm import sessionmaker

class Next(sqlalchemy_config.Base):
    __tablename__ = 'nexts'

    next_id = Column(BigInteger, primary_key=True, autoincrement=True)
    member_id = Column(BigInteger, ForeignKey('members.id'), nullable=False, comment='會員編號')
    book_id = Column(BigInteger, ForeignKey('books.book_id'), nullable=False, comment='書籍編號')
    quantity = Column(Integer, nullable=False, comment='數量')
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    book = relationship("Book", back_populates="nexts")
    member = relationship("Member", back_populates="nexts")

def get_next_by_book_id(db: sqlalchemy_config.Session, book_id: int):
    return db.query(Next).filter(Next.book_id == book_id).all()

def update_next_by_book_id(db: sqlalchemy_config.Session, book_id: int, updates: dict):
    nexts = db.query(Next).filter(Next.book_id == book_id).all()
    if nexts:
        for next in nexts:
            for key, value in updates.items():
                if hasattr(next, key):
                    setattr(next, key, value)
        db.commit()
        db.refresh(next)
