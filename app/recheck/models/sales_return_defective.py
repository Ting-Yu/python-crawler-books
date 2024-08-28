from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config

class SalesReturnDefective(sqlalchemy_config.Base):
    __tablename__ = 'sales_return_defective'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sales_return_id = Column(String(255), ForeignKey('sales_returns.sales_return_id'), nullable=False, index=True)
    sales_return_item_id = Column(BigInteger, ForeignKey('sales_return_items.id'), nullable=True, index=True)
    book_id = Column(BigInteger, ForeignKey('books.book_id'), nullable=True, index=True)
    status = Column(String(255), nullable=False, default='pending')
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    sales_return = relationship("SalesReturn", back_populates="sales_return_defective")
    sales_return_item = relationship("SalesReturnItem", back_populates="sales_return_defective")
    book = relationship("Book", back_populates="sales_return_defective")
