from backend.agents.state import AgentState
from backend.services.pdf_service import pdf_service
from jinja2 import Environment, FileSystemLoader
import os

def memo_gen_node(state: AgentState) -> AgentState:
    job_id = state.get("job_id")
    
    env = Environment(loader=FileSystemLoader(os.path.join("backend", "templates")))
    template = env.get_template("credit_memo.html")
    
    html_out = template.render(
        job_id=job_id,
        statements=state.get("extracted_statements", []),
        ratios=state.get("computed_ratios", {}),
        risk_score=state.get("risk_score", {}),
        commentary=state.get("qualitative_commentary", ""),
        flags=state.get("risk_flags", [])
    )
    
    memo_path = pdf_service.render_html_to_pdf(html_out, job_id)
    
    return {
        "memo_path": memo_path,
        "current_node": "generating memo"
    }
