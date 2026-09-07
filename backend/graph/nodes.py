from datetime import datetime

from backend.agents.memory import TradingMemoryLog
from backend.agents.step1_industry_identifier import IndustryIdentifierAgent
from backend.agents.step2_industry_shortlist import IndustryShortlistAgent
from backend.agents.step3_company_comparator import CompanyComparatorAgent
from backend.agents.step4_stock_researcher import StockResearcherAgent
from backend.agents.step5_portfolio_manager import PortfolioManagerAgent
from backend.agents.step6_execution_trader import ExecutionTraderAgent
from backend.graph.state import PipelineGraphState


def run_step1(state: PipelineGraphState) -> PipelineGraphState:
    agent = IndustryIdentifierAgent()
    result = agent.run()
    
    selected_sector = state.get("user_sector_name")
    if not selected_sector:
        # Default to the winner from Step 1 if user didn't provide one
        winning_theme = result.get("winning_theme", {})
        selected_sector = winning_theme.get("name", "Renewable Energy & Green Power")
        
    return {"step1_result": result, "selected_sector": selected_sector}

def run_step2(state: PipelineGraphState) -> PipelineGraphState:
    agent = IndustryShortlistAgent()
    sector = state.get("selected_sector") or "Renewable Energy & Green Power"
    
    result = agent.run(sector_name=sector)
    
    shortlisted = state.get("user_compare_tickers")
    if not shortlisted:
        # Extract top 3 tickers from the shortlisted theme details
        theme_details = result.get("theme_details", {})
        selected_set = theme_details.get("selected_set", [])
        if selected_set:
            raw_tickers = [s["ticker"] for s in selected_set if s.get("ticker")]
            shortlisted = [t if (t.endswith(".NS") or t.endswith(".BO")) else f"{t}.NS" for t in raw_tickers[:3]]
        else:
            top_20 = theme_details.get("universe_top20", [])
            shortlisted = [t if (t.endswith(".NS") or t.endswith(".BO")) else f"{t}.NS" for t in top_20[:3]] if top_20 else []
        
    return {"step2_result": result, "shortlisted_tickers": shortlisted}

def run_step3(state: PipelineGraphState) -> PipelineGraphState:
    agent = CompanyComparatorAgent()
    sector = state.get("selected_sector") or "Renewable Energy & Green Power"
    tickers = state.get("shortlisted_tickers") or []
    
    result = agent.run(tickers=tickers, sector_name=sector)
    
    winner = state.get("user_target_ticker")
    if not winner:
        # Extract the winner from step 3 result
        winner_data = result.get("winner", {})
        winner = winner_data.get("ticker", "IREDA.NS")
        
    return {"step3_result": result, "winning_ticker": winner}

def run_step4(state: PipelineGraphState) -> PipelineGraphState:
    agent = StockResearcherAgent()
    ticker = state.get("winning_ticker") or "IREDA.NS"
    
    result = agent.run(ticker=ticker)
    
    return {"step4_result": result}



def run_step5(state: PipelineGraphState) -> PipelineGraphState:
    agent = PortfolioManagerAgent()
    ticker = state.get("winning_ticker") or "IREDA.NS"
    step4_research = state.get("step4_result") or {}
    
    memory_log = TradingMemoryLog({'memory_log_path': 'backend/data/trading_memory.log'})
    past_lessons = memory_log.get_past_context(ticker)
    result = agent.run(ticker=ticker, step4_research=step4_research, past_lessons=past_lessons)
    
    return {"step5_result": result}

def run_step6(state: PipelineGraphState) -> PipelineGraphState:
    agent = ExecutionTraderAgent()
    
    step5_result = state.get("step5_result") or {}
    decision = step5_result.get("decision", {
        "ticker": state.get("winning_ticker", "IREDA.NS"),
        "action": "HOLD",
        "confidence_score": 50,
        "reasoning": "Fallback decision."
    })
    
    result = agent.run(decision=decision)
    
    memory_log = TradingMemoryLog({"memory_log_path": "backend/data/trading_memory.log"})
    today = datetime.today().strftime("%Y-%m-%d")
    # Store the decision in the memory log
    memory_log.store_decision(
        ticker=decision.get("ticker", "IREDA.NS"),
        trade_date=today,
        rating=decision.get("action", "HOLD"),
        final_trade_decision=str(result["execution_plan"])
    )

    
    return {"step6_result": result}
