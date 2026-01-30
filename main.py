from fastapi import FastAPI
from db.database import Base, engine
from routers.products import router as products_router
import models.products  
from routers.auth import router as auth_router
import models.users
from routers.ai import router as ai_router
from dotenv import load_dotenv

load_dotenv()


Base.metadata.create_all(bind=engine)

app = FastAPI(title="API PRODUCTS")

@app.get("/")
def root():
    return {"message": "Bonjour"}

app.include_router(products_router)
app.include_router(auth_router)
app.include_router(ai_router)
