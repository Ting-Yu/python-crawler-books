from sqlalchemy import Column, String, BigInteger, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config

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


def get_all_purchases(db: sqlalchemy_config.Session, filters: list, skip: int = 0, limit: int = 30):
    query = db.query(Purchase)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return query.offset(skip).limit(limit).all()