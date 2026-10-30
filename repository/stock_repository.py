import os
from supabase import create_client, Client
import psycopg2
from datetime import datetime, date
from typing import Sequence, TypedDict


class Stock(TypedDict):
    ticker: str
    company_name: str
    category: str
    price: float

def create_supabase_db():
    # Connecting to PostgreSQL database
    try:
        connection_string = os.environ.get("sb_connection_string_shared")
        print("Connection string:", connection_string)
        conn = psycopg2.connect(connection_string)
        print("Connected to the database successfully!")

        cursor = conn.cursor()
        print("Cursor created successfully!")

        cursor.execute("CREATE TABLE IF NOT EXISTS stock (" \
                            "ticker TEXT PRIMARY KEY, " \
                            "company_name TEXT NOT NULL, " \
                            "price NUMERIC(10, 2), " \
                            "category TEXT, " \
                            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, " \
                            "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP" \
                        ");"
                        )

        cursor.execute("CREATE TABLE IF NOT EXISTS stock_price_history (" \
                                    "stock_price_history_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, " \
                                    "ticker TEXT NOT NULL REFERENCES stock(ticker), " \
                                    "price NUMERIC(10, 2), " \
                                    "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, " \
                                    "price_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP" \
                                ");"
                                )

        conn.commit()
        print("Table(s) created successfully if not exists!")

        cursor.close()
        conn.close()
        print("Cursor and connection closed successfully!")
    except Exception as error:
        print(f"Database operation failed: {error}")

def create_supabase_client():
    sb_url = os.environ.get("SUPABASE_URL")
    sb_key = os.environ.get("SUPABASE_KEY")
    sb_client: Client = create_client(sb_url, sb_key)
    print("Supabase client created successfully!")
    return sb_client 

def add_stock_price_history(ticker: str, price: float):
    if not ticker or not price:
        raise ValueError("Incomplete data")
       
    data = {
        "ticker": ticker,
        "price": price
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

def delete_stock_price_history(stock_price_history_id: int):
    if stock_price_history_id <= 0:
        raise ValueError("A valid stock price history ID is required")

    try:
        response = (
                create_supabase_client()
                .table("stock_price_history")
                .delete()
                .eq("stock_price_history_id", stock_price_history_id)
                .execute()
            )
        print("Deleted stock price history from id:", stock_price_history_id)
        return response.data
    except:
        print("Unable to delete stock price history from id:", stock_price_history_id)


def add_stocks(stocks: Sequence[Stock]):
    if not stocks:
        raise ValueError("At least one stock is required")

    now = datetime.now().isoformat()
    data = [
        {
            **stock,
            "created_at": now,
            "updated_at": now
        }
        for stock in stocks
    ]
    if create_supabase_client().table("stock").insert(data).execute():
        print("Inserted stocks:", data)
    else:
        print("Unable to insert stocks:", data)

def get_stocks(tickers: Sequence[str]):
    if not tickers:
        return []
    response = create_supabase_client().table("stock").select("*").in_("ticker", list(tickers)).execute()
    return response.data

def get_all_stocks():
    response = create_supabase_client().table("stock").select("*").execute()
    return response.data

def update_stocks(stocks: Sequence[Stock]):
    if stocks is None or len(stocks) == 0:
        raise ValueError("At least one stock is required")

    for stock in stocks:
        data = {
            **stock,
            "updated_at": datetime.now().isoformat()
        }
        
        if create_supabase_client().table("stock").update(data).eq("ticker", stock["ticker"]).execute():
            print("Updated stock:", stock)
        else:
            print("Unable to update stock:", stock)
   

def delete_stocks(tickers: Sequence[str]):
    if not tickers:
        raise ValueError("At least one ticker is required")

    if create_supabase_client().table("stock").delete().in_("ticker", list(tickers)).execute():
        print("Deleted stocks with tickers:", list(tickers))
    else:
        print("Unable to delete stocks with tickers:", list(tickers))
