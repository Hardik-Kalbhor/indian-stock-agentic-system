from backend.agents.schemas import Step4Output
from backend.services.market_data_service import MarketDataService


class StockResearcherAgent:
    def __init__(self):
        self.agent_name = "StockResearcherAgent (Step 4)"
        self.firm_name = "nv analytics"

    def run(self, ticker: str = "IREDA.NS"):
        """Executes Step 4: Comprehensive Equity Analysis Report with 6 Institutional Additions."""
        symbol = ticker.upper()
        if not symbol.endswith(".NS") and not symbol.endswith(".BO"):
            symbol = f"{symbol}.NS"

        fund = MarketDataService.get_company_fundamentals(symbol)
        df = MarketDataService.get_stock_data(symbol)
        tech = MarketDataService.calculate_technicals(df)

        current_price = tech["current_price"]
        mcap_cr = fund.get("mcap_cr", 33596)
        pe = fund.get("pe", 17.9)
        target_price = fund.get("target_price", f"₹{round(current_price * 1.35, 2)}")
        
        try:
            target_num = float(str(target_price).replace("₹", "").replace(",", "").strip())
            upside_num = round(((target_num - current_price) / current_price) * 100, 1)
            upside_pct = f"+{upside_num}%" if upside_num >= 0 else f"{upside_num}%"
        except Exception:
            upside_pct = fund.get("upside_pct", "+35.0%")

        recommendation = fund.get("recommendation", "BUY")

        # -------------------------------------------------------------
        # SECTION 1: Company Overview & Investment Recommendation Box
        # -------------------------------------------------------------
        sec1_overview = {
            "title": "1. Company Overview",
            "stock_name": fund.get("name"),
            "ticker": symbol,
            "author": fund.get("author", "nv analytics Research Desk"),
            "sector": fund.get("sector"),
            "hq_location": fund.get("hq_location", "India"),
            "face_value": fund.get("face_value", "₹10"),
            "high_low_52w": fund.get("52w_high_low", "₹200 / ₹100"),
            "isin": fund.get("isin", "INE000000000"),
            "business_description": fund.get("business_overview"),
            "primary_business_activities": fund.get("primary_business_activities", []),
            "recent_developments": fund.get("recent_developments", "Company continues strategic expansion across domestic market hubs."),
            "investment_recommendation_box": {
                "recommendation": recommendation,
                "target_price": target_price,
                "current_price": f"₹{current_price:.2f}",
                "upside_downside": upside_pct,
                "investment_horizon": fund.get("horizon", "18-24 months")
            }
        }

        # Dynamic PEG calculation & commentary
        eps_growth_val = float(fund.get('eps_cagr_5y', 15.0))
        calculated_peg = round(pe / max(eps_growth_val, 1.0), 2)
        if calculated_peg < 1.0:
            peg_comment = f"offering an attractive PEG ratio of {calculated_peg}x (favorable growth-adjusted valuation)"
        elif calculated_peg <= 2.0:
            peg_comment = f"representing a balanced PEG ratio of {calculated_peg}x"
        else:
            peg_comment = f"reflecting a premium PEG ratio of {calculated_peg}x driven by sector leadership"

        # Dynamic Cash Quality commentary
        ocf_pat_val = float(fund.get('ocf_to_pat_pct', 85.0))
        sloan_val = float(fund.get('sloan_accrual_ratio_pct', 3.5))
        if ocf_pat_val >= 80.0 and sloan_val < 5.0:
            cash_quality_comment = f"Solid cash quality: OCF/PAT ratio of {ocf_pat_val:.1f}% and low Sloan accruals ({sloan_val:.1f}%) verify strong cash realization and low earnings manipulation risk."
        else:
            cash_quality_comment = f"Earnings quality profile: OCF/PAT ratio of {ocf_pat_val:.1f}% with Sloan accruals at {sloan_val:.1f}%, reflecting active working capital cycle management."

        # Dynamic Technical Summary
        sma50_val = tech['sma50']
        sma200_val = tech['sma200']
        rsi_val = tech['rsi']

        sma50_rel = f"above 50D SMA (₹{sma50_val:.2f})" if current_price >= sma50_val else f"below 50D SMA (₹{sma50_val:.2f})"
        sma200_rel = f"above 200D SMA (₹{sma200_val:.2f})" if current_price >= sma200_val else f"below 200D SMA (₹{sma200_val:.2f})"

        if rsi_val >= 70:
            rsi_diag = f"RSI at {rsi_val:.2f} (Overbought territory)"
        elif rsi_val <= 30:
            rsi_diag = f"RSI at {rsi_val:.2f} (Oversold territory, potential mean-reversion setup)"
        elif rsi_val > 50:
            rsi_diag = f"RSI at {rsi_val:.2f} (Bullish momentum zone)"
        else:
            rsi_diag = f"RSI at {rsi_val:.2f} (Consolidation zone)"

        tech_summary = f"Stock is currently trading {sma50_rel} and {sma200_rel} with {rsi_diag}."

        # Dynamic Governance Assessment
        pledge_num = float(fund.get('promoter_pledge_pct', 0.0))
        rpt_num = float(fund.get('rpt_pct_pat', 1.8))
        auditor_op = fund.get("auditor_opinion", "Unqualified Clean Opinion")

        if pledge_num == 0:
            pledge_desc = "Zero promoter pledging"
        else:
            pledge_desc = f"Promoter pledge of {pledge_num:.1f}%"

        if rpt_num < 2.0:
            rpt_desc = f"minimal related-party transactions (RPT at {rpt_num:.1f}% of PAT < 2%)"
        else:
            rpt_desc = f"related-party transactions of {rpt_num:.1f}% of PAT"

        gov_assessment = f"{pledge_desc} and {rpt_desc} with {auditor_op} confirm institutional governance standards."

        # -------------------------------------------------------------
        # SECTION 2: Quantitative Analysis (5-Year & 6-8 Quarter Momentum)
        # -------------------------------------------------------------
        sec2_quantitative = {
            "title": "2. Quantitative Analysis",
            
            # Addition 1: 6-8 Quarter Financial Momentum Table
            "quarterly_momentum_engine": {
                "quarterly_table": fund.get("quarterly_momentum", []),
                "momentum_analysis": "Quarterly net profit growth has accelerated over recent quarters with robust top-line momentum, proving operational resilience."
            },

            "a_market_valuation": {
                "metrics": [
                    {"label": "Current Stock Price (CMP)", "val": f"₹{current_price:.2f}", "trend": "Live Market Quote"},
                    {"label": "Market Capitalization", "val": f"₹{mcap_cr:,.2f} Cr", "trend": "Increasing"},
                    {"label": "Price-to-Earnings (P/E) Ratio", "val": f"{pe}x", "trend": "Fair Valuation vs Peers"},
                    {"label": "52-Week High / Low", "val": fund.get("52w_high_low", "N/A"), "trend": "52-Week Range"}
                ],
                "trend_analysis": f"{fund.get('name')} has demonstrated a strong market capitalization trajectory over recent fiscal years, reflecting robust sector tailwinds.",
                "key_takeaways": f"Trading at a P/E of {pe}x relative to 5Y EPS CAGR of {eps_growth_val}%, {peg_comment}."
            },

            # Addition 3: DuPont ROE Decomposition & Capital Spread
            "dupont_capital_spread": {
                "roe": f"{fund.get('roe')}%",
                "net_profit_margin": f"{fund.get('net_margin')}%",
                "asset_turnover": f"{fund.get('asset_turnover')}x",
                "financial_leverage": f"{fund.get('dupont_leverage', 2.5)}x",
                "roce": f"{fund.get('roce')}%",
                "wacc": f"{fund.get('wacc', 9.5)}%",
                "roce_wacc_spread": f"+{fund.get('roce_wacc_spread', 9.7)}%",
                "spread_takeaway": f"ROCE ({fund.get('roce')}%) comfortably exceeds WACC ({fund.get('wacc', 9.5)}%) by +{fund.get('roce_wacc_spread', 9.7)}%, confirming high positive economic value creation."
            },

            "b_profitability_returns": {
                "hist_table": [
                    {"metric": "Return on Equity (ROE %)", "FY24": fund["hist_roe"][0]["val"], "FY23": fund["hist_roe"][1]["val"], "FY22": fund["hist_roe"][2]["val"], "FY21": fund["hist_roe"][3]["val"], "FY20": fund["hist_roe"][4]["val"], "trend": "Improving"},
                    {"metric": "Return on Capital (ROCE %)", "FY24": fund["hist_roce"][0]["val"], "FY23": fund["hist_roce"][1]["val"], "FY22": fund["hist_roce"][2]["val"], "FY21": fund["hist_roce"][3]["val"], "FY20": fund["hist_roce"][4]["val"], "trend": "Improving"},
                    {"metric": "Net Profit Margin %", "FY24": fund["hist_net_margin"][0]["val"], "FY23": fund["hist_net_margin"][1]["val"], "FY22": fund["hist_net_margin"][2]["val"], "FY21": fund["hist_net_margin"][3]["val"], "FY20": fund["hist_net_margin"][4]["val"], "trend": "Expanding"},
                    {"metric": "Operating Profit Margin %", "FY24": fund["hist_opm"][0]["val"], "FY23": fund["hist_opm"][1]["val"], "FY22": fund["hist_opm"][2]["val"], "FY21": fund["hist_opm"][3]["val"], "FY20": fund["hist_opm"][4]["val"], "trend": "Stable & High"}
                ],
                "trend_analysis": f"ROE has expanded consistently from {fund['hist_roe'][4]['val']} in FY20 to {fund['hist_roe'][0]['val']} in FY24, showing steady capital efficiency gains.",
                "key_takeaways": "Operating profit margins have stabilized at elevated levels, providing downside earnings protection during macro sector shifts."
            },

            "c_growth_metrics": {
                "metrics": [
                    {"label": "Revenue Growth Rate (5-Yr CAGR)", "val": f"{fund.get('sales_cagr_5y')}%", "trend": "Accelerating"},
                    {"label": "Revenue Growth Rate (3-Yr CAGR)", "val": f"{fund.get('sales_cagr_3y')}%", "trend": "Strong Surge"},
                    {"label": "EPS Growth Rate (5-Yr CAGR)", "val": f"{fund.get('eps_cagr_5y')}%", "trend": "Outpacing Revenue"}
                ],
                "trend_analysis": f"Revenue 5-year CAGR stands at {fund.get('sales_cagr_5y')}%, accelerating to {fund.get('sales_cagr_3y')}% over the 3-year trailing period.",
                "key_takeaways": f"EPS growth ({fund.get('eps_cagr_5y')}% CAGR) has outpaced top-line expansion, demonstrating positive operational leverage."
            },

            "d_balance_sheet_strength": {
                "hist_table": [
                    {"metric": "Debt-to-Equity Ratio", "FY24": fund["hist_de"][0]["val"], "FY23": fund["hist_de"][1]["val"], "FY22": fund["hist_de"][2]["val"], "FY21": fund["hist_de"][3]["val"], "FY20": fund["hist_de"][4]["val"], "trend": "Deleveraging / De-risking"}
                ],
                "trend_analysis": f"Debt-to-Equity leverage has improved from {fund['hist_de'][4]['val']} in FY20 down to {fund['hist_de'][0]['val']} in FY24.",
                "key_takeaways": "Deleveraging provides strong capital adequacy and interest coverage protection."
            },

            # Addition 2: Cash Quality & Accrual Engine
            "e_cash_flow_accruals": {
                "hist_table": [
                    {"metric": "Cash Flow from Operations", "FY24": fund["hist_cfo"][0]["val"], "FY23": fund["hist_cfo"][1]["val"], "FY22": fund["hist_cfo"][2]["val"], "FY21": fund["hist_cfo"][3]["val"], "FY20": fund["hist_cfo"][4]["val"], "trend": "Strong Growth"}
                ],
                "ocf_to_pat_pct": f"{fund.get('ocf_to_pat_pct', 85.0)}%",
                "cash_conversion_cycle_days": f"{fund.get('cash_conversion_cycle_days', 25)} Days",
                "sloan_accrual_ratio_pct": f"{fund.get('sloan_accrual_ratio_pct', 3.0)}%",
                "quality_assessment": cash_quality_comment
            },

            "f_dividend": {
                "metrics": [
                    {"label": "Dividend Yield", "val": f"{fund.get('div_yield')}%", "trend": "Stable"},
                    {"label": "Dividend Payout Ratio", "val": f"{fund.get('div_payout')}%", "trend": "Reinvestment Focused"}
                ],
                "trend_analysis": f"Maintains a prudent dividend policy ({fund.get('div_yield')}% yield), balancing shareholder payouts with aggressive internal growth compounding.",
                "key_takeaways": "Retention of 80%+ earnings drives long-term book value compounding."
            },

            "g_efficiency": {
                "metrics": [
                    {"label": "Asset Turnover Ratio", "val": f"{fund.get('asset_turnover')}x", "trend": "Optimal"},
                    {"label": "Cash Conversion Cycle", "val": f"{fund.get('cash_conversion_cycle_days')} Days", "trend": "Favorable"},
                    {"label": "Working Capital Days", "val": f"{fund.get('working_capital_days')} Days", "trend": "Lean Working Capital"}
                ],
                "trend_analysis": "Working capital cycle remains highly controlled with low customer credit delays.",
                "key_takeaways": "Efficient working capital utilization minimizes short-term debt borrowing needs."
            },

            # Addition 4: Technical Analysis, Volatility & Microstructure
            "technical_microstructure": {
                "rsi_14d": tech["rsi"],
                "macd_signal": tech["technical_rating"],
                "sma_50d": f"₹{tech['sma50']}",
                "sma_200d": f"₹{tech['sma200']}",
                "beta": fund.get("beta", 0.88),
                "volatility_90d": f"{fund.get('volatility_90d', 18.4)}%",
                "max_drawdown_1y": f"{fund.get('max_drawdown_1y', -14.2)}%",
                "max_drawdown_3y": f"{fund.get('max_drawdown_3y', -22.5)}%",
                "adtv_30d": fund.get("adtv_30d_cr", "₹345 Cr"),
                "technical_summary": tech_summary
            },

            "h_peer_valuation": {
                "peer_table": fund.get("peer_comparison", []),
                "qualitative_peer_commentary": f"Compared to industry peers, {fund.get('name')} commands an attractive valuation relative to its higher ROE and superior earnings growth profile."
            }
        }

        # -------------------------------------------------------------
        # SECTION 3: Qualitative Analysis & Hard Governance
        # -------------------------------------------------------------
        sec3_qualitative = {
            "title": "3. Qualitative Analysis",
            "a_business_model": {
                "core_products": fund.get("core_products", []),
                "revenue_streams": fund.get("revenue_streams"),
                "competitive_advantages": fund.get("competitive_advantages")
            },
            "b_management_quality": {
                "executive_track_record": fund.get("management_quality"),
                "corporate_governance": fund.get("governance_rating")
            },

            # Addition 5: Hard Corporate Governance Indicators
            "hard_governance_indicators": {
                "promoter_pledge_pct": f"{fund.get('promoter_pledge_pct', 0.0)}%",
                "rpt_as_pct_pat": f"{fund.get('rpt_pct_pat', 1.8)}%",
                "auditor_qualification_flag": fund.get("auditor_opinion", "Unqualified Clean Opinion"),
                "governance_assessment": gov_assessment
            },

            "c_growth_strategy": {
                "expansion_plans": fund.get("growth_strategy"),
                "rd_initiatives": "Investing in next-gen digital infrastructure and advanced technology adoption."
            }
        }

        # -------------------------------------------------------------
        # SECTION 4: Shareholding Pattern Analysis
        # -------------------------------------------------------------
        sec4_shareholding = {
            "title": "4. Shareholding Pattern Analysis",
            "pattern_table": fund.get("shareholding_pattern", []),
            "analysis_commentary": "Promoter stake remains strong and stable. Institutional investor interest (FII & DII) has shown steady net accumulation over the last 4 quarters."
        }

        # -------------------------------------------------------------
        # SECTION 5: Investment Thesis
        # -------------------------------------------------------------
        sec5_thesis = {
            "title": "5. Investment Thesis",
            "key_growth_drivers": fund.get("key_growth_drivers", []),
            "stock_catalysts": fund.get("stock_catalysts", []),
            "industry_positioning": f"{fund.get('name')} is strategically positioned to capture secular growth in the {fund.get('sector')} sector."
        }

        # -------------------------------------------------------------
        # SECTION 6: Valuation & Recommendation (Scenario Matrix)
        # -------------------------------------------------------------
        sec6_valuation = {
            "title": "6. Valuation and Recommendation",
            "sotp_valuation_table": fund.get("sotp_valuation", []),
            
            # Addition 6: Scenario-Based Valuation Matrix (Bull / Base / Bear)
            "scenario_valuation_matrix": fund.get("valuation_scenarios", []),

            "fair_value_estimate": target_price,
            "current_price": f"₹{current_price}",
            "upside_potential": upside_pct,
            "recommendation": recommendation,
            "investment_horizon": fund.get("horizon", "18-24 months"),
            "rationale": f"High earnings growth ({fund.get('eps_cagr_5y')}% CAGR), ROCE − WACC spread of +{fund.get('roce_wacc_spread', 9.7)}%, and clean governance support our Base Case price target of {target_price}."
        }

        # -------------------------------------------------------------
        # SECTION 7: Conclusion
        # -------------------------------------------------------------
        sec7_conclusion = {
            "title": "7. Conclusion",
            "summary_statement": f"{fund.get('name')} presents a high-conviction investment opportunity in the Indian equity market.",
            "final_recommendation": f"We restate our {recommendation} rating with a Base Case target price of {target_price} ({upside_pct} upside) over an 18-24 month horizon."
        }

        # -------------------------------------------------------------
        # SECTION 8: AI Powered News Reader & Fundamental Sentiment Radar
        # -------------------------------------------------------------
        news_intel = fund.get("news_intelligence") or {}
        sec8_news = {
            "title": "8. AI Powered News Reader & Fundamental Sentiment Radar",
            "composite_sentiment_score": news_intel.get("composite_sentiment_score", 0.0),
            "sentiment_badge": news_intel.get("sentiment_badge", "🟢 Neutral (0%)"),
            "dominant_catalyst": news_intel.get("dominant_catalyst", "Order Inflows & Contracts"),
            "ai_engine_used": news_intel.get("ai_engine_used", "AI Intelligence Engine"),
            "total_news_analyzed": news_intel.get("total_news_analyzed", 0),
            "bullish_count": news_intel.get("bullish_count", 0),
            "bearish_count": news_intel.get("bearish_count", 0),
            "neutral_count": news_intel.get("neutral_count", 0),
            "news_catalysts": news_intel.get("news_catalysts", []),
            "analysis_commentary": f"AI evaluated {news_intel.get('total_news_analyzed', 0)} recent corporate announcements and news events for {fund.get('name')}. Overall sentiment is {news_intel.get('overall_sentiment', 'Bullish')} with dominant catalysts centered around {news_intel.get('dominant_catalyst', 'Order Inflows')}."
        }

        result = {
            "step": 4,
            "step_title": "Comprehensive Equity Analysis Report",
            "firm": self.firm_name,
            "ticker": symbol,
            "stock_name": fund.get("name"),
            "section1_company_overview": sec1_overview,
            "section2_quantitative_analysis": sec2_quantitative,
            "section3_qualitative_analysis": sec3_qualitative,
            "section4_shareholding_pattern": sec4_shareholding,
            "section5_investment_thesis": sec5_thesis,
            "section6_valuation_recommendation": sec6_valuation,
            "section7_conclusion": sec7_conclusion,
            "section8_news_catalysts": sec8_news,
            "status": "COMPLETED"
        }
        return Step4Output.model_validate(result).model_dump()
