import os
import shutil
from typing import List
from fastapi import UploadFile
from backend.config import settings

class StorageService:
    def __init__(self):
        self.base_dir = "/tmp/uploads"
        os.makedirs(self.base_dir, exist_ok=True)

    async def save_upload_files(self, job_id: str, files: List[UploadFile]) -> List[str]:
        job_dir = os.path.join(self.base_dir, job_id)
        os.makedirs(job_dir, exist_ok=True)
        
        saved_paths = []
        for file in files:
            file_path = os.path.join(job_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            saved_paths.append(file_path)
            
        return saved_paths
        
    def cleanup_job_files(self, job_id: str):
        job_dir = os.path.join(self.base_dir, job_id)
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)

storage_service = StorageService()
