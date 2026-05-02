from backend.models.financial import FinancialStatement, ComputedRatios

def compute_all_ratios(statement: FinancialStatement) -> ComputedRatios:
    ratios = ComputedRatios()
    flags = []

    def safe_div(num, den, ratio_name):
        if num is None or den is None:
            flags.append(f"Missing data for {ratio_name}")
            return None
        if den == 0:
            flags.append(f"Division by zero in {ratio_name}")
            return None
        return float(num) / float(den)

    # Liquidity
    ratios.current_ratio = safe_div(statement.current_assets, statement.current_liabilities, "current_ratio")
    
    if statement.current_assets is not None and statement.total_assets is not None:
        quick_num = statement.current_assets - (0.1 * statement.total_assets)
        ratios.quick_ratio = safe_div(quick_num, statement.current_liabilities, "quick_ratio")
    else:
        flags.append("Missing data for quick_ratio")
        
    ratios.cash_ratio = safe_div(statement.cash_and_equivalents, statement.current_liabilities, "cash_ratio")

    # Leverage
    ratios.debt_to_equity = safe_div(statement.total_debt, statement.total_equity, "debt_to_equity")
    ratios.debt_to_assets = safe_div(statement.total_debt, statement.total_assets, "debt_to_assets")
    ratios.interest_coverage = safe_div(statement.ebitda, statement.interest_expense, "interest_coverage")

    # Profitability
    ratios.gross_margin = safe_div(statement.gross_profit, statement.revenue, "gross_margin")
    ratios.ebitda_margin = safe_div(statement.ebitda, statement.revenue, "ebitda_margin")
    ratios.net_margin = safe_div(statement.net_income, statement.revenue, "net_margin")
    ratios.return_on_equity = safe_div(statement.net_income, statement.total_equity, "return_on_equity")
    ratios.return_on_assets = safe_div(statement.net_income, statement.total_assets, "return_on_assets")

    # Solvency (Altman Z-Score)
    # Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
    # X1=(current_assets-current_liabilities)/total_assets
    # X2=retained_earnings/total_assets (use net_income as proxy)
    # X3=ebitda/total_assets
    # X4=total_equity/total_liabilities
    # X5=revenue/total_assets
    x1 = None
    if statement.current_assets is not None and statement.current_liabilities is not None:
        x1 = safe_div(statement.current_assets - statement.current_liabilities, statement.total_assets, "altman_z_x1")
        
    x2 = safe_div(statement.net_income, statement.total_assets, "altman_z_x2")
    x3 = safe_div(statement.ebitda, statement.total_assets, "altman_z_x3")
    x4 = safe_div(statement.total_equity, statement.total_liabilities, "altman_z_x4")
    x5 = safe_div(statement.revenue, statement.total_assets, "altman_z_x5")

    if all(x is not None for x in [x1, x2, x3, x4, x5]):
        ratios.altman_z_score = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5
    else:
        flags.append("Missing data for altman_z_score")

    ratios.flags = list(set(flags))
    return ratios
