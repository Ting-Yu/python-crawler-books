from sqlalchemy import Column, BigInteger, String, Text, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from . import sqlalchemy_config

class Supplier(sqlalchemy_config.Base):
    __tablename__ = 'suppliers'

    supplier_id = Column(BigInteger, primary_key=True, autoincrement=True)
    locate = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    contact = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    purchase_mail = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    end_remark = Column(Text, nullable=True, comment='截單備註')
    shipping_reamrk = Column(Text, nullable=True)
    company_vat = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)
    accounting_remark = Column(Text, nullable=True, comment='會計資訊')
    return_remark = Column(Text, nullable=True, comment='退貨備註')
    min_number = Column(Integer, nullable=False, default=0, comment='最小出貨數量')
    min_price = Column(Integer, nullable=False, default=0, comment='最小出貨金額')
    stock_remark = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    position = Column(String(255), nullable=True)
    cellphone = Column(String(255), nullable=True)
    contact_remark = Column(Text, nullable=True)
    restock = Column(String(255), nullable=True)
    accounting_type = Column(String(255), nullable=True)
    condition = Column(String(255), nullable=True)
    end_date = Column(String(255), nullable=True)
    tax = Column(String(255), nullable=True)
    return_goods = Column(String(255), nullable=True)
    return_ship = Column(String(255), nullable=True)
    is_removed = Column(Boolean, nullable=False, default=False)
    checked_amount = Column(Integer, nullable=False, default=0)
    checked_price = Column(Integer, nullable=False, default=0)

    purchases = relationship("Purchase", back_populates="supplier")