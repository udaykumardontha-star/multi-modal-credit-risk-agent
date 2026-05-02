import operator
from typing import TypedDict, Annotated, List, Dict, Any, Optional

class AgentState(TypedDict):
    job_id: str
    input_files: List[str]
    parsed_chunks: Annotated[List[Dict[str, Any]], operator.add]
    extracted_statements: List[Dict[str, Any]]
    computed_ratios: Optional[Dict[str, Any]]
    risk_score: Optional[Dict[str, Any]]
    qualitative_commentary: Optional[str]
    risk_flags: List[str]
    decision: Optional[str]
    confidence: Optional[float]
    memo_path: Optional[str]
    errors: Annotated[List[str], operator.add]
    current_node: str
