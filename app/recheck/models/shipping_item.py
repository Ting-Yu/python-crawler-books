from sqlalchemy import Column, BigInteger, String, Integer, DECIMAL, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import sqlalchemy_config
from sqlalchemy_pagination import paginate
from sqlalchemy.orm import sessionmaker


class ShippingItem(sqlalchemy_config.Base):
    __tablename__ = 'shipping_items'

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    shipping_id = Column(String(255), ForeignKey('shippings.shipping_id', ondelete='CASCADE'), nullable=False)
    book_id = Column(BigInteger, ForeignKey('books.book_id', ondelete='SET NULL'), nullable=True)
    isbn = Column(String(255), nullable=True)
    book_name = Column(String(255), nullable=True)
    temp_isbn = Column(String(255), nullable=True)
    temp_book_name = Column(String(255), nullable=True)
    price = Column(Integer, nullable=False, default=0)
    quantity = Column(Integer, nullable=False, default=0)
    sale_discount = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='sale discount of the book')
    purchase_discount = Column(DECIMAL(10, 2), nullable=False, default=0.00, comment='purchase discount of the book')
    tax = Column(String(255), nullable=True)
    remark = Column(Text, nullable=True)
    old_book_id = Column(BigInteger, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    shipping = relationship("Shipping", back_populates="shipping_items")
    book = relationship("Book", back_populates="shipping_items")
    sales_return_shipping = relationship("SalesReturnShipping", back_populates="shipping_item")

def get_paginated_shippings(db: sqlalchemy_config.Session, filters: list, page=1, page_size=10, sort_by=None):
    query = db.query(ShippingItem)
    for filter_condition in filters:
        query = query.filter(filter_condition)

    if sort_by:
        for sort_condition, direction in sort_by:
            if direction == 'asc':
                query = query.order_by(sort_condition.asc())
            elif direction == 'desc':
                query = query.order_by(sort_condition.desc())

    return paginate(query, page, page_size)

def get_shipping_item_by_temp_isbn(db: sqlalchemy_config.Session, temp_isbn: int):
    return db.query(ShippingItem).filter(ShippingItem.temp_isbn == temp_isbn).all()

def get_shipping_item_by_temp_book_name(db: sqlalchemy_config.Session, temp_book_name: str):
    return db.query(ShippingItem).filter(ShippingItem.temp_book_name == temp_book_name).all()

def update_shipping_item_by_temp_isbn(db: sqlalchemy_config.Session, temp_isbn: int, updates: dict):
    shipping_items = db.query(ShippingItem).filter(ShippingItem.temp_isbn == temp_isbn).all()
    if shipping_items:
        for shipping_item in shipping_items:
            for key, value in updates.items():
                if hasattr(shipping_item, key):
                    setattr(shipping_item, key, value)
        db.commit()
        db.refresh(shipping_item)

def update_shipping_item_by_temp_book_name(db: sqlalchemy_config.Session, temp_book_name: str, updates: dict):
    shipping_items = db.query(ShippingItem).filter(ShippingItem.temp_book_name == temp_book_name).all()
    if shipping_items:
        for shipping_item in shipping_items:
            for key, value in updates.items():
                if hasattr(shipping_item, key):
                    setattr(shipping_item, key, value)
        db.commit()
        db.refresh(shipping_item)


# Create a sessionmaker, bind it to your engine
Session = sessionmaker(bind=sqlalchemy_config.engine)


def update_shipping_item_in_chunks(db: Session, updates: list, chunk_size: int = 50):
    for i in range(0, len(updates), chunk_size):
        chunk = updates[i:i + chunk_size]
        # Check if a transaction is already in progress
        if not db.in_transaction():
            with db.begin():  # Start a transaction only if not already in one
                update_chunk_shipping(db, chunk)
        else:
            update_chunk_shipping(db, chunk)


# def update_chunk_shipping(db: Session, chunk: list):
#     input(f"Chunk: {chunk}")
#     book_id_cases = sqlalchemy_config.case(
#         {update['id']: update['book_id'] for update in chunk},
#         else_=ShippingItem.book_id
#     )
#     isbn_cases = sqlalchemy_config.case(
#         {update['id']: update['isbn'] for update in chunk},
#         else_=ShippingItem.isbn
#     )
#
#     db.execute(
#         sqlalchemy_config.update(ShippingItem).
#         values(
#             book_id=book_id_cases,
#             isbn=isbn_cases
#         ).
#         where(ShippingItem.id.in_([update['id'] for update in chunk]))
#     )
#     if db.in_transaction():
#         db.commit()

def update_chunk_shipping(db: Session, chunk: list):
    for update in chunk:
        # Perform an individual update for each item in the chunk
        db.query(ShippingItem).filter(ShippingItem.id == update['id']).update({
            ShippingItem.book_id: update['book_id'],
            ShippingItem.isbn: update['isbn']
        }, synchronize_session=False)
    db.commit()