from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List
import uuid
import os
import json
from backend.config import settings
from backend.services.storage_service import storage_service
from backend.tasks.celery_tasks import run_analysis, redis_client

router = APIRouter()

@router.post("/analyze", status_code=202)
async def analyze_documents(files: List[UploadFile] = File(...)):
    if len(files) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 files allowed")
        
    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"File type {ext} not allowed")
            
    job_id = str(uuid.uuid4())
    
    # Save files
    saved_paths = await storage_service.save_upload_files(job_id, files)
    
    # Create job in Redis
    redis_client.set(f"job:{job_id}", json.dumps({
        "status": "QUEUED",
        "file_count": len(files)
    }))
    
    # Dispatch Celery task
    run_analysis.delay(job_id, saved_paths)
    
    return {
        "job_id": job_id,
        "status": "queued",
        "file_count": len(files)
    }
