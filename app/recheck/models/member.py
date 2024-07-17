from sqlalchemy import Column, BigInteger, String, Text, Date, DateTime, Boolean, Integer
from sqlalchemy.orm import relationship
from . import sqlalchemy_config
from sqlalchemy.dialects import postgresql

class Member(sqlalchemy_config.Base):
    __tablename__ = 'members'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment='姓名')
    store_name = Column(String(255), nullable=True, comment='店家名稱')
    account = Column(String(255), nullable=False, unique=True, comment='帳號')
    password = Column(String(255), nullable=False, comment='密碼')
    phone = Column(String(255), nullable=True, comment='電話')
    role = Column(Integer, nullable=False, default=1, comment='角色 1.社員 2.非社員 3.前員工 4.轉讓 5.退社')
    cellphone = Column(String(255), nullable=True, comment='手機')
    cellphone_code = Column(String(255), nullable=True, comment='手機區碼')
    country_code = Column(String(255), nullable=True, comment='國碼')
    city = Column(String(255), nullable=True, comment='城市')
    district = Column(String(255), nullable=True, comment='區域')
    zip = Column(String(255), nullable=True, comment='郵遞區號')
    email = Column(String(255), nullable=True, comment='信箱')
    contact_name = Column(String(255), nullable=True, comment='聯絡人')
    address = Column(String(255), nullable=True, comment='地址')
    company_vat = Column(String(255), nullable=True, comment='統編')
    company_name = Column(String(255), nullable=True, comment='公司名稱')
    remark = Column(Text, nullable=True, comment='備註')
    ship_remark = Column(String(255), nullable=True, comment='收件備註')
    locate = Column(String(255), nullable=True, comment='位置')
    logistics = Column(String(255), nullable=True, comment='物流')
    is_active = Column(Boolean, nullable=False, default=True, comment='是否啟用')
    is_hidden = Column(Boolean, nullable=False, default=False, comment='是否隱藏')
    is_removed = Column(Boolean, nullable=False, default=False, comment='是否已刪除')
    join_date = Column(Date, nullable=True, comment='加入日期')
    is_admin = Column(Boolean, nullable=False, default=False, comment='是否為管理員')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    orders = relationship("Order", back_populates="member")
    purchases = relationship("Purchase", back_populates="member")

def get_member_by_name(db: sqlalchemy_config.Session, member_name: str):
    print(f"*** get_member_by_name: {member_name}")
    return db.query(Member).filter(Member.name == member_name).first()

def get_member_by_id(db: sqlalchemy_config.Session, member_id: int):
    return db.query(Member).filter(Member.id == member_id).first()

def get_member_by_ids(db: sqlalchemy_config.Session, members_id: list):
    return db.query(Member).filter(Member.id.in_(members_id)).all()

def get_members_all(db: sqlalchemy_config.Session):
    return db.query(Member).all()