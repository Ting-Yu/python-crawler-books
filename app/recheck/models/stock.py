from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Text, Date, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_pagination import paginate
from sqlalchemy.orm import sessionmaker


class Stock(sqlalchemy_config.Base):
    __tablename__ = 'stocks'

    stock_id = Column(String(255), primary_key=True)
    purchase_id = Column(String(255), nullable=True)
    supplier_id = Column(BigInteger, ForeignKey('suppliers.supplier_id'), nullable=False)
    status = Column(String(255), nullable=False, default='pending', comment='pending, processing, completed, cancelled')
    remark = Column(Text, nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    total_price = Column(Integer, nullable=False, default=0)
    total_purchase_price = Column(Integer, nullable=False, default=0)
    created_by = Column(BigInteger, ForeignKey('members.id'), nullable=True)
    in_stock_date = Column(Date, nullable=True)
    account_date = Column(Date, nullable=True)
    shipping_code = Column(String(255), nullable=True)
    invoice_number = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    # supplier = relationship("Supplier", back_populates="stocks")
    # created_by_member = relationship("Member", back_populates="stocks")
    # purchase = relationship("Purchase", back_populates="stocks")
    stock_items = relationship("StockItem", back_populates="stock")
    # stock_histories = relationship("StockHistory", back_populates="stock")


def get_paginated_stocks(db: sqlalchemy_config.Session, filters: list, page=1, page_size=10):
    query = db.query(Stock)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return paginate(query, page, page_size)
