import os
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
import requests
import yfinance as yf

from backend.agents.memory import TradingMemoryLog

load_dotenv()

class ReflectorAgent:
    def __init__(self):
        self.agent_name = "ReflectorAgent"
        self.memory_log = TradingMemoryLog({"memory_log_path": "backend/data/trading_memory.log"})
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        
    def resolve_pending_trades(self, force_resolve_today=False):
        """Finds pending trades, calculates returns, generates reflections, and updates the log."""
        pending = self.memory_log.get_pending_entries()
        if not pending:
            print("No pending trades to reflect upon.")
            return
            
        today = datetime.today()
        updates = []
        
        for entry in pending:
            trade_date_str = entry["date"]
            ticker = entry["ticker"]
            trade_date = datetime.strptime(trade_date_str, "%Y-%m-%d")
            
            # Assume 3 day holding period for reflection
            days_held = (today - trade_date).days
            if days_held < 3 and not force_resolve_today:
                print(f"Skipping {ticker} from {trade_date_str} (holding period < 3 days)")
                continue
                
            # For testing: if days_held is 0 (today), mock it as 3 days.
            if days_held == 0 and force_resolve_today:
                days_held = 3
                
            print(f"Resolving {ticker} trade from {trade_date_str}...")
            
            try:
                # Fetch price from trade_date to today
                hist = yf.download(ticker, start=trade_date_str, progress=False)
                if hist.empty or len(hist) < 2:
                    print(f"Not enough price data for {ticker} yet.")
                    continue
                    
                entry_price = float(hist['Close'].iloc[0].iloc[0] if hasattr(hist['Close'].iloc[0], "iloc") else hist['Close'].iloc[0])
                exit_price = float(hist['Close'].iloc[-1].iloc[0] if hasattr(hist['Close'].iloc[-1], "iloc") else hist['Close'].iloc[-1])
                resolution_date = hist.index[-1].strftime("%Y-%m-%d")
                
                # Fetch NIFTY 50 benchmark
                nifty = yf.download("^NSEI", start=trade_date_str, progress=False)
                if not nifty.empty and len(nifty) >= 2:
                    bench_entry = float(nifty['Close'].iloc[0].iloc[0] if hasattr(nifty['Close'].iloc[0], "iloc") else nifty['Close'].iloc[0])
                    bench_exit = float(nifty['Close'].iloc[-1].iloc[0] if hasattr(nifty['Close'].iloc[-1], "iloc") else nifty['Close'].iloc[-1])
                    bench_return = (bench_exit - bench_entry) / bench_entry
                else:
                    bench_return = 0.0
                
                # If shorting (SELL), return is inverted
                is_short = entry["rating"] in ["SELL", "UNDERWEIGHT"]
                if is_short:
                    raw_return = (entry_price - exit_price) / entry_price
                else:
                    raw_return = (exit_price - entry_price) / entry_price
                    
                alpha_return = raw_return - bench_return
                
                # Generate Reflection via Gemini
                reflection = self._generate_reflection(ticker, trade_date_str, entry["rating"], entry["decision"], raw_return, alpha_return)
                
                updates.append({
                    "ticker": ticker,
                    "trade_date": trade_date_str,
                    "raw_return": raw_return,
                    "alpha_return": alpha_return,
                    "holding_days": days_held,
                    "resolution_date": resolution_date,
                    "reflection": reflection
                })
            except Exception as e:
                print(f"Error resolving {ticker}: {e}")
                
        if updates:
            self.memory_log.batch_update_with_outcomes(updates)
            print(f"Successfully logged reflections for {len(updates)} trades.")

    def _generate_reflection(self, ticker, trade_date, action, decision, raw_return, alpha_return) -> str:
        """Uses Gemini to reflect on the trade outcome."""
        if not self.gemini_api_key:
            return "No LLM key configured. Hardcoded reflection: Trade outcome recorded."
            
        system_prompt = "You are an elite Institutional Portfolio Manager reviewing past trades. Write a short, highly analytical paragraph (3-4 sentences max) reflecting on why this trade succeeded or failed. Mention the raw return, alpha return, and what the firm should learn from this execution for future trades. Speak in institutional financial terms."
        
        outcome_str = "PROFITABLE" if raw_return > 0 else "LOSS-MAKING"
        
        user_prompt = f"Trade details:\nTicker: {ticker}\nDate: {trade_date}\nAction: {action}\nOriginal Execution Plan: {decision}\n\nOutcome: {outcome_str}\nRaw Return: {raw_return:.2%}\nAlpha vs Benchmark: {alpha_return:.2%}\n\nPlease write your reflection."
        
        payload: dict[str, Any] = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
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
                res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
                if res.status_code == 200:
                    data = res.json()
                    return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No reflection generated.")
                elif res.status_code in (503, 429, 500):
                    last_err = f"Model {model_name} error {res.status_code}: {res.text[:100]}"
                    continue
                else:
                    res.raise_for_status()
            except Exception as e:
                last_err = f"Model {model_name} failed: {e}"
                continue
                
        return f"Reflection generation failed: {last_err}"

if __name__ == "__main__":
    agent = ReflectorAgent()
    agent.resolve_pending_trades(force_resolve_today=True)
