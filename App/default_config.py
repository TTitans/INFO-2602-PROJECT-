import os

# Use PostgreSQL database URL from environment or fallback to SQLite for local development
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///temp-database.db")
SECRET_KEY = os.environ.get("SESSION_SECRET", "secret key")
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}