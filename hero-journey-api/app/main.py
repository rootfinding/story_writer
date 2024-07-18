from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import wizard
from app.database.db import engine, Base
from pydantic.fields import FieldInfo
from app.routers import wizard
from app.database.db import engine, Base
from app.database.db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Hero's Journey API")

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(wizard.router)

# Montar los archivos estáticos
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/api")
async def root():
    return {"message": "Welcome to the Hero's Journey API. Use this API to embark on and evaluate your hero's journey."}
