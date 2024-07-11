from sqlalchemy import Column, String, BigInteger, Integer, Text, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config

class PurchaseItem(sqlalchemy_config.Base):
    __tablename__ = 'purchase_items'

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    purchase_id = Column(String(255), ForeignKey('purchases.purchase_id', ondelete='CASCADE'), nullable=False)
    publisher_id = Column(BigInteger, ForeignKey('publishers.publisher_id'), nullable=False)
    book_id = Column(BigInteger, ForeignKey('books.book_id'), nullable=False)
    price = Column(Integer, nullable=False, default=0, comment='price of the book')
    amount = Column(Integer, nullable=False, default=0, comment='amount of the book')
    status = Column(String(255), nullable=False, default='pending', comment='pending, processing, completed, cancelled')
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    sale_discount = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='sale discount of the book')
    purchase_discount = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='purchase discount of the book')
    arrival_amount = Column(Integer, nullable=False, default=0, comment='arrival amount of the book')

    purchase = relationship("Purchase", back_populates="purchase_items")
    publisher = relationship("Publisher", back_populates="purchase_items")
    book = relationship("Book", back_populates="purchase_items")
    order_item = relationship("OrderItem", back_populates="purchase_item")

