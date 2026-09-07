from typing import Any

from backend.agents.schemas import PortfolioDecision, Step6Output, TradeExecutionPlan
from backend.services.market_data_service import MarketDataService


class ExecutionTraderAgent:
    def __init__(self):
        self.agent_name = "ExecutionTraderAgent (Step 6)"
        self.firm_name = "nv analytics"

    def run(self, decision: dict[str, Any]) -> dict[str, Any]:
        """
        Executes Step 6: Trade Execution Plan.
        Translates the Portfolio Manager's directional call into strict trade mechanics 
        (Entry, Stop Loss, Target, Sizing) using actual market prices.
        """
        decision_obj = PortfolioDecision(**decision)
        ticker = decision_obj.ticker
        
        # Fetch live price & institutional technicals via MarketDataService
        price_data = MarketDataService.get_stock_data(ticker)
        technicals = MarketDataService.calculate_technicals(price_data)
        
        current_price = technicals.get("current_price", 100.0)
        atr = technicals.get("atr", 5.0)
        support = technicals.get("support", current_price * 0.95)
        resistance = technicals.get("resistance", current_price * 1.08)
            
        entry_price = current_price
        stop_loss = None
        target_price = None
        position_size = 0.0
        
        if decision_obj.action in ["BUY", "OVERWEIGHT"]:
            # Buy at market or slight pullback
            entry_price = round(current_price * 0.99, 2) 
            # Stop loss 1.5 ATR below entry, or anchored below support
            raw_stop = entry_price - (1.5 * atr)
            stop_loss = round(min(raw_stop, support - (0.5 * atr)) if support < entry_price else raw_stop, 2)
            # Target 3 ATR above entry, anchored above resistance
            raw_target = entry_price + (3.0 * atr)
            target_price = round(max(raw_target, resistance) if resistance > entry_price else raw_target, 2)
            
            position_size = 5.0 if decision_obj.action == "BUY" else 2.5
            
        elif decision_obj.action in ["SELL", "UNDERWEIGHT"]:
            # Sell at market or slight bounce
            entry_price = round(current_price * 1.01, 2)
            # Stop loss 1.5 ATR above entry, anchored above resistance
            raw_stop = entry_price + (1.5 * atr)
            stop_loss = round(max(raw_stop, resistance + (0.5 * atr)) if resistance > entry_price else raw_stop, 2)
            # Target 3 ATR below entry, anchored at support
            raw_target = entry_price - (3.0 * atr)
            target_price = round(min(raw_target, support) if support < entry_price else raw_target, 2)
            
            position_size = 0.0 # Exit position
        
        elif decision_obj.action == "HOLD":
            position_size = 2.5 # Maintain existing
            
        plan = TradeExecutionPlan(
            ticker=ticker,
            action=decision_obj.action,
            entry_price=entry_price,
            stop_loss=stop_loss,
            target_price=target_price,
            position_size_pct=position_size
        )
        
        result = {
            "step": 6,
            "step_title": "Trade Execution Plan",
            "firm": self.firm_name,
            "execution_plan": plan.model_dump(),
            "status": "COMPLETED"
        }
        return Step6Output.model_validate(result).model_dump()
