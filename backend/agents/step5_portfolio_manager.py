from typing import Any, Literal

from backend.agents.schemas import PortfolioDecision, Step5Output


class PortfolioManagerAgent:
    def __init__(self):
        self.agent_name = "PortfolioManagerAgent (Step 5)"
        self.firm_name = "nv analytics"

    def run(self, ticker: str, step4_research: dict[str, Any] | None = None, past_lessons: str = "") -> dict[str, Any]:
        """
        Executes Step 5: Portfolio Manager Decision.
        Simulates an LLM parsing the deep research to formulate an actionable portfolio allocation.
        """
        step4_research = step4_research or {}
        
        # Simulate LLM logic based on step 4 research
        action: Literal["BUY", "SELL", "HOLD", "OVERWEIGHT", "UNDERWEIGHT"] = "HOLD"
        confidence = 50
        reasoning = "Insufficient data to make a strong directional call."
        
        news = step4_research.get("section8_news_catalysts", {})
        sentiment_score = news.get("composite_sentiment_score", 0.0)
        
        if sentiment_score > 0.3:
            action = "BUY"
            confidence = 85
            reasoning = f"Strong positive catalyst flow with an AI sentiment score of {sentiment_score}. Fundamental factors support accumulation."
        elif sentiment_score > 0.1:
            action = "OVERWEIGHT"
            confidence = 65
            reasoning = "Mildly positive catalysts. Recommend overweighting slightly relative to benchmark."
        elif sentiment_score < -0.3:
            action = "SELL"
            confidence = 80
            reasoning = f"Significant negative catalysts (Score: {sentiment_score}). Recommend exiting positions."
        elif sentiment_score < -0.1:
            action = "UNDERWEIGHT"
            confidence = 60
            reasoning = "Deteriorating near-term momentum. Reduce exposure."
            
        if past_lessons:
            reasoning += f"\n\nMEMORY REFLECTION (Past Lessons):\n{past_lessons}"

        decision = PortfolioDecision(
            ticker=ticker,
            action=action,
            confidence_score=confidence,
            reasoning=reasoning
        )
        
        result = {
            "step": 5,
            "step_title": "Portfolio Manager Decision",
            "firm": self.firm_name,
            "decision": decision.model_dump(),
            "status": "COMPLETED"
        }
        return Step5Output.model_validate(result).model_dump()
