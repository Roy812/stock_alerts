import os
from calendar import monthrange
from datetime import date, datetime
from typing import Any

import requests

from repository import stock_repository, stock_earnings_repository


def current_month_date_range() -> tuple[str, str]:
    today = date.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=monthrange(today.year, today.month)[1])
    return first_day.isoformat(), last_day.isoformat()


def get_earnings(from_date: str, to_date: str) -> list[dict[str, Any]]:
    response = requests.get(
        "https://financialmodelingprep.com/stable/earnings-calendar",
        params={
            "from": from_date,
            "to": to_date,
            "apikey": os.environ.get("FMP_API_KEY"),
        },
        timeout=15,
    )
    response.raise_for_status()
    events = response.json()

    stocks = stock_repository.get_all_stocks()
    tickers = {stock["ticker"].upper() for stock in stocks}

    return [
        event for event in events
        if event.get("symbol", "").upper() in tickers
    ]


def save_earnings_event(event: dict[str, Any]) -> str:
    ticker = event.get("symbol")
    earnings_date = event.get("date")
    if not ticker or not earnings_date:
        raise ValueError("An earnings event must include a ticker and date")

    existing = stock_earnings_repository.get_stock_earnings(
        ticker=ticker,
        date=earnings_date,
    )
    updates = {
        "revenue_estimated": event.get("revenueEstimated"),
        "revenue_actual": event.get("revenueActual"),
        "eps_estimated": event.get("epsEstimated"),
        "eps_actual": event.get("epsActual"),
    }
    if existing:
        stock_earnings_id = existing[0].get("stock_earnings_id")
        if stock_earnings_id is None:
            raise ValueError(
                f"Existing earnings for {ticker} on {earnings_date} "
                "has no stock_earnings_id"
            )
        stock_earnings_repository.update_stock_earnings(
            stock_earnings_id=stock_earnings_id,
            updates=updates,
        )
        print(f"Updated earnings for {ticker} on {earnings_date}")
        return "updated"

    stock_earnings_repository.add_stock_earnings(
        ticker=ticker,
        date=earnings_date,
        **updates,
    )
    return "inserted"


if __name__ == "__main__":
    try:
        requests.post(
            "https://ntfy.sh/stock_alerts",
            data="Started stock earnings wf on: "
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        for event in get_earnings(*current_month_date_range()):
            save_earnings_event(event)
        requests.post(
            "https://ntfy.sh/stock_alerts",
            data="Stock earnings fetched successfully",
        )
    except Exception:
        requests.post(
            "https://ntfy.sh/stock_alerts", 
            data="Failed to fetch stock earnings",
            )