from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy import inspect, text

from .config import get_settings
from .database import Base, SessionLocal, engine
from .routers import admin, auth, certificates, public, student
from .seed import seed_database


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_schema_compatibility()
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


def ensure_schema_compatibility() -> None:
    inspector = inspect(engine)
    if "fees" in inspector.get_table_names():
        fee_columns = {column["name"] for column in inspector.get_columns("fees")}
        with engine.begin() as connection:
            if "receipt_pdf" not in fee_columns:
                connection.execute(text("ALTER TABLE fees ADD COLUMN receipt_pdf VARCHAR(255) DEFAULT ''"))
            if "status" not in fee_columns:
                connection.execute(text("ALTER TABLE fees ADD COLUMN status VARCHAR(20) DEFAULT 'PENDING'"))
            if "transaction_id" not in fee_columns:
                connection.execute(text("ALTER TABLE fees ADD COLUMN transaction_id VARCHAR(100)"))

    if "students" in inspector.get_table_names():
        student_columns = {column["name"] for column in inspector.get_columns("students")}
        with engine.begin() as connection:
            if "batch_id" not in student_columns:
                connection.execute(text("ALTER TABLE students ADD COLUMN batch_id INTEGER REFERENCES batches(id)"))

    if "users" in inspector.get_table_names():
        user_columns = {column["name"] for column in inspector.get_columns("users")}
        with engine.begin() as connection:
            if "email_verified" not in user_columns:
                connection.execute(text("ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE"))
            if "phone_verified" not in user_columns:
                connection.execute(text("ALTER TABLE users ADD COLUMN phone_verified BOOLEAN DEFAULT FALSE"))


@app.get("/api/health")
def health() -> dict[str, bool | str]:
    return {"status": True, "service": "Somarwal Institute API"}


app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(public.router, prefix="/api", tags=["Public"])
app.include_router(certificates.router, prefix="/api/certificate", tags=["Certificates"])
app.include_router(student.router, prefix="/api/student", tags=["Student Portal"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
