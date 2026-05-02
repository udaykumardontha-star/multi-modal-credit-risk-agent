import json
from backend.agents.state import AgentState
from backend.agents.tools.ratio_engine import compute_all_ratios
from backend.models.financial import FinancialStatement
from backend.services.llm_service import llm_service

def analysis_node(state: AgentState) -> AgentState:
    statements = state.get("extracted_statements", [])
    if not statements:
        return {"current_node": "analysis failed"}
        
    stmt = FinancialStatement(**statements[0])
    ratios = compute_all_ratios(stmt)
    ratios_dict = ratios.model_dump()
    
    prompt = f"""
You are an expert Credit Risk Analyst. Review the following computed financial ratios and data for {stmt.company_name} ({stmt.period}):
{json.dumps(ratios_dict, indent=2)}

Task 1: Write 2-3 paragraphs of professional qualitative commentary on the financial health, focusing on liquidity, solvency, leverage, and profitability.
Task 2: Identify the top 3 risk flags based on these ratios (e.g. ICR < 1.5, D/E > 3).

Output MUST be valid JSON:
{{
  "commentary": "string",
  "risk_flags": ["flag 1", "flag 2", "flag 3"]
}}
"""
    try:
        response = llm_service.generate_text(prompt)
        response = response.strip()
        if response.startswith("```json"): response = response.replace("```json", "", 1)
        if response.endswith("```"): response = response[:-3]
        response = response.strip()
        
        analysis = json.loads(response)
        commentary = analysis.get("commentary", "No commentary generated.")
        risk_flags = analysis.get("risk_flags", [])
    except Exception as e:
        commentary = "Failed to generate commentary."
        risk_flags = ["Error generating risk flags"]
        
    # Merge engine flags with LLM flags
    all_flags = ratios.flags + risk_flags
        
    return {
        "computed_ratios": ratios_dict,
        "qualitative_commentary": commentary,
        "risk_flags": all_flags,
        "current_node": "computing ratios"
    }
