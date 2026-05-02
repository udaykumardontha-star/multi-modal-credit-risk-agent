from pydantic import BaseModel, Field
from typing import Literal, Optional

class RiskScore(BaseModel):
    composite_score: float = Field(..., ge=0, le=100, description="Weighted composite risk score from 0 to 100")
    altman_z: Optional[float] = Field(..., description="Altman Z-Score value")
    decision: Literal["APPROVE", "REFER", "REJECT"] = Field(..., description="Final credit decision")
    confidence: float = Field(..., ge=0, le=100, description="Confidence percentage based on data completeness")
    rationale: str = Field(..., description="Short rationale for the decision")
