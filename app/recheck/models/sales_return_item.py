from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config

class SalesReturnItem(sqlalchemy_config.Base):
    __tablename__ = 'sales_return_items'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sales_return_id = Column(String(255), ForeignKey('sales_returns.sales_return_id'), nullable=False, index=True)
    book_id = Column(BigInteger, ForeignKey('books.book_id'), nullable=True, index=True)
    temp_isbn = Column(String(255), nullable=True)
    temp_book_name = Column(String(255), nullable=True)
    temp_book_id = Column(BigInteger, nullable=True)
    expected_return_quantity = Column(Integer, nullable=False, default=0, comment='預計退量')
    actual_return_quantity = Column(Integer, nullable=False, default=0, comment='實際退量')
    defective_quantity = Column(Integer, nullable=False, default=0, comment='瑕疵量')
    price = Column(Integer, nullable=False, default=0, comment='退貨單價')
    sale_discount = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='銷售折扣')
    tax = Column(String(255), nullable=True, comment='稅')
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    sales_return = relationship("SalesReturn", back_populates="sales_return_items")
    book = relationship("Book", back_populates="sales_return_items")
    sales_return_shipping = relationship("SalesReturnShipping", back_populates="sales_return_item")
    sales_return_defective = relationship("SalesReturnDefective", back_populates="sales_return_item")

def get_all_sales_return_items(db: sqlalchemy_config.Session, filters: list, skip: int = 0,):
    query = db.query(SalesReturnItem)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return query.offset(skip).all()

def get_sales_return_item_by_id(db: sqlalchemy_config.Session, sales_return_item_id: int):
    return db.query(SalesReturnItem).filter(SalesReturnItem.id == sales_return_item_id).first()

def get_sales_return_item_by_ids(db: sqlalchemy_config.Session, sales_return_item_ids: list):
    return db.query(SalesReturnItem).filter(SalesReturnItem.id.in_(sales_return_item_ids)).all()

def update_sales_return_item_by_id(db: sqlalchemy_config.Session, sales_return_item_id: int, updates: dict):
    sales_return_item = db.query(SalesReturnItem).filter(SalesReturnItem.id == sales_return_item_id).first()
    if sales_return_item:
        for key, value in updates.items():
            if hasattr(sales_return_item, key):
                setattr(sales_return_item, key, value)
        db.commit()
        db.refresh(sales_return_item)
    return sales_return_item