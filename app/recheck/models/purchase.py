from sqlalchemy import Column, String, BigInteger, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config
from sqlalchemy_pagination import paginate

class Purchase(sqlalchemy_config.Base):
    __tablename__ = 'purchases'

    purchase_id = Column(String(255), primary_key=True, nullable=False)
    supplier_id = Column(BigInteger, ForeignKey('suppliers.supplier_id'), nullable=False)
    member_id = Column(BigInteger, ForeignKey('members.id'), nullable=True)
    status = Column(String(255), nullable=False, default='pending', comment='pending, processing, completed, cancelled')
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    supplier = relationship("Supplier", back_populates="purchases")
    member = relationship("Member", back_populates="purchases")
    purchase_items = relationship("PurchaseItem", back_populates="purchase")


def get_paginated_purchases(db: sqlalchemy_config.Session, filters: list, page=1, page_size=10):
    query = db.query(Purchase)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return paginate(query, page, page_size)
