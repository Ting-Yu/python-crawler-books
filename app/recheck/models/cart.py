from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Text, Date, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_pagination import paginate
from sqlalchemy.orm import sessionmaker

class Cart(sqlalchemy_config.Base):
    __tablename__ = 'carts'

    cart_id = Column(BigInteger, primary_key=True, autoincrement=True)
    member_id = Column(BigInteger, ForeignKey('members.id'), nullable=False, comment='會員編號')
    book_id = Column(BigInteger, ForeignKey('books.book_id'), nullable=False, comment='書籍編號')
    use_type = Column(String(255), nullable=True, comment='書本用途')
    activity_date = Column(Date, nullable=True, comment='活動日期')
    remark = Column(Text, nullable=True, comment='備註')
    quantity = Column(Integer, nullable=False, comment='數量')
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    # book = relationship("Book", back_populates="carts")
    # member = relationship("Member", back_populates="carts")


def get_cart_by_book_id(db: sqlalchemy_config.Session, book_id: int):
    return db.query(Cart).filter(Cart.book_id == book_id).all()

def update_cart_by_book_id(db: sqlalchemy_config.Session, book_id: int, updates: dict):
    carts = db.query(Cart).filter(Cart.book_id == book_id).all()
    if carts:
        for cart in carts:
            for key, value in updates.items():
                if hasattr(cart, key):
                    setattr(cart, key, value)
        db.commit()
        db.refresh(cart)
