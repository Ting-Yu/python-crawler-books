from sqlalchemy import Column, String, BigInteger, Integer, Text, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config

class OrderItem(sqlalchemy_config.Base):
    __tablename__ = 'order_items'

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    order_id = Column(String(255), ForeignKey('orders.order_id', ondelete='CASCADE'), nullable=False)
    book_id = Column(BigInteger, ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    price = Column(Integer, nullable=False, default=0, comment='price of the book')
    sale_discount = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    use_type = Column(Integer, nullable=False, default=1)
    activity_date = Column(String(255), nullable=True, comment='activity date if use_type is 2')
    remark = Column(Text, nullable=True)
    status = Column(String(255), nullable=False, default='pending', comment='pending, processing, completed, cancelled')
    purchase_item_id = Column(BigInteger, ForeignKey('purchase_items.id'), nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    order = relationship("Order", back_populates="order_items")
    book = relationship("Book", back_populates="order_items")
    purchase_item = relationship("PurchaseItem", back_populates="order_items")