from sqlalchemy import Column, BigInteger, String, Integer, DECIMAL, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import sqlalchemy_config
from sqlalchemy_pagination import paginate

class ShippingItem(sqlalchemy_config.Base):
    __tablename__ = 'shipping_items'

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    shipping_id = Column(String(255), ForeignKey('shippings.shipping_id', ondelete='CASCADE'), nullable=False)
    book_id = Column(BigInteger, ForeignKey('books.book_id', ondelete='SET NULL'), nullable=True)
    isbn = Column(String(255), nullable=True)
    book_name = Column(String(255), nullable=True)
    temp_isbn = Column(String(255), nullable=True)
    temp_book_name = Column(String(255), nullable=True)
    price = Column(Integer, nullable=False, default=0)
    quantity = Column(Integer, nullable=False, default=0)
    sale_discount = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='sale discount of the book')
    purchase_discount = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='purchase discount of the book')
    tax = Column(String(255), nullable=True)
    remark = Column(Text, nullable=True)
    old_book_id = Column(BigInteger, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    shipping = relationship("Shipping", back_populates="shipping_items")
    book = relationship("Book", back_populates="shipping_items")


def get_paginated_shippings(db: sqlalchemy_config.Session, filters: list, page=1, page_size=10, sort_by=None):
    query = db.query(ShippingItem)
    for filter_condition in filters:
        query = query.filter(filter_condition)

    if sort_by:
        for sort_condition, direction in sort_by:
            if direction == 'asc':
                query = query.order_by(sort_condition.asc())
            elif direction == 'desc':
                query = query.order_by(sort_condition.desc())

    return paginate(query, page, page_size)


def update_purchase_item_by_temp_isbn(db: sqlalchemy_config.Session, temp_isbn: int, updates: dict):
    purchase_item = db.query(ShippingItem).filter(ShippingItem.temp_isbn == temp_isbn).first()
    if purchase_item:
        for key, value in updates.items():
            if hasattr(purchase_item, key):
                setattr(purchase_item, key, value)
        db.commit()
        db.refresh(purchase_item)
    return purchase_item
