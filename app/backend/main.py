from fastapi import FastAPI
from database.database import engine
import models.produto.produto
from routes.produto.routes_produto import router

models.produto.produto.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)