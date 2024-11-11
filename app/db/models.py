from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    discounts = relationship("Discount", back_populates="category")

class Subcategory(Base):
    __tablename__ = "subcategories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    discounts = relationship("Discount", back_populates="subcategory")
    
    
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=True)
    price = Column(Float)
    stock = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    sold_date = Column(Date, nullable=True)

    category = relationship("Category", lazy="joined")
    subcategory = relationship("Subcategory", lazy="joined")
    discounts = relationship("Discount", back_populates="product")
    sales = relationship("Sale", back_populates="product")


class Discount(Base):
    __tablename__ = "discounts"
    id = Column(Integer, primary_key=True, index=True)
    percentage = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)

    category = relationship("Category", back_populates="discounts")
    subcategory = relationship("Subcategory", back_populates="discounts")
    product = relationship("Product", back_populates="discounts")


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    actual_price = Column(Float, nullable=False)
    discounted_price = Column(Float, nullable=True)
    sale_date = Column(Date, nullable=False)

    product = relationship("Product", back_populates="sales")