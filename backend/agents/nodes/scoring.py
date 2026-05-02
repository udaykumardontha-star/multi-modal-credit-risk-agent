from backend.agents.state import AgentState
from backend.models.risk import RiskScore
import math

def scoring_node(state: AgentState) -> AgentState:
    ratios = state.get("computed_ratios", {})
    
    # 12 expected ratios minus flags
    expected_ratios = 12
    valid_ratios = sum(1 for k, v in ratios.items() if k != "flags" and v is not None)
    confidence = (valid_ratios / expected_ratios) * 100 if expected_ratios > 0 else 0
    
    def score_ratio(value, good_thresh, bad_thresh, higher_is_better=True):
        if value is None: return 50 # Neutral default
        if higher_is_better:
            if value >= good_thresh: return 100
            if value <= bad_thresh: return 0
            return ((value - bad_thresh) / (good_thresh - bad_thresh)) * 100
        else:
            if value <= good_thresh: return 100
            if value >= bad_thresh: return 0
            return ((bad_thresh - value) / (bad_thresh - good_thresh)) * 100

    s_z = score_ratio(ratios.get("altman_z_score"), 2.99, 1.81)
    s_ic = score_ratio(ratios.get("interest_coverage"), 3.0, 1.0)
    s_de = score_ratio(ratios.get("debt_to_equity"), 1.0, 3.0, higher_is_better=False)
    s_cr = score_ratio(ratios.get("current_ratio"), 1.5, 1.0)
    s_ebm = score_ratio(ratios.get("ebitda_margin"), 0.15, 0.05)
    s_nm = score_ratio(ratios.get("net_margin"), 0.10, 0.02)
    s_roa = score_ratio(ratios.get("return_on_assets"), 0.05, 0.01)
    
    composite_score = (s_z * 0.25) + (s_ic * 0.20) + (s_de * 0.15) + \
                      (s_cr * 0.15) + (s_ebm * 0.10) + (s_nm * 0.10) + (s_roa * 0.05)
                      
    composite_score = min(max(composite_score, 0), 100)
    
    altman_z = ratios.get("altman_z_score")
    
    if altman_z is not None and altman_z < 1.81:
        decision = "REJECT"
        rationale = "Automatic rejection due to Altman Z-Score indicating distress (<1.81)."
    elif composite_score >= 70:
        decision = "APPROVE"
        rationale = f"Composite score {composite_score:.1f} meets approval threshold."
    elif composite_score >= 45:
        decision = "REFER"
        rationale = f"Composite score {composite_score:.1f} requires manual review."
    else:
        decision = "REJECT"
        rationale = f"Composite score {composite_score:.1f} is below acceptable threshold."
        
    risk_score = RiskScore(
        composite_score=composite_score,
        altman_z=altman_z,
        decision=decision,
        confidence=confidence,
        rationale=rationale
    )
    
    return {
        "risk_score": risk_score.model_dump(),
        "decision": decision,
        "confidence": confidence,
        "current_node": "scoring risk"
    }
