from sqlalchemy import Column, BigInteger, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from . import sqlalchemy_config
from sqlalchemy_pagination import paginate

class Publisher(sqlalchemy_config.Base):
    __tablename__ = 'publishers'

    publisher_id = Column(BigInteger, primary_key=True, autoincrement=True)
    supplier_id = Column(BigInteger, ForeignKey('suppliers.supplier_id'), nullable=True)
    name = Column(String(255), nullable=False, comment='出版社名稱')
    remark = Column(Text, nullable=True, comment='備註')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    is_removed = Column(Boolean, nullable=False, default=False)
    sale_discount = Column(Float, nullable=False, default=0, comment='銷折')
    purchase_discount = Column(Float, nullable=False, default=0, comment='進折')
    is_hidden = Column(Boolean, nullable=False, default=False, comment='是否隱藏')

    books = relationship("Book", back_populates="publisher")
    purchase_items = relationship("PurchaseItem", back_populates="publisher")

def get_all_publishers(db: sqlalchemy_config.Session, filters: list, skip: int = 0, limit: int = 30):
    query = db.query(Publisher)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return query.offset(skip).limit(limit).all()
def get_paginated_publishers(db: sqlalchemy_config.Session, filters: list, page=1, page_size=10):
    query = db.query(Publisher)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return paginate(query, page, page_size)

def get_publisher_by_name(db: sqlalchemy_config.Session, name: str):
    return db.query(Publisher).filter(Publisher.name == name).first()

def create_publisher(db: sqlalchemy_config.Session, publisher: Publisher):
    db.add(publisher)
    db.commit()
    return publisher

