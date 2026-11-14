from datetime import date
import os
from supabase import create_client, Client


def create_supabase_client():
    sb_url = os.environ.get("SUPABASE_URL")
    sb_key = os.environ.get("SUPABASE_KEY")
    sb_client: Client = create_client(sb_url, sb_key)
    print("Supabase client created successfully!")
    return sb_client


def add_stock_price_history(ticker: str, price: float, volume: int):
    if not ticker or not price:
        raise ValueError("Incomplete data")

    data = {
        "ticker": ticker,
        "price": price,
        "volume": volume,
        "date": date.today().strftime("%Y-%m-%d")
    }
    try:
        response = create_supabase_client().table("stock_price_history").insert(data).execute()
        print("Inserted stock price history:", response.data)
        return response.data
    except:
        print("Unable to insert stock price history:", data)


def get_stock_price_history(ticker: str):
    if not ticker:
        return []

    response = (
        create_supabase_client()
        .table("stock_price_history")
        .select("*")
        .eq("ticker", ticker)
        .execute()
    )
    return response.data


def update_stock_price_history(stock_price_history_id: int, price: float):
    if stock_price_history_id <= 0:
        raise ValueError("A valid stock price history ID is required")

    try:
        response = (
            create_supabase_client()
            .table("stock_price_history")
            .update({"price": price})
            .eq("stock_price_history_id", stock_price_history_id)
            .execute()
        )
        print("Unable to update stock price history from id:", stock_price_history_id)
        return response.data
    except:
        print("Unable to update stock price history from id:", stock_price_history_id)


def delete_stock_price_history(ticker: str):
    if not ticker:
        raise ValueError("A ticker is required")

    try:
        response = (
            create_supabase_client()
            .table("stock_price_history")
            .delete()
            .eq("ticker", ticker)
            .execute()
        )
        print("Deleted stock price history for ticker:", ticker)
        return response.data
    except:
        print("Unable to delete stock price history for ticker:", ticker)
