# Community 1

> 18 nodes · cohesion 0.20

## Key Concepts

- **MarketDataService** (12 connections) — `backend/services/market_data_service.py`
- **CompanyComparatorAgent** (7 connections) — `backend/agents/step3_company_comparator.py`
- **StockResearcherAgent** (7 connections) — `backend/agents/step4_stock_researcher.py`
- **.run()** (6 connections) — `backend/agents/step3_company_comparator.py`
- **.run()** (5 connections) — `backend/agents/step4_stock_researcher.py`
- **market_data_service.py** (5 connections) — `backend/services/market_data_service.py`
- **.calculate_technicals()** (5 connections) — `backend/services/market_data_service.py`
- **step3_company_comparator.py** (4 connections) — `backend/agents/step3_company_comparator.py`
- **step4_stock_researcher.py** (4 connections) — `backend/agents/step4_stock_researcher.py`
- **.get_company_fundamentals()** (4 connections) — `backend/services/market_data_service.py`
- **.get_stock_data()** (4 connections) — `backend/services/market_data_service.py`
- **._generate_mock_price_series()** (3 connections) — `backend/services/market_data_service.py`
- **.get_sector_tickers()** (3 connections) — `backend/services/market_data_service.py`
- **.__init__()** (1 connections) — `backend/agents/step3_company_comparator.py`
- **Executes Step 3: Company Comparison Deep Research Engine with 6 Institutional…** (1 connections) — `backend/agents/step3_company_comparator.py`
- **Executes Step 4: Comprehensive Equity Analysis Report with 6 Institutional…** (1 connections) — `backend/agents/step4_stock_researcher.py`
- **.__init__()** (1 connections) — `backend/agents/step4_stock_researcher.py`
- **DataFrame** (1 connections)

## Relationships

- [Community 2](Community_2.md) (5 shared connections)
- [Community 3](Community_3.md) (4 shared connections)
- [Community 4](Community_4.md) (2 shared connections)
- [Community 5](Community_5.md) (1 shared connections)
- [Community 6](Community_6.md) (1 shared connections)
- [Community 0](Community_0.md) (1 shared connections)

## Source Files

- `backend/agents/step3_company_comparator.py`
- `backend/agents/step4_stock_researcher.py`
- `backend/services/market_data_service.py`

## Audit Trail

- EXTRACTED: 37 (84%)
- INFERRED: 7 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*