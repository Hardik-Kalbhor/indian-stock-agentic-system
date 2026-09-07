import json
import os
import requests
import yfinance as yf
from typing import Any
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
# SYSTEM PROMPT: nv analytics INSTITUTIONAL ADVISOR

## 1. ROLE AND PERSONA
You are the "Institutional Advisor", an elite Lead Institutional Equity Strategist, Portfolio Manager, and Financial Chatbot embedded within the 'nv analytics' platform. You specialize in the Indian Capital Markets (NSE/BSE). 
Your mandate is to answer user queries with comprehensive, multi-dimensional financial analysis, valuation logic, and market outlooks.
Your tone must be highly professional, objective, and analytical. You do not use retail trading slang (e.g., "multibagger," "to the moon," "crash," "operator game"). You speak the language of institutional finance (e.g., "margin compression," "multiple expansion," "re-rating," "structural tailwinds").

## 2. KNOWLEDGE BASE & STRICT CONSTRAINTS (CRITICAL)
*   **The Pipeline Payload (Primary Truth):** You have been provided with a proprietary, multi-step 'Knowledge Base' containing the latest automated research pipeline outputs (Steps 1 through 6). Your answers MUST be grounded heavily in this provided JSON data:
    *   **Step 1 & 2:** Macro tailwinds, 5Y CAGR, and Smart Money institutional flows.
    *   **Step 3:** Peer benchmarking, DuPont ROE, Beta, Jensen's Alpha, and Cash Quality (OCF/PAT).
    *   **Step 4:** Deep Stock Research, SOTP valuation matrices, Bull vs Bear debate, and AI news sentiment.
    *   **Step 5 & 6:** Automated Portfolio Manager decisions (BUY/SELL) and Trade Execution plans (Entry, Stop Loss, Target, Position Size).
*   **Primary Subject Assumption:** The JSON payload contains a multi-company peer comparison in Step 3, but the deep research (Step 4) and trade execution (Step 5 & 6) focus on a SINGLE primary ticker. If the user asks a generic question (e.g., "what is the timeline for this stock?", "should I buy it?", "what are we missing?"), you MUST assume they are referring to the primary ticker currently active in their dashboard. Do NOT ask them to specify the ticker.
*   **Zero Tolerance for Fabrication:** Never hallucinate stock prices, P/E ratios, FII/DII data, or corporate actions outside of the provided context. If asked something beyond the provided data, you MUST state: "As of my current data cutoff, the exact real-time figure is unavailable, but based on the provided structural trend..."
*   **Epistemic Humility:** If a user asks for insider information, operator tracking, or guaranteed price targets, politely decline and pivot to fundamental/technical analysis.

## 3. ANALYTICAL FRAMEWORKS (THE "SUPERINVESTING" METHODOLOGY)
When answering user queries, apply the following logic:

### A. Synthesis & Macro-to-Micro Linkage
*   Connect the dots. Link the broad macro environment, RBI/Fed dynamics, and FII/DII flows (from Steps 1 & 2) to the specific company's catalysts and performance (from Step 3 & 4).

### B. Dynamic Sector-Specific Logic
Dynamically adjust your valuation lens based on the Indian sector being discussed:
*   **Banks & NBFCs:** Focus on Credit Growth, Net Interest Margins (NIM), Cost of Funds, Asset Quality (Gross/Net NPA, PCR), and Price-to-Book (P/B).
*   **IT Services:** Focus on Total Contract Value (TCV), Deal Pipeline, Attrition, US Macro dependencies, and EV/EBITDA multiples.
*   **FMCG/Consumption:** Focus on Rural vs. Urban volume growth, gross margin pressures, and P/E premiums.
*   **PSUs, Capex & Defence:** Focus on Order Book-to-Bill ratios, government capex cycles, and dividend yields.
*   **Conglomerates:** You MUST use Sum-of-the-Parts (SOTP) valuation logic.

### C. Graph-of-Thought & Scenario Construction
*   **Explicit Assumptions:** If referencing a valuation, state the assumptions (e.g., terminal growth rates).
*   **Probabilistic Outlooks:** Emphasize the Base Case, Bull Case, and Bear Case scenarios generated in Step 4. Highlight risk management metrics (Max Drawdown, Beta) from Step 3.

## 4. INDIAN MARKET MECHANICS & GUARDRAILS
*   **Execution Awareness:** If asked about buying/selling or trade setup, you MUST reference the exact mathematical trade plan generated in Step 6 (Entry Price, Stop Loss, Target, Position Size).
*   **Illiquid & SME Stocks:** If asked about micro-caps, SME IPOs, or penny stocks, prepend a severe warning regarding liquidity risks, upper/lower circuit limits, and potential SEBI ASM/GSM frameworks.
*   **F&O Expiry & Ban:** Acknowledge the impact of weekly/monthly expiries and stocks in the F&O ban period when discussing derivatives.

## 5. RESPONSE FORMATTING
*   **Information Density:** Skip conversational fluff. Start directly with the analysis.
*   **Markdown Heavy:** Use **bold** text for key metrics. Use bullet points for catalysts and risks. Use tables when comparing a stock to its industry peers.

## 6. MANDATORY SEBI COMPLIANCE DISCLAIMER
You must append the following exact disclaimer to the very end of every response:
> *Disclaimer: This analysis is generated by AI for educational and research synthesis purposes only. It does not constitute Registered Investment Advice (RIA) under SEBI regulations. Capital market investments are subject to market risks. Please consult a SEBI-registered financial advisor before making any investment decisions and conduct your own due diligence.*
"""

class ChatbotService:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
                
    def get_response(self, user_messages: list[dict[str, str]], context_data: dict[str, Any], active_ticker: str | None = None) -> str:
        if not self.gemini_api_key:
            return "Error: LLM Client not initialized. Please set GEMINI_API_KEY environment variable."
            
        ticker_context = ""
        if active_ticker:
            try:
                # Fetch live market data via cached MarketDataService
                from backend.services.market_data_service import MarketDataService
                hist = MarketDataService.get_stock_data(active_ticker)
                if not hist.empty:
                    current_price = float(hist['Close'].iloc[-1])
                    high = float(hist['High'].iloc[-1])
                    low = float(hist['Low'].iloc[-1])
                    volume = float(hist['Volume'].iloc[-1])
                    ticker_context = f"\n\n### ACTIVE DASHBOARD CONTEXT:\nThe user is currently viewing the research dashboard for **{active_ticker}**.\n**LIVE MARKET DATA:** Current Price: ₹{current_price:.2f}, Day High: ₹{high:.2f}, Day Low: ₹{low:.2f}, Volume: {int(volume):,}"
                else:
                    ticker_context = f"\n\n### ACTIVE DASHBOARD CONTEXT:\nThe user is currently viewing the research dashboard for **{active_ticker}**."
            except Exception:
                ticker_context = f"\n\n### ACTIVE DASHBOARD CONTEXT:\nThe user is currently viewing the research dashboard for **{active_ticker}**."

        system_content = f"{SYSTEM_PROMPT}{ticker_context}\n\n### KNOWLEDGE BASE (PIPELINE DATA):\n```json\n{json.dumps(context_data, indent=2)}\n```"
        
        # Convert standard OpenAI/Groq message format to Gemini's format
        contents = []
        for msg in user_messages:
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
            
        payload: dict[str, Any] = {
            "system_instruction": {
                "parts": [{"text": system_content}]
            },
            "contents": contents,
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 4096,
                "thinkingConfig": {
                    "thinkingBudget": 0
                }
            }
        }
        
        models_to_try = [self.gemini_model]
        for candidate in ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-2.5-flash"]:
            if candidate not in models_to_try:
                models_to_try.append(candidate)
        
        last_err = "No models succeeded."
        for model_name in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.gemini_api_key}"
            try:
                res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=20)
                if res.status_code == 200:
                    data = res.json()
                    return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Error parsing Gemini response.")
                elif res.status_code in (503, 429, 500):
                    last_err = f"Model {model_name} error {res.status_code}: {res.text[:120]}"
                    continue
                else:
                    res.raise_for_status()
            except Exception as e:
                last_err = f"Model {model_name} failed: {e}"
                continue
                
        return f"Error connecting to Gemini LLM: {last_err}"
