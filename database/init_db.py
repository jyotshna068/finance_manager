from config.database import Base, engine
from database import models  # noqa: ensures models are registered

def init_db():
    """Creates all tables. Run once during setup."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully.")

if __name__ == "__main__":
    init_db()