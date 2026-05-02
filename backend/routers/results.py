from fastapi import APIRouter, HTTPException
import json
from backend.tasks.celery_tasks import redis_client

router = APIRouter()

@router.get("/{job_id}")
async def get_results(job_id: str):
    job_data_str = redis_client.get(f"job:{job_id}")
    if not job_data_str:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job_data = json.loads(job_data_str)
    status = job_data.get("status")
    
    if status == "COMPLETE":
        result_str = redis_client.get(f"result:{job_id}")
        if result_str:
            return json.loads(result_str)
        return {"status": "COMPLETE", "detail": "Result data missing"}
        
    elif status == "FAILED":
        raise HTTPException(status_code=500, detail=job_data.get("error", "Unknown error"))
        
    else:
        return {
            "status": status,
            "current_node": job_data.get("current_node", "queued")
        }
