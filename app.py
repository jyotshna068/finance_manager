from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from database.init_db import init_db

from api.auth import router as auth_router
from api.upload import router as upload_router
from api.dashboard import router as dashboard_router
from api.reports import router as reports_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title=settings.APP_NAME, lifespan = lifespan)

# CORS — adjust allow_origins for production deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(dashboard_router)
app.include_router(reports_router)

@app.get("/")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)