from sqlalchemy import Column, Integer, String, DateTime, Float, func, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    categories = relationship("Category", back_populates="products")

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)

    products = relationship("Product", back_populates="categories")
