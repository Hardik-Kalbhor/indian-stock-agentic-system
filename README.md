# NV Analytics | Indian Stock Market Multi-Agent Analysis Engine

An autonomous agentic AI system for Indian Equity Markets (NSE/BSE) powered by FastAPI, LangGraph, Google Gemini, Groq, and Screener/Yahoo Finance data.

## Features

- **6-Step Sequential & Modular Pipeline:**
  1. **Step 1: Industry Identification** — Macro trend analysis & top growth sectors.
  2. **Step 2: Industry Shortlist** — Hard filters, market cap screening, F&O Smart Money positioning.
  3. **Step 3: Company Comparator** — DuPont ROE breakdown, Jensen's Alpha, Beta, Cash conversion, and Peer Benchmarking.
  4. **Step 4: Deep Stock Researcher** — Bull/Bear debates, SOTP valuation matrices, and fundamental catalysts.
  5. **Step 5: Portfolio Manager** — Institutional asset allocation decision engine with reflection memory.
  6. **Step 6: Execution Trader** — Dynamic trade plans with entry price, ATR-based stop-loss, targets, and sizing.
- **Institutional Advisor Chatbot** — Powered by Google Gemini (`gemini-3.8-flash`) grounded strictly in pipeline data.
- **Interactive Dashboards** — Vanilla HTML5/Tailwind/ApexCharts web UI served directly by FastAPI.

## Setup & Installation

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/<your-username>/indian-stock-agentic-system.git
cd indian-stock-agentic-system

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

### 3. Run Locally
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

## Deployment (Render)

This repository includes a `render.yaml` specification for deploying as a single Python Web Service on Render.
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 1`
