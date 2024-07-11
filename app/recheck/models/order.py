from sqlalchemy import Column, String, BigInteger, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config
from sqlalchemy_pagination import paginate

class Order(sqlalchemy_config.Base):
    __tablename__ = 'orders'

    order_id = Column(String(255), primary_key=True, nullable=False)
    member_id = Column(BigInteger, ForeignKey('members.id', ondelete='CASCADE'), nullable=False)
    total_price = Column(Integer, nullable=False, default=0)
    total_amount = Column(Integer, nullable=False, default=0, comment='total amount of all items')
    total_shipping = Column(Integer, nullable=False, default=0, comment='total shipping amount')
    remark = Column(Text, nullable=True)
    status = Column(String(255), nullable=False, default='pending', comment='pending, processing, completed, cancelled')
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    member = relationship("Member", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

def get_paginated_orders(db: sqlalchemy_config.Session, filters: list, page=1, page_size=10):
    query = db.query(Order)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return paginate(query, page, page_size)
