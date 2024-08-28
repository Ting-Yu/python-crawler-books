from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config

class SalesReturnShipping(sqlalchemy_config.Base):
    __tablename__ = 'sales_return_shipping'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sales_return_id = Column(String(255), ForeignKey('sales_returns.sales_return_id'), nullable=False, index=True)
    sales_return_item_id = Column(BigInteger, ForeignKey('sales_return_items.id'), nullable=True, index=True)
    shipping_id = Column(String(255), ForeignKey('shippings.shipping_id'), nullable=True, index=True)
    shipping_item_id = Column(BigInteger, ForeignKey('shipping_items.id'), nullable=True, index=True)
    book_id = Column(BigInteger, ForeignKey('books.book_id'), nullable=True, index=True)
    amount = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    book = relationship("Book", back_populates="sales_return_shipping")
    sales_return = relationship("SalesReturn", back_populates="sales_return_shipping")
    sales_return_item = relationship("SalesReturnItem", back_populates="sales_return_shipping")
    shipping = relationship("Shipping", back_populates="sales_return_shipping")
    shipping_item = relationship("ShippingItem", back_populates="sales_return_shipping")
