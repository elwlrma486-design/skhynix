"""Fetch 2015-2025 DART data; dashboard displays 2016-2025."""
from pathlib import Path
import pandas as pd
from dart_api import fetch_annual_financials, get_api_key, save_raw

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUT = ROOT / "data" / "financial_data.csv"
START_YEAR = 2015
END_YEAR = 2025

ALIASES = {
    "revenue": ["매출액", "수익(매출액)", "Revenue"],
    "operating_income": ["영업이익", "영업이익(손실)", "Operating income"],
    "net_income": ["당기순이익", "당기순이익(손실)", "Profit (loss) for the period"],
    "total_assets": ["자산총계", "Total assets"],
    "total_liabilities": ["부채총계", "Total liabilities"],
    "total_equity": ["자본총계", "Total equity"],
    "current_assets": ["유동자산", "Current assets"],
    "current_liabilities": ["유동부채", "Current liabilities"],
    "cash_and_equivalents": ["현금및현금성자산", "현금 및 현금성자산", "Cash and cash equivalents"],
    "inventory": ["재고자산", "Inventories"],
    "operating_cash_flow": ["영업활동으로 인한 현금흐름", "영업활동 현금흐름", "Net cash flows from operating activities"],
    "capex": ["유형자산의 취득", "유형자산 취득", "Acquisition of property, plant and equipment"],
}

def clean_amount(value):
    if value in (None, ""):
        return None
    return float(str(value).replace(",", "").replace(" ", ""))

def pick(rows, aliases):
    for alias in aliases:
        for row in rows:
            if row.get("account_nm") == alias:
                return clean_amount(row.get("thstrm_amount"))
    for alias in aliases:
        target = alias.replace(" ", "").lower()
        for row in rows:
            name = str(row.get("account_nm", "")).replace(" ", "").lower()
            if target in name:
                return clean_amount(row.get("thstrm_amount"))
    return None

def main():
    get_api_key()
    records = []
    for year in range(START_YEAR, END_YEAR + 1):
        rows = fetch_annual_financials(year, "CFS")
        save_raw({"status": "000", "list": rows}, year, RAW_DIR)
        record = {"year": year}
        for key, aliases in ALIASES.items():
            record[key] = pick(rows, aliases)
        records.append(record)
    df = pd.DataFrame(records).sort_values("year")
    df.to_csv(OUT, index=False)
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
