from sqlalchemy import Column, BigInteger, String, Text, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from . import sqlalchemy_config
from sqlalchemy_pagination import paginate
from sqlalchemy.orm import sessionmaker

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
    stocks = relationship("Stock", back_populates="supplier")

def get_all_suppliers(db: sqlalchemy_config.Session, filters: list, skip: int = 0, limit: int = 30):
    query = db.query(Supplier)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return query.offset(skip).limit(limit).all()
def get_paginated_suppliers(db: sqlalchemy_config.Session, filters: list, page=1, page_size=10):
    query = db.query(Supplier)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return paginate(query, page, page_size)

# Create a sessionmaker, bind it to your engine
Session = sessionmaker(bind=sqlalchemy_config.engine)

def update_suppliers_in_chunks(db: Session, updates: list, chunk_size: int = 50):
    for i in range(0, len(updates), chunk_size):
        chunk = updates[i:i + chunk_size]
        # Check if a transaction is already in progress
        if not db.in_transaction():
            with db.begin():  # Start a transaction only if not already in one
                update_chunk(db, chunk)
        else:
            update_chunk(db, chunk)
def update_chunk(db: Session, chunk: list):
    # Prepare CASE statements for each field
    return_goods = sqlalchemy_config.case(
        {update['supplier_id']: update['return_goods'] for update in chunk},
        else_=Supplier.return_goods
    )

    db.execute(
        sqlalchemy_config.update(Supplier).
        values(
            return_goods=return_goods
        ).
        where(Supplier.supplier_id.in_([update['supplier_id'] for update in chunk]))
    )
    if db.in_transaction():
        db.commit()