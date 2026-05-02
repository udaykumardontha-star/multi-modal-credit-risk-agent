from backend.agents.nodes.scoring import scoring_node

def test_scoring_reject_altman():
    state = {
        "computed_ratios": {
            "altman_z_score": 1.5,
            "interest_coverage": 10.0, # Great, but altman is bad
            "debt_to_equity": 0.5,
            "current_ratio": 2.0,
            "ebitda_margin": 0.2,
            "net_margin": 0.1,
            "return_on_assets": 0.1
        }
    }
    result = scoring_node(state)
    assert result["decision"] == "REJECT"

def test_scoring_approve():
    state = {
        "computed_ratios": {
            "altman_z_score": 3.5,
            "interest_coverage": 5.0,
            "debt_to_equity": 0.5,
            "current_ratio": 2.0,
            "ebitda_margin": 0.2,
            "net_margin": 0.15,
            "return_on_assets": 0.1
        }
    }
    result = scoring_node(state)
    assert result["decision"] == "APPROVE"
    assert result["risk_score"]["composite_score"] > 70
