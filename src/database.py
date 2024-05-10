from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import get_settings

settings = get_settings()
charset = 'utf8mb4'
SQLALCHEMY_DATABASE_URL = f'{settings.MYSQL_DATABASE_URL}?charset={charset}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
