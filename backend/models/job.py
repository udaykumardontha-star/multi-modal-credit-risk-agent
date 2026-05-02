from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict, Any

class JobStatus(BaseModel):
    job_id: str
    status: Literal["QUEUED", "PROCESSING", "COMPLETE", "FAILED"]
    current_node: Optional[str] = None
    error: Optional[str] = None
    file_count: Optional[int] = 0

class JobResult(BaseModel):
    job_id: str
    status: Literal["COMPLETE"] = "COMPLETE"
    memo_url: str
    extracted_statements: List[Dict[str, Any]]
    computed_ratios: Dict[str, Any]
    risk_score: Dict[str, Any]
    qualitative_commentary: str
    risk_flags: List[str]
    confidence: float
