from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

engine = create_async_engine(settings.DB_URL, echo=True)

new_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

class BaseModel(DeclarativeBase):
    pass