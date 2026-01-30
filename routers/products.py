from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.database import SessionLocal
from models.products import Products
from schemas.products import Product, ProductCreate, ProductUpdate
from dependencies.auth import get_current_user
from models.users import User

router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(Products).all()

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    db_product = Products(**product.dict())
    db_product.user_id = user.id
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", response_model=Product)
def delete_product(product_id: int, db: Session = Depends(get_db), username: str = Depends(get_current_user) ):
    
    user = db.query(User).filter(User.username == username).first()

    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    if product.user_id != user.id:
        raise HTTPException(status_code=403, detail="Vous n'êtes pas le propriétaire de ce produit")

    
    db.delete(product)
    db.commit()
    return product


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    product.name = product_data.name
    product.prix = product_data.prix

    db.commit()
    db.refresh(product)
    return product


