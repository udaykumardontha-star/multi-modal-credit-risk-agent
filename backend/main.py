from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from backend.config import settings
from backend.routers import upload, results

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    yield
    # Shutdown
    pass

app = FastAPI(title="Credit Risk Agent API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/v1")
app.include_router(results.router, prefix="/api/v1/results")

app.mount("/outputs", StaticFiles(directory=settings.OUTPUT_DIR), name="outputs")

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
