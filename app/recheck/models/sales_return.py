from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Text, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config

class SalesReturn(sqlalchemy_config.Base):
    __tablename__ = 'sales_returns'

    sales_return_id = Column(String(255), primary_key=True)
    member_id = Column(BigInteger, ForeignKey('members.id'), nullable=True)
    temp_member_name = Column(String(255), nullable=True)
    logistics_way = Column(Integer, nullable=False, default=1, comment='1: 合作社安排收退貨, 2: 自行寄回')
    logistics_notified = Column(Integer, nullable=False, default=0, comment='通知物流取貨')
    logistics = Column(String(255), nullable=True, comment='物流方式')
    logistics_id = Column(String(255), nullable=True, comment='物流單號')
    logistics_date = Column(Date, nullable=True, comment='回社日期')
    logistics_fee = Column(Integer, nullable=False, default=0, comment='物流費用')
    logistics_need = Column(Integer, nullable=False, default=0, comment='是否需要物流')
    account_date = Column(Date, nullable=True, comment='帳務日期')
    account_tag = Column(String(255), nullable=True, comment='帳務標記')
    return_box_count = Column(Integer, nullable=False, default=1, comment='退貨箱數')
    remark_to_member = Column(Text, nullable=True, comment='給社員備註')
    remark_to_inside = Column(Text, nullable=True, comment='內部備註')
    remark = Column(Text, nullable=True, comment='備註')
    status = Column(String(255), nullable=False, default='pending', comment='pending, processing, completed, cancelled, error')
    created_by = Column(BigInteger, ForeignKey('members.id'), nullable=True)
    create_way = Column(String(255), nullable=False, default='auto', comment='auto, console, import')
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    sales_return_items = relationship("SalesReturnItem", back_populates="sales_return")
    sales_return_shipping = relationship("SalesReturnShipping", back_populates="sales_return")
    sales_return_defective = relationship("SalesReturnDefective", back_populates="sales_return")
def get_all_sales_returns(db: sqlalchemy_config.Session, filters: list, skip: int = 0,):
    query = db.query(SalesReturn)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return query.offset(skip).all()

def get_sales_return_by_id(db: sqlalchemy_config.Session, sales_return_id: int):
    return db.query(SalesReturn).filter(SalesReturn.sales_return_id == sales_return_id).first()

def get_sales_return_by_ids(db: sqlalchemy_config.Session, sales_return_ids: list):
    return db.query(SalesReturn).filter(SalesReturn.sales_return_id.in_(sales_return_ids)).all()

def update_sales_return_by_id(db: sqlalchemy_config.Session, sales_return_id: int, updates: dict):
    sales_return = db.query(SalesReturn).filter(SalesReturn.sales_return_id == sales_return_id).first()
    if sales_return:
        for key, value in updates.items():
            if hasattr(sales_return, key):
                setattr(sales_return, key, value)
        db.commit()
        db.refresh(sales_return)
    return sales_return