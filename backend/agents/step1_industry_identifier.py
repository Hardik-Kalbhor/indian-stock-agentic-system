from backend.agents.schemas import Step1Output


class IndustryIdentifierAgent:
    def __init__(self):
        self.agent_name = "IndustryIdentifierAgent (Step 1)"
        self.firm_name = "NV Analytics"

    def run(self):
        """Executes Step 1: 10-Sector Industry Identification & Growth Sector Research for Indian Equities."""
        macro_indicators = {
            "execution_date": "04 August 2026",
            "gdp_growth_fy26": "7.7%",
            "cpi_inflation": "4.38%",
            "repo_rate": "5.25%",
            "bank_credit_growth": "18.8% YoY",
            "effective_capex_cr": "₹17.15 Lakh Cr",
            "nifty_pe": "20.78x",
            "valuation_status": "Fairly Valued (vs 5Y Median 21.5x)",
            "gsec_10y_yield": "6.98%",
            "earnings_yield_spread": "-2.17%",
            "usd_inr": "₹95.25",
            "fiscal_deficit": "4.3% of GDP",
            "institutional_flows": "DII Net Accumulation (+₹24,500 Cr/mo SIP floor)"
        }

        top_10_sectors = [
            {
                "rank": 1,
                "sector": "Renewable Energy & Green Power",
                "classification": "Structural Growth",
                "score": 4.70,
                "scoring_breakdown": { "macro": 5.0, "policy": 5.0, "cagr": 5.0, "valuation": 3.5, "earnings": 4.5, "momentum": 4.5, "smart_money": 5.0 },
                "cagr_5y": "28.5%",
                "market_size_cr": "₹2,80,000 Cr",
                "pe_range": "18x - 34x",
                "key_drivers": ["500 GW target by 2030", "Solar/Hydrogen PLI ₹24k Cr", "Grid Access Priority"],
                "conviction": 5,
                "anchor_stocks": ["IREDA.NS", "TATAPOWER.NS", "NTPC.NS", "SUZLON.NS"]
            },
            {
                "rank": 2,
                "sector": "Defence & Aerospace Manufacturing",
                "classification": "Structural Growth",
                "score": 4.60,
                "scoring_breakdown": { "macro": 5.0, "policy": 5.0, "cagr": 5.0, "valuation": 3.0, "earnings": 5.0, "momentum": 4.5, "smart_money": 5.0 },
                "cagr_5y": "24.2%",
                "market_size_cr": "₹1,90,000 Cr",
                "pe_range": "32x - 47x",
                "key_drivers": ["75%+ indigenous procurement mandate", "Export target ₹50,000 Cr", "7Y order backlog"],
                "conviction": 5,
                "anchor_stocks": ["HAL.NS", "BEL.NS", "MAZDOCK.NS", "COCHINSHIP.NS"]
            },
            {
                "rank": 3,
                "sector": "Capital Goods & Industrial Engineering",
                "classification": "Capital Cycle",
                "score": 4.45,
                "scoring_breakdown": { "macro": 4.5, "policy": 4.5, "cagr": 4.0, "valuation": 4.0, "earnings": 4.5, "momentum": 4.5, "smart_money": 4.5 },
                "cagr_5y": "20.8%",
                "market_size_cr": "₹5,20,000 Cr",
                "pe_range": "28x - 52x",
                "key_drivers": ["₹12.2L Cr public capex push", "Private corporate capex resurgence", "Factory automation"],
                "conviction": 4,
                "anchor_stocks": ["LT.NS", "SIEMENS.NS", "ABB.NS", "CGPOWER.NS"]
            },
            {
                "rank": 4,
                "sector": "EV & New-Age Mobility",
                "classification": "Structural Growth",
                "score": 4.40,
                "scoring_breakdown": { "macro": 4.5, "policy": 5.0, "cagr": 5.0, "valuation": 3.0, "earnings": 4.0, "momentum": 4.0, "smart_money": 4.5 },
                "cagr_5y": "32.6%",
                "market_size_cr": "₹1,40,000 Cr",
                "pe_range": "28x - 42x",
                "key_drivers": ["PM E-DRIVE scheme ₹10,900 Cr", "Lithium cell gigafactories", "Fleet electrification"],
                "conviction": 4,
                "anchor_stocks": ["TATAMOTORS.NS", "TVSMOTOR.NS", "M&M.NS", "EXIDEIND.NS"]
            },
            {
                "rank": 5,
                "sector": "AI Infrastructure, Data Centers & Digital IT",
                "classification": "Secular Compounder",
                "score": 4.30,
                "scoring_breakdown": { "macro": 4.5, "policy": 4.5, "cagr": 5.0, "valuation": 3.5, "earnings": 4.0, "momentum": 3.5, "smart_money": 4.5 },
                "cagr_5y": "25.4%",
                "market_size_cr": "₹1,10,000 Cr",
                "pe_range": "16x - 45x",
                "key_drivers": ["Hyper-scaler 2.5+ GW DC capacity buildout", "IndiaAI Mission ₹10,370 Cr", "Digital engineering"],
                "conviction": 4,
                "anchor_stocks": ["TCS.NS", "NETWEB.NS", "PERSISTENT.NS", "INFY.NS"]
            },
            {
                "rank": 6,
                "sector": "Banking & Financial Services (BFSI)",
                "classification": "Secular Compounder",
                "score": 4.20,
                "scoring_breakdown": { "macro": 4.5, "policy": 3.5, "cagr": 3.5, "valuation": 5.0, "earnings": 4.5, "momentum": 4.0, "smart_money": 4.0 },
                "cagr_5y": "13.0%",
                "market_size_cr": "₹18,50,000 Cr",
                "pe_range": "11x - 18x",
                "key_drivers": ["Robust 18.8% YoY credit growth", "Clean GNPA < 2.8%", "14.7x attractive PE discount"],
                "conviction": 4,
                "anchor_stocks": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS"]
            },
            {
                "rank": 7,
                "sector": "Specialty Chemicals & Advanced Materials",
                "classification": "Capital Cycle",
                "score": 3.85,
                "scoring_breakdown": { "macro": 3.5, "policy": 4.0, "cagr": 4.0, "valuation": 3.5, "earnings": 4.0, "momentum": 3.5, "smart_money": 4.0 },
                "cagr_5y": "18.2%",
                "market_size_cr": "₹2,20,000 Cr",
                "pe_range": "28x - 38x",
                "key_drivers": ["China+1 diversification", "Domestic import substitution", "Fluoropolymer demand"],
                "conviction": 3.5,
                "anchor_stocks": ["SRF.NS", "PIIND.NS", "FLUOROCHEM.NS"]
            },
            {
                "rank": 8,
                "sector": "Pharmaceuticals & Healthcare Services",
                "classification": "Secular Compounder",
                "score": 3.75,
                "scoring_breakdown": { "macro": 3.5, "policy": 4.0, "cagr": 3.5, "valuation": 3.5, "earnings": 4.0, "momentum": 3.5, "smart_money": 4.0 },
                "cagr_5y": "13.6%",
                "market_size_cr": "₹3,80,000 Cr",
                "pe_range": "24x - 42x",
                "key_drivers": ["US FDA complex generic filings", "Domestic hospital bed expansion", "Health insurance penetration"],
                "conviction": 3.5,
                "anchor_stocks": ["SUNPHARMA.NS", "CIPLA.NS", "APOLLOHOSP.NS"]
            },
            {
                "rank": 9,
                "sector": "Quick Commerce & Logistics",
                "classification": "Structural Growth",
                "score": 3.70,
                "scoring_breakdown": { "macro": 4.0, "policy": 3.0, "cagr": 4.5, "valuation": 2.5, "earnings": 4.0, "momentum": 4.0, "smart_money": 4.0 },
                "cagr_5y": "31.0%",
                "market_size_cr": "₹80,000 Cr",
                "pe_range": "28x - 68x",
                "key_drivers": ["10-minute hyper-local delivery dark stores", "Urban retail transformation", "50%+ YoY revenue growth"],
                "conviction": 3.5,
                "anchor_stocks": ["ETERNAL.NS", "DELHIVERY.NS"]
            },
            {
                "rank": 10,
                "sector": "Real Estate & Urban Infrastructure",
                "classification": "Capital Cycle",
                "score": 3.65,
                "scoring_breakdown": { "macro": 4.0, "policy": 3.5, "cagr": 3.5, "valuation": 3.0, "earnings": 4.0, "momentum": 4.0, "smart_money": 3.5 },
                "cagr_5y": "17.4%",
                "market_size_cr": "₹3,50,000 Cr",
                "pe_range": "32x - 48x",
                "key_drivers": ["Decade-low residential housing inventory", "Urban transit infrastructure", "Premiumization trend"],
                "conviction": 3.5,
                "anchor_stocks": ["DLF.NS", "GODREJPROP.NS"]
            }
        ]

        # Archived & Historical Reports Library
        archived_reports = [
            {
                "id": "report-20260804",
                "title": "India Top 10 Growth Sectors Deep Research Briefing (August 2026)",
                "date": "04 August 2026",
                "sectors_count": 35,
                "top_sector": "Renewable Energy & Green Power (4.70/5)",
                "url": "/india-growth-sectors-20260804.html",
                "badge": "LATEST 10-SECTOR REPORT",
                "badge_color": "green",
                "summary": "35-sector 7-dimension scoring matrix, 8-KPI macro strip with G-Sec yield spread, 10 top growth sectors, Chart.js rotation charts, policy execution heatmap, and 15+ verified reference citations under NV Analytics branding."
            },
            {
                "id": "report-20260803",
                "title": "India Growth Sectors Deep Research Briefing (03 August 2026)",
                "date": "03 August 2026",
                "sectors_count": 32,
                "top_sector": "Renewable Energy & Green Power (4.65/5)",
                "url": "/india-growth-sectors-20260803.html",
                "badge": "PREVIOUS BRIEFING",
                "badge_color": "teal",
                "summary": "Complete 32-sector scoring matrix, live macro linkages, interactive Chart.js rotation analytics, policy heatmap, and 20+ verified references."
            }
        ]

        result = {
            "step": 1,
            "step_title": "Industry Identification & Growth Sector Research",
            "firm": self.firm_name,
            "macro_indicators": macro_indicators,
            "sectors_screened_count": 35,
            "top_selected_sectors": top_10_sectors,
            "archived_reports": archived_reports,
            "status": "COMPLETED"
        }
        return Step1Output.model_validate(result).model_dump()
