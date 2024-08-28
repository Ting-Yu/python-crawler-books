from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Text, Date, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_pagination import paginate
from sqlalchemy.orm import sessionmaker


class StockHistory(sqlalchemy_config.Base):
    __tablename__ = 'stock_history'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    stock_id = Column(String(255), ForeignKey('stocks.stock_id'), nullable=False)
    stock_item_id = Column(BigInteger, ForeignKey('stock_items.id'), nullable=True)
    type = Column(String(255), nullable=False, default='manual', comment='in_stock, to_shipping, system, manual')
    status = Column(String(255), nullable=False, default='pending', comment='pending, processing, completed, cancelled')
    remark = Column(Text, nullable=True)
    book_id = Column(BigInteger, ForeignKey('books.book_id'), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Integer, nullable=False, default=0)
    sale_discount = Column(DECIMAL(10, 3), nullable=False, default=0.000, comment='sale discount of the book')
    purchase_discount = Column(DECIMAL(10, 3), nullable=False, default=0.000, comment='purchase discount of the book')
    tax = Column(String(255), nullable=True)
    created_by = Column(BigInteger, ForeignKey('members.id'), nullable=True)
    in_stock_date = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    stock_before = Column(Integer, nullable=False, default=0)
    stock_after = Column(Integer, nullable=False, default=0)

    stock = relationship("Stock", back_populates="stock_histories")
    stock_item = relationship("StockItem", back_populates="stock_histories")
    book = relationship("Book", back_populates="stock_histories")
    created_by_member = relationship("Member", back_populates="stock_histories")


def get_stock_history_by_book_id(db: sqlalchemy_config.Session, book_id: int):
    return db.query(StockHistory).filter(StockHistory.book_id == book_id).all()


def update_stock_history_by_book_id(db: sqlalchemy_config.Session, book_id: int, updates: dict):
    stock_histories = db.query(StockHistory).filter(StockHistory.book_id == book_id).all()
    if stock_histories:
        for stock_history in stock_histories:
            for key, value in updates.items():
                if hasattr(stock_history, key):
                    setattr(stock_history, key, value)
        db.commit()
        db.refresh(stock_history)
