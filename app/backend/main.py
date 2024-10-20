from fastapi import FastAPI
from database.database import engine

import models.product.product
import models.sales.sales
import models.employee.employee
import models.supplier.supplier

from routes.product.routes_product import router as product_router
from routes.sales.routes_sales import router as sales_router
from routes.employee.routes_employee import router as employee_router
from routes.supplier.routes_supplier import router as supplier_router

models.product.product.Base.metadata.create_all(bind=engine)
models.sales.sales.Base.metadata.create_all(bind=engine)
models.employee.employee.Base.metadata.create_all(bind=engine)
models.supplier.supplier.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(product_router)
app.include_router(sales_router)
app.include_router(employee_router)
app.include_router(supplier_router)
