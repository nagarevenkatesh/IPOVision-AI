# backend/app/services/live_ipo_service.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.ipo import IPO

NSE_IPO_URL = "https://www.nseindia.com/market-data/all-upcoming-issues-ipo"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_nse_html():
    s = requests.Session()
    s.get("https://www.nseindia.com", headers=HEADERS, timeout=20)
    r = s.get(NSE_IPO_URL, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.text


def sync_live_ipos(db: Session):
    html = fetch_nse_html()
    soup = BeautifulSoup(html, "html.parser")

    # This is intentionally defensive: if NSE changes layout, it will not crash the app.
    rows = soup.find_all("tr")
    saved = 0

    for row in rows:
        cols = [c.get_text(" ", strip=True) for c in row.find_all(["td", "th"])]
        if len(cols) < 6:
            continue

        company_name = cols[0]
        ticker = cols[1] if len(cols) > 1 else ""
        issue_start = cols[2] if len(cols) > 2 else ""
        issue_end = cols[3] if len(cols) > 3 else ""
        status = cols[4] if len(cols) > 4 else ""

        if not company_name or not ticker:
            continue

        existing = db.query(IPO).filter(IPO.ticker == ticker).first()
        if existing:
            continue

        try:
            listing_date = datetime.today().date()
        except Exception:
            continue

        ipo = IPO(
            company_name=company_name,
            ticker=ticker,
            sector=status or "",
            exchange="NSE",
            issue_price=0.0,
            listing_date=listing_date,
        )
        db.add(ipo)
        saved += 1

    db.commit()
    return {"saved": saved, "total_fetched": saved}