import pandas as pd

df = pd.read_csv("../data/financial_data.csv").set_index("year")

def avg(series, year):
    return (series.loc[year] + series.loc[year - 1]) / 2

rows = []
for year in df.index:
    avg_assets = avg(df["total_assets"], year) if year > df.index.min() else None
    avg_equity = avg(df["total_equity"], year) if year > df.index.min() else None
    rows.append({
        "year": year,
        "revenue_growth": None if year == df.index.min() else df.loc[year, "revenue"] / df.loc[year-1, "revenue"] - 1,
        "operating_margin": df.loc[year, "operating_income"] / df.loc[year, "revenue"],
        "net_margin": df.loc[year, "net_income"] / df.loc[year, "revenue"],
        "roa": None if avg_assets is None else df.loc[year, "net_income"] / avg_assets,
        "roe": None if avg_equity is None else df.loc[year, "net_income"] / avg_equity,
        "debt_to_equity": df.loc[year, "total_liabilities"] / df.loc[year, "total_equity"],
        "equity_ratio": df.loc[year, "total_equity"] / df.loc[year, "total_assets"],
        "current_ratio": df.loc[year, "current_assets"] / df.loc[year, "current_liabilities"],
        "asset_turnover": None if avg_assets is None else df.loc[year, "revenue"] / avg_assets,
        "cfo_to_revenue": df.loc[year, "operating_cash_flow"] / df.loc[year, "revenue"],
        "cfo_to_net_income": None if df.loc[year, "net_income"] == 0 else df.loc[year, "operating_cash_flow"] / df.loc[year, "net_income"],
        "fcf": None if pd.isna(df.loc[year, "capex"]) else df.loc[year, "operating_cash_flow"] - df.loc[year, "capex"],
        "capex_to_revenue": None if pd.isna(df.loc[year, "capex"]) else df.loc[year, "capex"] / df.loc[year, "revenue"],
    })

ratios = pd.DataFrame(rows).set_index("year")
print(ratios.round(4))
