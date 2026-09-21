"""10-year financial ratio analysis for SK hynix.
The CSV may contain 2015 as an opening-balance support year; displayed analysis is 2016-2025.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "financial_data.csv").set_index("year").sort_index()
analysis = df.loc[2016:2025].copy()

analysis["revenue_growth"] = analysis["revenue"].pct_change()
analysis["operating_margin"] = analysis["operating_income"] / analysis["revenue"]
analysis["net_margin"] = analysis["net_income"] / analysis["revenue"]
analysis["debt_to_equity"] = analysis["total_liabilities"] / analysis["total_equity"]
analysis["equity_ratio"] = analysis["total_equity"] / analysis["total_assets"]
analysis["current_ratio"] = analysis["current_assets"] / analysis["current_liabilities"]
analysis["cfo_to_revenue"] = analysis["operating_cash_flow"] / analysis["revenue"]
analysis["cfo_to_net_income"] = analysis["operating_cash_flow"] / analysis["net_income"]
analysis["fcf"] = analysis["operating_cash_flow"] - analysis["capex"]
analysis["capex_to_revenue"] = analysis["capex"] / analysis["revenue"]

avg_assets = (df["total_assets"] + df["total_assets"].shift(1)) / 2
avg_equity = (df["total_equity"] + df["total_equity"].shift(1)) / 2
analysis["roa"] = analysis["net_income"] / avg_assets.loc[analysis.index]
analysis["roe"] = analysis["net_income"] / avg_equity.loc[analysis.index]
analysis["asset_turnover"] = analysis["revenue"] / avg_assets.loc[analysis.index]

print(analysis.round(4).to_string())
