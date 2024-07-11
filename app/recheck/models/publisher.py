from sqlalchemy import Column, BigInteger, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from . import sqlalchemy_config

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