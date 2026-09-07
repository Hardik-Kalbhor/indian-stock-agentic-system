import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Any

from pydantic import BaseModel, Field

from backend.agents.schemas import (
    FullPipelineResponse,
    Step1Output,
    Step2Output,
    Step3Output,
    Step4Output,
    Step5Output,
    Step6Output,
)
from backend.agents.step1_industry_identifier import IndustryIdentifierAgent
from backend.agents.step2_industry_shortlist import IndustryShortlistAgent
from backend.agents.step3_company_comparator import CompanyComparatorAgent
from backend.agents.step4_stock_researcher import StockResearcherAgent
from backend.agents.step5_portfolio_manager import PortfolioManagerAgent
from backend.agents.step6_execution_trader import ExecutionTraderAgent

app = FastAPI(
    title="nv analytics | Indian Stock Market Multi-Agent Analysis Engine",
    description="Agentic AI System for Indian Equity Markets supporting individual step execution and sequential pipeline analysis.",
    version="2.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Payloads
class Step2Request(BaseModel):
    sector_name: str = "Renewable Energy & Green Power"
    market_cap_filter: str = "all"   # "large", "mid", "small", "all"
    price_min: int | None = 0               # min share price filter (₹)
    price_max: int | None = 5000            # max share price filter (₹)

class Step3Request(BaseModel):
    sector_name: str = "Renewable Energy & Green Power"
    tickers: list[str] = []

class Step4Request(BaseModel):
    ticker: str = "IREDA.NS"

class Step5Request(BaseModel):
    ticker: str = "IREDA.NS"
    step4_research: dict[str, Any] = Field(default_factory=dict)
    past_lessons: str = ""

class Step6Request(BaseModel):
    decision: dict[str, Any] = Field(default_factory=lambda: {
        "ticker": "IREDA.NS",
        "action": "HOLD",
        "confidence_score": 50,
        "reasoning": "Standard execution plan.",
    })

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatbotRequest(BaseModel):
    messages: list[ChatMessage]
    context_data: dict
    active_ticker: str | None = None


class FullPipelineRequest(BaseModel):
    sector_name: str = "Renewable Energy & Green Power"
    ticker: str = "IREDA.NS"
    compare_tickers: list[str] = []

# API Endpoints
@app.get("/api/health")
def health_check():
    return {"status": "ONLINE", "firm": "nv analytics", "market": "NSE / BSE India"}

@app.get("/api/step1", response_model=Step1Output)
@app.post("/api/step1", response_model=Step1Output)
def execute_step1():
    """Step 1: Industry Identification & Growth Sector Research."""
    agent = IndustryIdentifierAgent()
    return agent.run()

@app.post("/api/step2", response_model=Step2Output)
def execute_step2(req: Step2Request):
    """Step 2: Industry Analysis and Stock Shortlist."""
    agent = IndustryShortlistAgent()
    return agent.run(
        sector_name=req.sector_name,
        market_cap_filter=req.market_cap_filter,
        price_min=req.price_min if req.price_min is not None else 0,
        price_max=req.price_max if req.price_max is not None else 5000
    )

@app.post("/api/step3", response_model=Step3Output)
def execute_step3(req: Step3Request):
    """Step 3: Company Comparison Deep Research Engine."""
    agent = CompanyComparatorAgent()
    return agent.run(tickers=req.tickers, sector_name=req.sector_name)

@app.post("/api/step4", response_model=Step4Output)
def execute_step4(req: Step4Request):
    """Step 4: Stock Research & Bull/Bear Debate."""
    agent = StockResearcherAgent()
    return agent.run(ticker=req.ticker)

@app.post("/api/step5", response_model=Step5Output)
def execute_step5(req: Step5Request):
    """Step 5: Portfolio Manager Strategic Asset Allocation."""
    agent = PortfolioManagerAgent()
    return agent.run(
        ticker=req.ticker,
        step4_research=req.step4_research,
        past_lessons=req.past_lessons
    )

@app.post("/api/step6", response_model=Step6Output)
def execute_step6(req: Step6Request):
    """Step 6: Execution Trader Execution Planning."""
    agent = ExecutionTraderAgent()
    return agent.run(decision=req.decision)

@app.get("/api/news/{ticker}")
def get_stock_news(ticker: str):
    """Fetches real-time market news and executes AI-powered fundamental catalyst scoring."""
    from backend.services.news_engine import news_scoring_agent
    summary = news_scoring_agent.get_ticker_sentiment_summary(ticker)
    return JSONResponse(content=summary)

@app.post("/api/pipeline", response_model=FullPipelineResponse)
def execute_full_pipeline(req: FullPipelineRequest):
    """Executes all 6 steps in sequence using LangGraph state machine."""
    from backend.graph.pipeline_graph import pipeline_graph
    
    # Initialize state with user preferences from request
    initial_state = {
        "user_sector_name": req.sector_name,
        "user_target_ticker": req.ticker,
        "user_compare_tickers": req.compare_tickers if req.compare_tickers else None
    }
    
    # Invoke the compiled LangGraph
    final_state = pipeline_graph.invoke(initial_state)
    
    return {
        "system": "nv analytics Multi-Agent LangGraph Pipeline",
        "pipeline_status": "COMPLETED",
        "step1": final_state.get("step1_result"),
        "step2": final_state.get("step2_result"),
        "step3": final_state.get("step3_result"),
        "step4": final_state.get("step4_result"),
        "step5": final_state.get("step5_result"),
        "step6": final_state.get("step6_result")
    }

@app.post("/api/chat")
def chat_with_agent(req: ChatbotRequest):
    """Chat with the Institutional Equity Strategist AI."""
    from backend.services.chatbot_service import ChatbotService
    chatbot = ChatbotService()
    user_msgs = [{"role": msg.role, "content": msg.content} for msg in req.messages]
    reply = chatbot.get_response(user_msgs, req.context_data, req.active_ticker)
    return JSONResponse(content={"reply": reply})


# Serve Static Assets & HTML Routes
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/api/auth/config")
def get_auth_config():
    """Returns the public Supabase configuration for client-side authentication."""
    return JSONResponse(content={
        "supabase_url": os.getenv("SUPABASE_URL", ""),
        "supabase_anon_key": os.getenv("SUPABASE_ANON_KEY", "")
    })

@app.get("/", response_class=HTMLResponse)
def read_root():
    index_file = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r") as f:
            return f.read()
    return "<h1>nv analytics Server is running!</h1>"

@app.get("/login", response_class=HTMLResponse)
@app.get("/login.html", response_class=HTMLResponse)
def read_login():
    login_file = os.path.join(os.path.dirname(__file__), "..", "frontend", "login.html")
    if os.path.exists(login_file):
        with open(login_file, "r") as f:
            return f.read()
    return "<h1>Login page not found</h1>"

@app.get("/step2-dashboard.html", response_class=HTMLResponse)
def read_step2_dashboard():
    file_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "step2-dashboard.html")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return "<h1>Step 2 Dashboard loading...</h1>"

@app.get("/step3-dashboard.html", response_class=HTMLResponse)
def read_step3_dashboard():
    file_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "step3-dashboard.html")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return "<h1>Step 3 Dashboard loading...</h1>"

@app.get("/step4-dashboard.html", response_class=HTMLResponse)
def read_step4_dashboard():
    file_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "step4-dashboard.html")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return "<h1>Step 4 Dashboard loading...</h1>"

@app.get("/india-growth-sectors-20260804.html", response_class=HTMLResponse)
def read_growth_sectors_20260804():
    file_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "india-growth-sectors-20260804.html")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return "<h1>Growth Sectors 2026-08-04 Report loading...</h1>"

@app.get("/india-growth-sectors-20260803.html", response_class=HTMLResponse)
def read_growth_sectors_20260803():
    file_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "india-growth-sectors-20260803.html")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return "<h1>Growth Sectors 2026-08-03 Report loading...</h1>"
