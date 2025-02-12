from sqlalchemy import Column, String, BigInteger, Date, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from . import sqlalchemy_config
from sqlalchemy_pagination import paginate

class Shipping(sqlalchemy_config.Base):
    __tablename__ = 'shippings'

    shipping_id = Column(String(255), primary_key=True, nullable=False)
    member_id = Column(BigInteger, ForeignKey('members.id', ondelete='CASCADE'), nullable=True)
    temp_member_name = Column(String(255), nullable=True)
    shipping_date = Column(Date, nullable=True)
    pickup_date = Column(Date, nullable=True)
    logistics = Column(String(255), nullable=True)
    logistics_id = Column(String(255), nullable=True)
    logistics_date = Column(Date, nullable=True)
    status = Column(String(255), nullable=False, default='pending', comment='pending, processing, pickup, completed, cancelled, error')
    remark = Column(Text, nullable=True)
    created_by = Column(BigInteger, ForeignKey('members.id', ondelete='CASCADE'), nullable=True)
    create_way = Column(String(255), nullable=False, default='auto', comment='auto, console, import')
    pickup_name = Column(String(255), nullable=True)
    pickup_addr = Column(String(255), nullable=True)
    pickup_phone = Column(String(255), nullable=True)
    pickup_cellphone = Column(String(255), nullable=True)
    pickup_email = Column(String(255), nullable=True)
    pickup_remark = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    member = relationship("Member", foreign_keys=[member_id])
    creator = relationship("Member", foreign_keys=[created_by])

    shipping_items = relationship("ShippingItem", back_populates="shipping")
    sales_return_shipping = relationship("SalesReturnShipping", back_populates="shipping")  # 添加這行


def get_paginated_shippings(db: sqlalchemy_config.Session, filters: list, page=1, page_size=10):
    query = db.query(Shipping)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return paginate(query, page, page_size)

def get_shipping_by_shipping_id(db: sqlalchemy_config.Session, shipping_id: str):
    return db.query(Shipping).filter(Shipping.shipping_id == shipping_id).first()

def get_shipping_by_temp_member_name(db: sqlalchemy_config.Session, temp_member_name: str):
    query = db.query(Shipping)
    query = query.filter(Shipping.member_id.is_(None))
    query = query.filter(Shipping.temp_member_name == temp_member_name)
    return query.all()

def update_shipping_by_id(db: sqlalchemy_config.Session, shipping_id: str, updates: dict):
    shipping = db.query(Shipping).filter(Shipping.shipping_id == shipping_id).first()
    if shipping:
        for key, value in updates.items():
            if hasattr(shipping, key):
                setattr(shipping, key, value)
        db.commit()
        db.refresh(shipping)
    return shipping