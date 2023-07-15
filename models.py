from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///inventory.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Brands(Base):
    __tablename__ = 'brands'
    brand_id = Column(Integer, primary_key=True)
    brand_name=Column(String)
    product = relationship("Products", back_populates="brand")

class Products(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name=Column(String)
    product_quantity=Column(Integer)
    product_price=Column(Integer)
    date_updated=Column(Date)
    brand_id=Column(Integer,ForeignKey("brands.brand_id"))
    brand = relationship("Brands", back_populates="product")
