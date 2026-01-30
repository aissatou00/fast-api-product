from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    prix = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)