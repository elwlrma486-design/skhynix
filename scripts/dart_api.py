"""DART Open API client."""
import os
from pathlib import Path
from typing import Any
import requests

BASE_URL = "https://opendart.fss.or.kr/api"
CORP_CODE = os.getenv("DART_CORP_CODE", "00164779")
ANNUAL_REPORT = "11011"

def get_api_key():
    key = os.getenv("DART_API_KEY")
    if not key:
        raise RuntimeError("DART_API_KEY 환경변수를 설정하세요.")
    return key

def request_json(endpoint: str, params: dict[str, str]) -> dict[str, Any]:
    r = requests.get(f"{BASE_URL}/{endpoint}.json", params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if data.get("status") != "000":
        raise RuntimeError(f"DART API 오류: {data.get('status')} / {data.get('message')}")
    return data

def fetch_annual_financials(year: int, fs_div: str = "CFS"):
    params = {
        "crtfc_key": get_api_key(),
        "corp_code": CORP_CODE,
        "bsns_year": str(year),
        "reprt_code": ANNUAL_REPORT,
        "fs_div": fs_div,
    }
    return request_json("fnlttSinglAcntAll", params).get("list", [])

def save_raw(data, year: int, output_dir: Path):
    import json
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"financials_{year}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
