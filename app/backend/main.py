from fastapi import FastAPI
import socket
from database.database import async_engine, init_db

from routes.product.routes_product import router as product_router
from routes.sales.routes_sales import router as sales_router
from routes.employee.routes_employee import router as employee_router
from routes.supplier.routes_supplier import router as supplier_router

# Inicializa as tabelas de forma assíncrona
async def on_startup():
    await init_db()

app = FastAPI(docs_url="/docs", openapi_url="/openapi.json", on_startup=[on_startup])

@app.get("/whoami")
async def whoami():
    return {"hostname": socket.gethostname()}

app.include_router(product_router)
app.include_router(sales_router)
app.include_router(employee_router)
app.include_router(supplier_router)
