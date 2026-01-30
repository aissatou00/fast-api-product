from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str 
    prix: int

    
class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int    
    
    class Config:
        from_attributes = True
