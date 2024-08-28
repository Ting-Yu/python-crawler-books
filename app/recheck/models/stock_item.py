from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Text, Date, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_pagination import paginate
from sqlalchemy.orm import sessionmaker


class StockItem(sqlalchemy_config.Base):
    __tablename__ = 'stock_items'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    stock_id = Column(String(255), ForeignKey('stocks.stock_id'), nullable=False)
    book_id = Column(BigInteger, ForeignKey('books.book_id'), nullable=True)
    custom_amount = Column(Integer, nullable=False, default=0)
    purchase_amount = Column(Integer, nullable=False, default=0)
    in_stock_amount = Column(Integer, nullable=False, default=0)
    flaw_amount = Column(Integer, nullable=False, default=0)
    price = Column(Integer, nullable=False, default=0)
    sale_discount = Column(DECIMAL(10, 3), nullable=False, default=0.000, comment='sale discount of the book')
    purchase_discount = Column(DECIMAL(10, 3), nullable=False, default=0.000, comment='purchase discount of the book')
    tax = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    stock = relationship("Stock", back_populates="stock_items")
    stock_histories = relationship("StockHistory", back_populates="stock_item")
    book = relationship("Book", back_populates="stock_items")


def get_stock_item_by_book_id(db: sqlalchemy_config.Session, book_id: int):
    return db.query(StockItem).filter(StockItem.book_id == book_id).all()


def update_stock_item_by_book_id(db: sqlalchemy_config.Session, book_id: int, updates: dict):
    stock_items = db.query(StockItem).filter(StockItem.book_id == book_id).all()
    if stock_items:
        for stock_item in stock_items:
            for key, value in updates.items():
                if hasattr(stock_item, key):
                    setattr(stock_item, key, value)
        db.commit()
        db.refresh(stock_item)


def update_stock_item_by_id(db: sqlalchemy_config.Session, stock_item_id: int, updates: dict):
    stock_item = db.query(StockItem).filter(StockItem.id == stock_item_id).first()
    print(f"*** Update Stock Item: {stock_item_id}")
    if stock_item:
        for key, value in updates.items():
            print(f"*** Update Stock Item: {key} = {value}")
            if hasattr(stock_item, key):
                setattr(stock_item, key, value)
        # stock_item_dict = vars(stock_item)
        # print(f"*** Set Order Item: {pformat(stock_item_dict)}")
        db.commit()
        db.refresh(stock_item)
    return stock_item
