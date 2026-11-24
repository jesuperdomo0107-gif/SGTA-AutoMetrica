import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://postgres:1234@localhost:5432/autometrica_db"
    ALLOWED_HOSTS: str = "*"
    CORS_ORIGINS: str = "*"
    FRONTEND_URL: str = "http://localhost:5173"
    JWT_SECRET_KEY: str = "autometrica_super_secret_jwt_key_2026_sena_seguro"

    # Configuración SMTP (Gmail / otros)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "AutoMétrica"
    SMTP_FROM_EMAIL: str = ""

    # Configuración SMS (Twilio)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    # Configuración Resend (Envío de correos reales)
    RESEND_API_KEY: str = ""
    RESEND_FROM: str = "AutoMétrica <onboarding@resend.dev>"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()

# Normalizar URL de PostgreSQL para SQLAlchemy (Render usa postgres:// en ocasiones)
db_url = settings.DATABASE_URL.strip()
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

is_production = (
    settings.ENVIRONMENT.lower() == "production"
    or os.getenv("RENDER") == "true"
    or not settings.DEBUG
)

if is_production:
    # En producción (Render): exigir PostgreSQL externo, nunca SQLite efímero
    if db_url.startswith("sqlite"):
        raise RuntimeError(
            "ERROR CRÍTICO DE PRODUCCIÓN: SQLite no está permitido en Render porque el almacenamiento es efímero. "
            "Configura la variable de entorno DATABASE_URL apuntando a tu instancia de Render PostgreSQL."
        )
    engine = create_engine(
        db_url,
        pool_size=5,
        max_overflow=2,
        pool_pre_ping=True,
        pool_recycle=300,
    )
    print("[Base de Datos] Conectado en modo PRODUCCIÓN a PostgreSQL externo.")
else:
    # En desarrollo local: intentar PostgreSQL y hacer fallback a SQLite si no está levantado
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        with engine.connect() as conn:
            pass
        print("[Base de Datos] Conectado exitosamente a PostgreSQL local.")
    except Exception as e:
        print(f"[Base de Datos] No se pudo conectar a PostgreSQL local: {e}")
        print("[Base de Datos] Activando fallback a base de datos SQLite local (autometrica_db.db)...")
        sqlite_url = "sqlite:///./autometrica_db.db"
        engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
