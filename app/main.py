from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.routers.auth import router as auth_router


app = FastAPI(
    title="PlatePulse API",
    version="1.0.0"
)


# Authentication routes
app.include_router(auth_router)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "PlatePulse API is running"
    }


# Database connection test
@app.get("/test-db")
def test_database():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        return {
            "database": result.scalar()
        }