"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.database import init_database
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup: Initialize database
    print("Starting Expense Tracker application...")
    init_database()
    yield
    # Shutdown
    print("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title="Expense Tracker",
    description="A simple yet powerful expense tracking application",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

