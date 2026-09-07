from typing import Any, Literal
from pydantic import BaseModel, Field, ConfigDict


# =====================================================================
# STEP 1: Industry Identification & Growth Sector Research Schemas
# =====================================================================

class MacroIndicators(BaseModel):
    model_config = ConfigDict(extra="allow")
    execution_date: str = Field(..., description="Date of macro snapshot execution")
    gdp_growth_fy26: str = Field(..., description="Projected real GDP growth")
    cpi_inflation: str = Field(..., description="Consumer price index inflation rate")
    repo_rate: str = Field(..., description="RBI policy repo rate")
    bank_credit_growth: str = Field(..., description="YoY systemic credit expansion")
    effective_capex_cr: str = Field(..., description="Union budget effective capital outlay")
    nifty_pe: str = Field(..., description="Benchmark Nifty 50 trailing price-to-earnings")
    valuation_status: str = Field(..., description="Valuation stance vs historical median")
    gsec_10y_yield: str = Field(..., description="Benchmark 10-Year Indian Sovereign Yield")
    earnings_yield_spread: str = Field(..., description="Spread between earnings yield and bond yield")
    usd_inr: str = Field(..., description="Spot exchange rate USD to INR")
    fiscal_deficit: str = Field(..., description="Target fiscal deficit as percentage of GDP")
    institutional_flows: str = Field(..., description="Institutional net monthly accumulation floor")


class SectorScoringBreakdown(BaseModel):
    model_config = ConfigDict(extra="allow")
    macro: float = Field(..., ge=0, le=5)
    policy: float = Field(..., ge=0, le=5)
    cagr: float = Field(..., ge=0, le=5)
    valuation: float = Field(..., ge=0, le=5)
    earnings: float = Field(..., ge=0, le=5)
    momentum: float = Field(..., ge=0, le=5)
    smart_money: float = Field(..., ge=0, le=5)


class TopSector(BaseModel):
    model_config = ConfigDict(extra="allow")
    rank: int = Field(..., ge=1, le=50)
    sector: str = Field(..., description="Sector or thematic name")
    classification: str = Field(..., description="Structural Growth / Capital Cycle / Secular Compounder")
    score: float = Field(..., description="Composite 5-point institutional conviction score")
    scoring_breakdown: SectorScoringBreakdown
    cagr_5y: str = Field(..., description="5-Year compound annual growth rate")
    market_size_cr: str = Field(..., description="Addressable market size in INR Crore")
    pe_range: str = Field(..., description="Historical and current P/E range")
    key_drivers: list[str] = Field(default_factory=list, description="Primary structural catalysts")
    conviction: float | int = Field(..., description="Conviction rating out of 5")
    anchor_stocks: list[str] = Field(default_factory=list, description="Leading anchor constituents")


class ArchivedReport(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    title: str
    date: str
    sectors_count: int
    top_sector: str
    url: str
    badge: str
    badge_color: str
    summary: str


class Step1Output(BaseModel):
    model_config = ConfigDict(extra="allow")
    step: int = Field(1, description="Step number")
    step_title: str = Field("Industry Identification & Growth Sector Research")
    firm: str = Field("NV Analytics")
    macro_indicators: MacroIndicators
    sectors_screened_count: int = Field(35, description="Number of sectors evaluated")
    top_selected_sectors: list[TopSector]
    archived_reports: list[ArchivedReport] = Field(default_factory=list)
    status: Literal["COMPLETED", "FAILED"] = "COMPLETED"


# =====================================================================
# STEP 2: Industry Analysis & Stock Shortlist Screener Schemas
# =====================================================================

class FinancialRatios(BaseModel):
    model_config = ConfigDict(extra="allow")
    ebitda_margin: str
    net_margin: str
    current_ratio: str
    quick_ratio: str
    eps: str
    div_yield: str
    fcf_share: str


class SmartMoneySignals(BaseModel):
    model_config = ConfigDict(extra="allow")
    fno_signal: str
    pcr: str
    fii_flow_3m: str
    dii_flow_3m: str


class GovernanceInsiderSignals(BaseModel):
    model_config = ConfigDict(extra="allow")
    promoter_trend: str
    insider_kmp_action: str
    rpt_status: str
    esop_dilution: str


class ValuationSanityCheck(BaseModel):
    model_config = ConfigDict(extra="allow")
    peg_ratio: str
    pe_vs_5y_median: str
    pat_consistency_12q: str
    cfo_to_pat_pct: str
    interest_coverage: str
    hard_filter_status: str


class CapexTimelineItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    project_name: str
    capex_outlay_cr: str
    expected_completion: str
    capacity_addition: str


class RiskMatrixItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    factor: str
    category: str
    impact_level: str
    probability: str
    mitigation_strategy: str


class PillarsScore(BaseModel):
    model_config = ConfigDict(extra="allow")
    fundamentals: int | float
    growth: int | float
    technical: int | float
    sentiment: int | float
    valuation: int | float
    penalties: int | float


class SelectedStock(BaseModel):
    model_config = ConfigDict(extra="allow")
    slot: str
    ticker: str
    name: str
    mcap: str
    price: str
    role: str
    badges: list[str] = Field(default_factory=list)
    diagnostic_score: int | float
    market_share_pct: str
    financial_ratios: FinancialRatios | dict[str, Any]
    smart_money_signals: SmartMoneySignals | dict[str, Any]
    governance_insider_signals: GovernanceInsiderSignals | dict[str, Any]
    valuation_sanity_check: ValuationSanityCheck | dict[str, Any]
    geo_footprint: dict[str, str] = Field(default_factory=dict)
    capex_timeline: list[CapexTimelineItem | dict[str, Any]] = Field(default_factory=list)
    risk_matrix: list[RiskMatrixItem | dict[str, Any]] = Field(default_factory=list)
    pillars: PillarsScore | dict[str, Any]
    audit_trail: str
    mcap_cr: float | None = None
    cap_category: str | None = None
    price_val: float | None = None


class ThemeDetails(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    name: str
    avg_score: int | float
    selected_range: str
    setup: str
    growth_thesis: str
    sentiment_thesis: str
    momentum_thesis: str
    valuation_risk_thesis: str
    data_quality_note: str
    weighting_note: str
    selected_set: list[SelectedStock | dict[str, Any]] = Field(default_factory=list)
    universe_top20: list[str] = Field(default_factory=list)
    near_misses: list[dict[str, str]] = Field(default_factory=list)
    bull_case: str
    bear_case: str
    invalidation_factors: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    cap_filter_applied: str | None = None
    cap_filter_label: str | None = None
    price_filter_min: int | float | None = None
    price_filter_max: int | float | None = None
    price_filter_label: str | None = None


class ThemeSummaryItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str
    avg_score: int | float
    selected_range: str


class Step2Output(BaseModel):
    model_config = ConfigDict(extra="allow")
    step: int = Field(2, description="Step number")
    step_title: str = Field("Industry Analysis & Stock Shortlist (Selected Set Screener)")
    firm: str = Field("nv analytics")
    active_theme: str
    market_cap_filter: str
    price_min: int | float
    price_max: int | float
    theme_summary_list: list[ThemeSummaryItem]
    theme_details: ThemeDetails
    all_themes_data: dict[str, Any]
    status: Literal["COMPLETED", "FAILED"] = "COMPLETED"


# =====================================================================
# STEP 3: Company Comparison Deep Research Engine Schemas
# =====================================================================

class KeyFactorCard(BaseModel):
    model_config = ConfigDict(extra="allow")
    title: str
    desc: str


class WinnerSummary(BaseModel):
    model_config = ConfigDict(extra="allow")
    ticker: str
    name: str
    score_100: float
    score_30: float
    verdict_paragraph: str
    key_factor_cards: list[KeyFactorCard]


class Step3Output(BaseModel):
    model_config = ConfigDict(extra="allow")
    step: int = Field(3, description="Step number")
    step_title: str = Field("Company Comparison Deep Research Engine")
    firm: str = Field("nv analytics")
    sector_name: str
    scoring_framework: dict[str, str]
    companies_compared_count: int
    companies: list[dict[str, Any]]
    winner: WinnerSummary
    shortcomings: dict[str, list[str]] = Field(default_factory=dict)
    status: Literal["COMPLETED", "FAILED"] = "COMPLETED"


# =====================================================================
# STEP 4: Comprehensive Equity Analysis Report Schemas
# =====================================================================

class RecommendationBox(BaseModel):
    model_config = ConfigDict(extra="allow")
    recommendation: str
    target_price: str
    current_price: str
    upside_downside: str
    investment_horizon: str


class Section1Overview(BaseModel):
    model_config = ConfigDict(extra="allow")
    title: str
    stock_name: str | None = None
    ticker: str
    author: str
    sector: str | None = None
    hq_location: str
    face_value: str
    high_low_52w: str
    isin: str
    business_description: str | None = None
    primary_business_activities: list[str] = Field(default_factory=list)
    recent_developments: str | list[str]
    investment_recommendation_box: RecommendationBox


class Step4Output(BaseModel):
    model_config = ConfigDict(extra="allow")
    step: int = Field(4, description="Step number")
    step_title: str = Field("Comprehensive Equity Analysis Report")
    firm: str = Field("nv analytics")
    ticker: str
    stock_name: str | None = None
    section1_company_overview: Section1Overview | dict[str, Any]
    section2_quantitative_analysis: dict[str, Any]
    section3_qualitative_analysis: dict[str, Any]
    section4_shareholding_pattern: dict[str, Any]
    section5_investment_thesis: dict[str, Any]
    section6_valuation_recommendation: dict[str, Any]
    section7_conclusion: dict[str, Any]
    section8_news_catalysts: dict[str, Any]
    status: Literal["COMPLETED", "FAILED"] = "COMPLETED"


# =====================================================================
# STEP 5 & 6: Portfolio Decision & Execution Trader Schemas
# =====================================================================

class PortfolioDecision(BaseModel):
    model_config = ConfigDict(extra="allow")
    ticker: str = Field(..., description="The stock ticker symbol.")
    action: Literal["BUY", "SELL", "HOLD", "OVERWEIGHT", "UNDERWEIGHT"] = Field(..., description="The portfolio action to take.")
    confidence_score: int = Field(..., ge=1, le=100, description="Confidence in this decision from 1 to 100.")
    reasoning: str = Field(..., description="Brief explanation for the portfolio decision based on fundamental and technical research.")


class Step5Output(BaseModel):
    model_config = ConfigDict(extra="allow")
    step: int = Field(5, description="Step number")
    step_title: str = Field("Portfolio Manager Decision")
    firm: str = Field("nv analytics")
    decision: PortfolioDecision
    status: Literal["COMPLETED", "FAILED"] = "COMPLETED"


class TradeExecutionPlan(BaseModel):
    model_config = ConfigDict(extra="allow")
    ticker: str = Field(..., description="The stock ticker symbol.")
    action: Literal["BUY", "SELL", "HOLD", "OVERWEIGHT", "UNDERWEIGHT"] = Field(..., description="The executed action.")
    entry_price: float | None = Field(None, description="The exact or limit price to enter the trade.")
    stop_loss: float | None = Field(None, description="The stop loss price for risk management.")
    target_price: float | None = Field(None, description="The price target to exit or take profit.")
    position_size_pct: float | None = Field(None, description="Suggested allocation size as a percentage of total portfolio (e.g. 5.0 for 5%).")


class Step6Output(BaseModel):
    model_config = ConfigDict(extra="allow")
    step: int = Field(6, description="Step number")
    step_title: str = Field("Execution Trader Plan")
    firm: str = Field("nv analytics")
    execution_plan: TradeExecutionPlan
    status: Literal["COMPLETED", "FAILED"] = "COMPLETED"


# =====================================================================
# ROOT: Full Pipeline Response Schema
# =====================================================================

class FullPipelineResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    system: str = Field("nv analytics Multi-Agent LangGraph Pipeline")
    pipeline_status: str = Field("COMPLETED")
    step1: Step1Output | None = None
    step2: Step2Output | None = None
    step3: Step3Output | None = None
    step4: Step4Output | None = None
    step5: Step5Output | None = None
    step6: Step6Output | None = None
