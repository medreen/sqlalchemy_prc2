from sqlalchemy import ForeignKey
from sqlalchemy import String,Integer,Float,DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

# create a connection to the database
engine = create_engine("sqlite:///./md_db.db", echo=True)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name : Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(100))
    password : Mapped[str] = mapped_column(String(200))
    phone_number: Mapped[str] = mapped_column(String(20))
    
class Product(Base):
    __tablename__ = "products"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_name : Mapped[str] = mapped_column(String(100))
    buying_price : Mapped[float] = mapped_column(Float)
    selling_price : Mapped[float] = mapped_column(Float)

class Sale(Base):
    __tablename__ = "sales"
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    sale_date: Mapped[datetime] = mapped_column(DateTime)

class Sales_detail(Base):
    __tablename__ = "sales_details"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"))
    sale_id : Mapped[int] = mapped_column(ForeignKey("sales.id"))
    quantity : Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Purchase(Base):
    __tablename__ = "purchases"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity : Mapped[int] = mapped_column(Integer)
    buying_price : Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    sales_id : Mapped[int] = mapped_column(ForeignKey("sales.id"))
    amount: Mapped[float] = mapped_column(Float)
    payment_method: Mapped[str] = mapped_column(String(30))
    payment_status: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# create the tables in the database
Base.metadata.create_all(engine)