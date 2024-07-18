from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.journey import Base

DATABASE_URL = "sqlite:///./test.db"  # Actualiza con la URL de tu base de datos

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    
    
    