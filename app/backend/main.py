from fastapi import FastAPI
from database.database import engine
import models.product.product
from routes.product.routes_product import router

models.product.product.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)