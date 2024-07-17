from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Text, Date, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_pagination import paginate

class Book(sqlalchemy_config.Base):
    __tablename__ = 'books'

    book_id = Column(BigInteger, primary_key=True, autoincrement=True)
    isbn = Column(String(255), nullable=True, comment='ISBN')
    title = Column(String(255), nullable=False, comment='書名')
    publisher_id = Column(BigInteger, ForeignKey('publishers.publisher_id'), nullable=False, comment='出版社編號')
    book_crawler_id = Column(String(255), nullable=True)
    published_at = Column(Date, nullable=True, comment='出版日期')
    author = Column(String(255), nullable=False, comment='作者')
    translator = Column(String(255), nullable=True, comment='譯者')
    cover = Column(String(255), nullable=True, comment='封面')
    price = Column(Integer, nullable=False, comment='定價')
    tax = Column(String(255), nullable=False, comment='稅別')
    sale_discount = Column(DECIMAL(10, 2), nullable=False)
    purchase_discount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(Text, nullable=True, comment='內容簡介')
    author_intro = Column(Text, nullable=True, comment='作者簡介')
    catalog = Column(Text, nullable=True, comment='目錄')
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    stock = Column(Integer, nullable=False, default=0)
    status = Column(Integer, nullable=False, default=1, comment='書籍狀態')
    origin_title = Column(String(255), nullable=True, comment='原文書名')
    barcode = Column(String(255), nullable=True, comment='條碼')
    book_number = Column(String(255), nullable=True, comment='書號')
    book_type = Column(Integer, nullable=False, default=1, comment='商品類別')
    can_refund = Column(Integer, nullable=False, default=0, comment='可否退書')
    limit_count = Column(Integer, nullable=False, default=0, comment='限定本數')
    author_foreign = Column(String(255), nullable=True, comment='作者外文名')
    china_book_class = Column(String(255), nullable=True, comment='中國圖書分類號')
    open_number = Column(String(255), nullable=True, comment='開數')
    page_count = Column(Integer, nullable=False, default=0, comment='頁數')
    edition = Column(String(255), nullable=True, comment='版次')
    soft_hard_cover = Column(String(255), nullable=True, comment='平/精裝')
    online_date = Column(Date, nullable=True, comment='上架日期')
    project_intro = Column(Text, nullable=True, comment='專案簡介')
    reward_history = Column(Text, nullable=True, comment='得獎與推薦紀錄')
    important_event = Column(Text, nullable=True, comment='重要事件')
    publisher_name = Column(String(255), nullable=True)

    publisher = relationship("Publisher", back_populates="books")
    order_items = relationship("OrderItem", back_populates="book")
    purchase_items = relationship("PurchaseItem", back_populates="book")
    shipping_items = relationship("ShippingItem", back_populates="book")


def get_all_books(db: sqlalchemy_config.Session, filters: list, skip: int = 0, limit: int = 30):
    query = db.query(Book)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return query.offset(skip).limit(limit).all()

    " example usage "
    # filters = [
    #     Book.book_crawler_id.is_not(None),
    #     Book.description.not_like('%簡介%')
    #     # Add more filter conditions as needed
    # ]
    #
    # books = get_all_books(db, filters)

def get_book_by_id(db: sqlalchemy_config.Session, book_id: int):
    return db.query(Book).filter(Book.book_id == book_id).first()

def get_book_by_ids(db: sqlalchemy_config.Session, book_ids: list):
    return db.query(Book).filter(Book.book_id.in_(book_ids)).all()
def get_book_by_isbns(db: sqlalchemy_config.Session, isbns: list):
    return db.query(Book).filter(Book.isbn.in_(isbns)).all()
def get_book_by_isbn(db: sqlalchemy_config.Session, isbn: str):
    return db.query(Book).filter(Book.isbn == isbn).first()

def get_paginated_books(db: sqlalchemy_config.Session, filters: list, page=1, page_size=10):
    query = db.query(Book)
    for filter_condition in filters:
        query = query.filter(filter_condition)
    return paginate(query, page, page_size)

def upsert_book(db: sqlalchemy_config.Session, book_data: dict):
    try:
        # Check if the book already exists based on ISBN
        existing_book = db.query(Book).filter(Book.isbn == book_data.get('isbn')).first()

        if existing_book:
            # Update existing book
            # for key, value in book_data.items():
            #     setattr(existing_book, key, value)
            # db.commit()
            return existing_book, False  # Return the book and False indicating it was updated
        else:
            # Create new book
            new_book = Book(**book_data)
            db.add(new_book)
            db.commit()
            return new_book, True  # Return the book and True indicating it was created
    except SQLAlchemyError as e:
        db.rollback()
        print(f"An error occurred: {e}")
        return None, None
    except Exception as e:
        # Rollback in case of error
        db.rollback()
        raise e


def update_book_by_book_id(db: sqlalchemy_config.Session, book_id: int, updates: dict):
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if book:
        for key, value in updates.items():
            if hasattr(book, key):
                setattr(book, key, value)
        db.commit()
        db.refresh(book)
    return book
