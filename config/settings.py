import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "AI Personal Finance Manager"
    ENV = os.getenv("ENV", "development")

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/finance_db")

    # Auth
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

    # LLM
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

    # File storage
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")
    MAX_FILE_SIZE_MB = 15

settings = Settings()