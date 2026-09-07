from typing import Any

import numpy as np
import pandas as pd
import yfinance as yf


def get_benchmark_ticker(ticker: str) -> str:
    """Maps an Indian stock ticker to its appropriate benchmark index."""
    if ticker.endswith(".NS"):
        return "^NSEI"  # Nifty 50
    elif ticker.endswith(".BO"):
        return "^BSESN" # BSE Sensex
    # Default to Nifty 50 for Indian equities
    return "^NSEI"

class BenchmarkService:
    @staticmethod
    def calculate_alpha_beta(ticker: str, period: str = "1y", risk_free_rate: float = 0.07) -> dict[str, Any]:
        """
        Calculates Beta, Total Return, Benchmark Return, and Alpha.
        Assumes Indian risk-free rate of ~7% (0.07) for Jensen's Alpha.
        """
        benchmark_ticker = get_benchmark_ticker(ticker)
        
        try:
            from backend.services.market_data_service import MarketDataService
            stock_data = MarketDataService.get_stock_data(ticker)
            bench_data = MarketDataService.get_stock_data(benchmark_ticker)
            
            if stock_data.empty or bench_data.empty:
                return {"error": "Insufficient data"}
                
            stock_close = stock_data['Close']
            bench_close = bench_data['Close']
            
            # Combine into single dataframe and drop NaNs
            df = pd.concat([stock_close, bench_close], axis=1)
            df.columns = ['Stock', 'Benchmark']
            df = df.dropna()
            
            if len(df) < 10:
                return {"error": "Insufficient overlapping data points"}
                
            # Calculate daily returns
            returns = df.pct_change().dropna()
            stock_returns = returns['Stock']
            bench_returns = returns['Benchmark']
            
            # 1. Calculate Beta
            covariance = np.cov(stock_returns, bench_returns)[0][1]
            variance = np.var(bench_returns)
            beta = covariance / variance if variance != 0 else 1.0
            
            # 2. Calculate Total Returns
            stock_total_return = (df['Stock'].iloc[-1] / df['Stock'].iloc[0]) - 1
            bench_total_return = (df['Benchmark'].iloc[-1] / df['Benchmark'].iloc[0]) - 1
            
            # 3. Calculate Relative Alpha (Simple Outperformance)
            relative_alpha = stock_total_return - bench_total_return
            
            # 4. Calculate Annualized Returns (assuming 252 trading days)
            days = (df.index[-1] - df.index[0]).days
            years = days / 365.25 if days > 0 else 1
            
            if years > 0:
                stock_cagr = ((1 + stock_total_return) ** (1/years)) - 1
                bench_cagr = ((1 + bench_total_return) ** (1/years)) - 1
            else:
                stock_cagr = stock_total_return
                bench_cagr = bench_total_return
                
            # 5. Calculate Jensen's Alpha
            # Alpha = Portfolio Return - [Risk Free Rate + Beta * (Market Return - Risk Free Rate)]
            jensens_alpha = stock_cagr - (risk_free_rate + beta * (bench_cagr - risk_free_rate))
            
            return {
                "benchmark_index": benchmark_ticker,
                "period": period,
                "beta": float(round(beta, 2)),
                "stock_total_return_pct": float(round(stock_total_return * 100, 2)),
                "benchmark_total_return_pct": float(round(bench_total_return * 100, 2)),
                "relative_alpha_pct": float(round(relative_alpha * 100, 2)),
                "jensens_alpha_pct": float(round(jensens_alpha * 100, 2))
            }
            
        except Exception as e:
            return {"error": str(e)}

benchmark_service = BenchmarkService()
