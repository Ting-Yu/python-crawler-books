from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Text, Date, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_pagination import paginate
from sqlalchemy.orm import sessionmaker


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
    carts = relationship("Cart", back_populates="book")
    nexts = relationship("Next", back_populates="book")
    stock_histories = relationship("StockHistory", back_populates="book")
    stock_items = relationship("StockItem", back_populates="book")
    sales_return_items = relationship("SalesReturnItem", back_populates="book")
    sales_return_shipping = relationship("SalesReturnShipping", back_populates="book")
    sales_return_defective = relationship("SalesReturnDefective", back_populates="book")


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
    query = db.query(Book)
    query = query.filter(Book.isbn.in_(isbns))
    query = query.filter(Book.status != 99)
    return query.all()


def get_book_by_titles(db: sqlalchemy_config.Session, titles: list):
    query = db.query(Book)
    query = query.filter(Book.title.in_(titles))
    query = query.filter(Book.status != 99)
    return query.all()


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


# Create a sessionmaker, bind it to your engine
Session = sessionmaker(bind=sqlalchemy_config.engine)


def bulk_insert_books(upsert_data_list):
    session = Session()  # Create a new session that is bound to the engine
    try:
        session.bulk_insert_mappings(Book, upsert_data_list)
        session.commit()  # Commit the transaction
        print("Batch insert successful.")
    except Exception as e:
        session.rollback()  # Rollback in case of error
        print(f"An error occurred during batch insert: {e}")
    finally:
        session.close()  # Ensure the session is closed after operation


def update_books_in_chunks(db: Session, updates: list, chunk_size: int = 50):
    for i in range(0, len(updates), chunk_size):
        chunk = updates[i:i + chunk_size]
        # Check if a transaction is already in progress
        if not db.in_transaction():
            with db.begin():  # Start a transaction only if not already in one
                update_chunk(db, chunk)
        else:
            update_chunk(db, chunk)


def update_chunk(db: Session, chunk: list):
    publisher_id_cases = sqlalchemy_config.case(
        {update['book_id']: update['publisher_id'] for update in chunk},
        else_=Book.publisher_id
    )
    sale_discount_cases = sqlalchemy_config.case(
        {update['book_id']: update['sale_discount'] for update in chunk},
        else_=Book.sale_discount
    )
    purchase_discount_cases = sqlalchemy_config.case(
        {update['book_id']: update['purchase_discount'] for update in chunk},
        else_=Book.purchase_discount
    )

    can_refund_updates = {update['book_id']: update['can_refund'] for update in chunk}

    can_refund_case = sqlalchemy_config.case(
        *[(Book.book_id == book_id, can_refund) for book_id, can_refund in can_refund_updates.items()],
        else_=Book.can_refund  # Use the current value of can_refund as the default
    )

    db.execute(
        sqlalchemy_config.update(Book).
        values(
            publisher_id=publisher_id_cases,
            sale_discount=sale_discount_cases,
            purchase_discount=purchase_discount_cases,
            can_refund=can_refund_case
        ).
        where(Book.book_id.in_([update['book_id'] for update in chunk]))
    )
    if db.in_transaction():
        db.commit()


def delete_book_by_id(db: sqlalchemy_config.Session, book_id: int):
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        return True
    return False
