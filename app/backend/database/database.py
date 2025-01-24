from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Obter as variáveis do arquivo .env
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')

# Criar a URL de conexão do banco de dados assíncrono
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@postgres:{DB_PORT}/{DB_NAME}"

# Criar o motor assíncrono
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# Sessão assíncrona
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base para os modelos declarativos
Base = declarative_base()


# Dependência para injeção de sessão no FastAPI
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


# Inicializar o banco de dados
async def init_db():
    async with async_engine.begin() as conn:
        # Criar as tabelas (migrations podem substituir isso no futuro)
        await conn.run_sync(Base.metadata.create_all)
