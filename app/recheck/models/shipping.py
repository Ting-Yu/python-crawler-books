from sqlalchemy import Column, String, BigInteger, Date, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from . import sqlalchemy_config

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
