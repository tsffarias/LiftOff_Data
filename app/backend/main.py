from fastapi import FastAPI
from database.database import engine
import models.product.product
import models.sales.sales
from routes.product.routes_product import router as product_router
from routes.sales.routes_sales import router as sales_router

models.product.product.Base.metadata.create_all(bind=engine)
models.sales.sales.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(product_router)
app.include_router(sales_router)
