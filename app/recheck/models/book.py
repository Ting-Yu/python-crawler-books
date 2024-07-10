from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Text, Date, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import sqlalchemy_config

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
