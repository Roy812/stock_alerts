import os
from typing import TypedDict

from supabase import Client, create_client


class StockEarningsUpdate(TypedDict, total=False):
    ticker: str
    date: str | None
    revenue_estimated: int | None
    revenue_actual: int | None
    eps_estimated: int | None
    eps_actual: int | None


def create_supabase_client() -> Client:
    sb_url = os.environ.get("SUPABASE_URL")
    sb_key = os.environ.get("SUPABASE_KEY")
    sb_client: Client = create_client(sb_url, sb_key)
    print("Supabase client created successfully!")
    return sb_client


def add_stock_earnings(
    ticker: str,
    date: str | None = None,
    revenue_estimated: int | None = None,
    revenue_actual: int | None = None,
    eps_estimated: int | None = None,
    eps_actual: int | None = None,
):
    if not ticker:
        raise ValueError("A ticker is required")

    data = {
        "ticker": ticker,
        "date": date,
        "revenue_estimated": revenue_estimated,
        "revenue_actual": revenue_actual,
        "eps_estimated": eps_estimated,
        "eps_actual": eps_actual,
    }
    response = create_supabase_client().table("stock_earnings").insert(data).execute()
    return response.data


def get_stock_earnings(ticker: str):
    if not ticker:
        return []

    response = (
        create_supabase_client()
        .table("stock_earnings")
        .select("*")
        .eq("ticker", ticker)
        .execute()
    )
    return response.data


def update_stock_earnings(
    stock_earnings_id: int, updates: StockEarningsUpdate
):
    if stock_earnings_id <= 0:
        raise ValueError("A valid stock earnings ID is required")
    if not updates:
        raise ValueError("At least one stock earnings field is required")
    if "ticker" in updates and not updates["ticker"]:
        raise ValueError("A ticker is required")

    allowed_fields = {
        "ticker",
        "date",
        "revenue_estimated",
        "revenue_actual",
        "eps_estimated",
        "eps_actual",
    }
    if not set(updates).issubset(allowed_fields):
        raise ValueError("Unsupported stock earnings field")

    response = (
        create_supabase_client()
        .table("stock_earnings")
        .update(updates)
        .eq("stock_earnings_id", stock_earnings_id)
        .execute()
    )
    return response.data


def delete_stock_earnings(stock_earnings_id: int):
    if stock_earnings_id <= 0:
        raise ValueError("A valid stock earnings ID is required")

    response = (
        create_supabase_client()
        .table("stock_earnings")
        .delete()
        .eq("stock_earnings_id", stock_earnings_id)
        .execute()
    )
    return response.data