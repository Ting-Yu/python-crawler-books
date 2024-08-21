from sqlalchemy import Column, String, BigInteger, Integer, Text, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config
from pprint import pformat


class PurchaseItem(sqlalchemy_config.Base):
    __tablename__ = 'purchase_items'

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    purchase_id = Column(String(255), ForeignKey('purchases.purchase_id', ondelete='CASCADE'), nullable=False)
    publisher_id = Column(BigInteger, ForeignKey('publishers.publisher_id'), nullable=False)
    book_id = Column(BigInteger, ForeignKey('books.book_id'), nullable=False)
    price = Column(Integer, nullable=False, default=0, comment='price of the book')
    amount = Column(Integer, nullable=False, default=0, comment='amount of the book')
    status = Column(String(255), nullable=False, default='pending', comment='pending, processing, completed, cancelled')
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    sale_discount = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='sale discount of the book')
    purchase_discount = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='purchase discount of the book')
    arrival_amount = Column(Integer, nullable=False, default=0, comment='arrival amount of the book')

    purchase = relationship("Purchase", back_populates="purchase_items")
    publisher = relationship("Publisher", back_populates="purchase_items")
    book = relationship("Book", back_populates="purchase_items")
    order_item = relationship("OrderItem", back_populates="purchase_item")


def update_purchase_item_by_id(db: sqlalchemy_config.Session, purchase_item_id: int, updates: dict):
    purchase_item = db.query(PurchaseItem).filter(PurchaseItem.id == purchase_item_id).first()
    # print(f"*** Update Purchase Item: {purchase_item_id}")
    if purchase_item:
        for key, value in updates.items():
            # print(f"*** Update Purchase Item: {key} = {value}")
            if hasattr(purchase_item, key):
                setattr(purchase_item, key, value)
        # purchase_item_dict = vars(purchase_item)
        # print(f"*** Set Purchase Item: {pformat(purchase_item_dict)}")
        db.commit()
        db.refresh(purchase_item)
    return purchase_item

def get_purchase_item_by_book_id(db: sqlalchemy_config.Session, book_id: int):
    return db.query(PurchaseItem).filter(PurchaseItem.book_id == book_id).all()

def update_purchase_item_by_book_id(db: sqlalchemy_config.Session, book_id: int, updates: dict):
    purchase_items = db.query(PurchaseItem).filter(PurchaseItem.book_id == book_id).all()
    if purchase_items:
        for purchase_item in purchase_items:
            for key, value in updates.items():
                if hasattr(purchase_item, key):
                    setattr(purchase_item, key, value)
        db.commit()
        db.refresh(purchase_item)
