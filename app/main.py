from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Simple FastAPI CRUD with PostgreSQL and Alembic.",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = settings.BACKEND_CORS_ORIGINS
if settings.ALLOW_ALL_ORIGINS:
    origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],             # Allow all HTTP methods
    allow_headers=["*"],             # Allow all headers
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/cors-test")
def cors_test():
    return {
        "message": "CORS is working!",
        "allowed_origins": settings.BACKEND_CORS_ORIGINS,
        "allow_all_origins": settings.ALLOW_ALL_ORIGINS
    }

from app.api.routes.users import router as users_router
app.include_router(users_router)
