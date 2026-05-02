from pydantic import BaseModel, Field
from typing import Optional, Literal

class FinancialStatement(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    period: str = Field(..., description="Financial period, e.g., 'FY2023' or 'Q1 2024'")
    currency: str = Field(..., description="Currency used in the statement, e.g., 'USD'")
    
    # Income Statement
    revenue: Optional[float] = Field(None, description="Total revenue or sales")
    gross_profit: Optional[float] = Field(None, description="Gross profit")
    ebitda: Optional[float] = Field(None, description="Earnings before interest, taxes, depreciation, and amortization")
    net_income: Optional[float] = Field(None, description="Net income or loss")
    interest_expense: Optional[float] = Field(None, description="Interest expense")
    
    # Balance Sheet
    total_assets: Optional[float] = Field(None, description="Total assets")
    total_liabilities: Optional[float] = Field(None, description="Total liabilities")
    total_equity: Optional[float] = Field(None, description="Total equity")
    current_assets: Optional[float] = Field(None, description="Current assets")
    current_liabilities: Optional[float] = Field(None, description="Current liabilities")
    cash_and_equivalents: Optional[float] = Field(None, description="Cash and cash equivalents")
    total_debt: Optional[float] = Field(None, description="Total debt (short-term + long-term)")
    
    # Cash Flow
    operating_cash_flow: Optional[float] = Field(None, description="Cash flow from operating activities")
    capital_expenditure: Optional[float] = Field(None, description="Capital expenditure (CapEx)")

class ComputedRatios(BaseModel):
    # Liquidity
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    cash_ratio: Optional[float] = None
    
    # Leverage
    debt_to_equity: Optional[float] = None
    debt_to_assets: Optional[float] = None
    interest_coverage: Optional[float] = None
    
    # Profitability
    gross_margin: Optional[float] = None
    ebitda_margin: Optional[float] = None
    net_margin: Optional[float] = None
    return_on_equity: Optional[float] = None
    return_on_assets: Optional[float] = None
    
    # Solvency
    altman_z_score: Optional[float] = None
    
    # Flags for missing data or 0 division
    flags: list[str] = Field(default_factory=list)

class DocumentChunk(BaseModel):
    content: str | bytes
    source: str
    chunk_type: Literal["text", "image", "table"]
    page_num: int
