from backend.agents.tools.ratio_engine import compute_all_ratios
from backend.models.financial import FinancialStatement

def test_ratios_calculation():
    stmt = FinancialStatement(
        company_name="Test",
        period="FY23",
        currency="USD",
        revenue=1000,
        gross_profit=500,
        ebitda=200,
        net_income=100,
        total_assets=2000,
        total_liabilities=1000,
        total_equity=1000,
        current_assets=500,
        current_liabilities=250,
        cash_and_equivalents=100,
        total_debt=500,
        interest_expense=50
    )
    
    ratios = compute_all_ratios(stmt)
    assert ratios.current_ratio == 2.0
    assert ratios.debt_to_equity == 0.5
    assert ratios.interest_coverage == 4.0
    assert ratios.net_margin == 0.1
    # Z-Score test
    # x1 = 250/2000 = 0.125
    # x2 = 100/2000 = 0.05
    # x3 = 200/2000 = 0.1
    # x4 = 1000/1000 = 1.0
    # x5 = 1000/2000 = 0.5
    # Z = 1.2(0.125) + 1.4(0.05) + 3.3(0.1) + 0.6(1.0) + 1.0(0.5) = 0.15 + 0.07 + 0.33 + 0.6 + 0.5 = 1.65
    assert round(ratios.altman_z_score, 2) == 1.65
