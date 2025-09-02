from fastapi import FastAPI

app = FastAPI(
    title="CRUD API",
    description="Simple FastAPI CRUD with PostgreSQL and Alembic.",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/health")
def health():
    return {"status": "ok"}

from app.api.routes.users import router as users_router
app.include_router(users_router)
